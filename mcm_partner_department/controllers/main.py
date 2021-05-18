# -*- coding: utf-8 -*-
from odoo import http,_
import json
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import QueryURL
from odoo.addons.portal.controllers.web import Home
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.osv import expression
from odoo.exceptions import ValidationError,Warning,UserError,RedirectWarning

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['GET', 'POST'], website=True, csrf=False)
    def cart_update(self, product_id, module='', departement='', add_qty=1, set_qty=0, promo=None, **kw):
        """This route is called when adding a product to cart (no options)."""
        error_message = ''
        sale_order = request.website.sale_get_order(force_create=True)
        if sale_order.order_line:
            list = []
            sale_order.write({'order_line': [(6, 0, list)]})
        if sale_order.state != 'draft':
            request.session['sale_order_id'] = None
            sale_order = request.website.sale_get_order(force_create=True)
        product_custom_attribute_values = None
        if kw.get('product_custom_attribute_values'):
            product_custom_attribute_values = json.loads(kw.get('product_custom_attribute_values'))

        no_variant_attribute_values = None
        if kw.get('no_variant_attribute_values'):
            no_variant_attribute_values = json.loads(kw.get('no_variant_attribute_values'))
        if promo:
            print(promo)
        sale_order._cart_update(
            product_id=int(product_id),
            add_qty=1,
            set_qty=1,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values
        )
        if promo:
            pricelist = request.env['product.pricelist'].sudo().search(
                [('company_id', '=', 2), ('id', "=", promo)])
            if pricelist:
                request.website.sale_get_order(code=pricelist.code)
        else:
            request.website.sale_get_order(code='')
        if (sale_order.partner_id.customer_rank == 0):
            sale_order.partner_id.customer_rank = 1
        if product_id:
            if module == 'all':
                product = request.env['product.template'].sudo().search(
                    [('id', '=', product_id)])
                error_session = "error"
                url = "/shop/product/" + str(slug(product))
                values = self._prepare_product_values(product, category='', search='', **kw)
                values['error_session'] = "error"
                return request.render("website_sale.product", values)

            if module != '' and module != 'all':
                module = request.env['mcmacademy.module'].sudo().search(
                    [('id', '=', module)])
                session = module.session_id
                if session:
                    sale_order.session_id = session
                    sale_order.partner_id.mcm_session_id = session
                if module:
                    sale_order.module_id = module
                    sale_order.partner_id.module_id = module
                list = []
                check_portal = False
                if sale_order.partner_id.user_ids:
                    for user in sale_order.partner_id.user_ids:
                        groups = user.groups_id
                        for group in groups:
                            if (group.name == _('Portail')):
                                check_portal = True
                if check_portal:
                    for partner in session.panier_perdu_ids:
                        list.append(partner.id)
                    list.append(sale_order.partner_id.id)
                    session.write({'panier_perdu_ids': [(6, 0, list)]})
                    sale_order.partner_id.statut = 'panier_perdu'
                    sale_order.partner_id.module_id = module
                    sale_order.partner_id.mcm_session_id = session
        if product_id:
            if departement != 'all':
                state = request.env['res.country.state'].sudo().search(
                    ['&', ('code', "=", str(departement)), ('country_id.code', 'ilike', 'FR')])
                if state:
                    sale_order.partner_id.state_id = state
                if departement == '59':
                    sale_order.partner_id.partner_departement = '59000'
                if departement == '62':
                    sale_order.partner_id.partner_departement = '62000'
            else:
                print('test false')
                product = request.env['product.template'].sudo().search(
                    [('id', '=', product_id)])
                error_message = "error"
                url = "/shop/product/" + str(slug(product))
                values = self._prepare_product_values(product, category='', search='', **kw)
                values['error_department'] = "error"
                return request.render("website_sale.product", values)

        if kw.get('express'):
            return request.redirect("/shop/checkout?express=1")
        if product_id:
            product = request.env['product.template'].sudo().search(
                [('id', '=', product_id)],limit=1)
            slugname=(product.name).strip().strip('-').replace(' ','-').lower()
            if not promo and product and product.company_id.id==2:
                return request.redirect("/%s/shop/cart" % (slugname))
            elif promo and product and product.company_id.id==2:
                pricelist = request.env['product.pricelist'].sudo().search(
                    [('company_id', '=', 2), ('id',"=",promo)])
                if pricelist:
                    if pricelist.name in ['ubereats','deliveroo','coursierjob','box2home']:
                        return request.redirect("/%s/%s/shop/cart" % (slugname,pricelist.name))
        return request.redirect("/shop/cart")
