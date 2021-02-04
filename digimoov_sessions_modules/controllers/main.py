from odoo import fields, http, SUPERUSER_ID, tools, _

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from werkzeug.exceptions import Forbidden, NotFound
from datetime import datetime,date

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class WebsiteSale(WebsiteSale):

    @http.route(['''/<string:product>/<string:partenaire>/shop/cart''','''/<string:product>/shop/cart''','''/shop/cart'''], type='http', auth="user", website=True, sitemap=False)
    def cart(self, access_token=None,product=None, revive='',partenaire=None, **post):
        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        order = request.website.sale_get_order()
        print(order)
        if order.company_id.id==1 and (partenaire or product):
            return request.redirect("/shop/cart/")
        if order and order.company_id.id==2:
            product_id = False
            if order:
                for line in order.order_line:
                    product_id = line.product_id

            if not product and not partenaire and product_id:
                product=True
                partenaire=True
            if product and not partenaire:
                if product_id:
                    slugname = (product_id.name).strip().strip('-').replace(' ', '-').lower()
                    if str(slugname) != str(product):
                        if order.pricelist_id and order.pricelist_id.name in ['ubereats','deliveroo','coursierjob']:
                            return request.redirect("/%s/%s/shop/cart/"% (slugname,order.pricelist_id.name))
                        else:
                            return request.redirect("/%s/shop/cart/"% (slugname))
                    else:
                        if order.pricelist_id and order.pricelist_id.name in ['ubereats','deliveroo','coursierjob']:
                            return request.redirect("/%s/%s/shop/cart/"% (slugname,order.pricelist_id.name))
                else:
                    return request.redirect("/pricing")
            elif product and partenaire:
                if product_id:
                    slugname = (product_id.name).strip().strip('-').replace(' ', '-').lower()
                    if str(slugname) != str(product):
                        pricelist = request.env['product.pricelist'].sudo().search(
                            [('company_id', '=', 2), ('name', "=", str(partenaire))])
                        if not pricelist:
                            pricelist_id=order.pricelist_id
                            if pricelist_id.name in ['ubereats','deliveroo','coursierjob']:
                                return request.redirect("/%s/%s/shop/cart/" % (slugname,pricelist_id.name))
                            else:
                                return request.redirect("/%s/shop/cart/" % (slugname))
                        else:
                            if pricelist.name in ['ubereats','deliveroo','coursierjob']:
                                return request.redirect("/%s/%s/shop/cart/" % (slugname, order.pricelist_id.name))
                            else:
                                return request.redirect("/%s/shop/cart/" % (slugname))
                    else:
                        pricelist = request.env['product.pricelist'].sudo().search(
                            [('company_id', '=', 2), ('name', "=", str(partenaire))])

                        if not pricelist:
                            pricelist_id=order.pricelist_id
                            if pricelist_id.name in ['ubereats','deliveroo','coursierjob']:
                                return request.redirect("/%s/%s/shop/cart/" % (slugname,pricelist_id.name))
                            else:
                                return request.redirect("/%s/shop/cart/" % (slugname))
                        else:
                            if pricelist.name in ['ubereats','deliveroo','coursierjob']:
                                if pricelist.name != order.pricelist_id.name:
                                    return request.redirect("/%s/%s/shop/cart/" % (slugname, order.pricelist_id.name))
                            else:
                                return request.redirect("/%s/shop/cart/" % (slugname))
                else:
                    pricelist = request.env['product.pricelist'].sudo().search(
                        [('company_id', '=', 2), ('name', "=", str(partenaire))])
                    if pricelist and pricelist.name in ['ubereats','deliveroo','coursierjob']:
                        return request.redirect("/%s" % (pricelist.name))
                    else:
                        return request.redirect("/pricing")
        list_products = []
        if order:
            for line in order.order_line:
                list_products.append(line.product_id)
        all_digimoov_modules=False
        for product in list_products:
            all_digimoov_modules = request.env['mcmacademy.module'].sudo().search(
                [('product_id', '=', product.product_tmpl_id.id),
                 ('company_id', '=', 2)])
        list_modules_digimoov = []
        today = date.today()
        if(all_digimoov_modules):
            for module in all_digimoov_modules:
                if module.date_exam:
                    if (module.date_exam - today).days > int(module.session_id.intervalle_jours) and module.session_id.website_published==True:
                        list_modules_digimoov.append(module)
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()
        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get('sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get('sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})
        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        })
        if order:
            order.order_line.filtered(lambda l: not l.product_id.active).unlink()
            _order = order
            if not request.env.context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()
        for module in list_modules_digimoov:
            print(module.ville)
            print(module.date_exam)
        values.update({
            'modules_digimoov':list_modules_digimoov,
            'error_ville':'',
            'error_exam_date':'',
            'error_condition':'',
        })
        if post.get('type') == 'popover':
            # force no-cache so IE11 doesn't cache this XHR
            return request.render("website_sale.cart_popover", values, headers={'Cache-Control': 'no-cache'})

        return request.render("website_sale.cart", values)

    def checkout_redirection(self, order):
        redirection=super(WebsiteSale,self).checkout_redirection(order)
        if order:
            if (order.company_id.id==2):
                check=False
                if not order.ville:
                    order.exam_center_error='error'
                    check=True
                else:
                    order.exam_center_error = ''
                if not order.module_id:
                    order.exam_date_error='error'
                    check = True
                else:
                    order.exam_date_error=''
                if not order.conditions:
                    order.conditions_error='error'
                    check = True
                if check:
                    return request.redirect('/shop/cart')

class Centre_Examen(http.Controller):
    @http.route(['/shop/cart/update_exam_center'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_exam_center(self, center):
        """This route is called when changing exam center from the cart."""
        order = request.website.sale_get_order()
        print("center")
        print(center)
        if center and center !='all':
            order.sudo().write({
                'ville':center,
                'module_id':False,
                'session_id':False,
            })
        else:
            order.sudo().write({
                'ville' :False
            })
        return order.ville

    @http.route(['/cpf/update_exam_center'], type='json', auth="public", methods=['POST'], website=True)
    def partner_update_exam_center(self, center):
        return True


class Date_Examen(http.Controller):
    @http.route(['/shop/cart/update_exam_date'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_exam_center(self, exam_date_id):
        order = request.website.sale_get_order()
        if exam_date_id and exam_date_id!='all':
            module=request.env['mcmacademy.module'].sudo().search([('id', '=', exam_date_id)], limit=1)
            if module and order:
                order.module_id=module
                order.session_id=module.session_id
        if exam_date_id and exam_date_id=='all':
            if order:
                order.module_id=False
                order.session_id=False

    @http.route(['/cpf/update_exam_date'], type='json', auth="public", methods=['POST'], website=True)
    def partner_update_exam_center(self, exam_date_id):
        partner = request.env.user.partner_id
        if exam_date_id and exam_date_id!='all':
            module=request.env['mcmacademy.module'].sudo().search([('id', '=', exam_date_id)], limit=1)
            if module and partner:
                partner.date_examen_edof=module.date_exam
        return True




