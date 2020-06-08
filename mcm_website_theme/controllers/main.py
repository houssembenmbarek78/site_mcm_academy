from odoo import http
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

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class Website(Home):

    @http.route('/'
        , type='http', auth="public", website=True)
    def index(self, state='', **kw, ):
        homepage = request.website.homepage_id
        all_categs = request.env['product.public.category'].sudo().search([('parent_id', '=', False)])
        all_states = request.env['res.country.state'].sudo().search([('country_id.code', 'ilike', 'FR')])
        taxi_category = request.env['product.public.category'].sudo().search([('name', 'ilike', 'Formation TAXI')])
        vtc_category = request.env['product.public.category'].sudo().search([('name', 'ilike', 'Formation VTC')])
        vmdtr_category = request.env['product.public.category'].sudo().search([('name', 'ilike', 'Formation VMDTR')])
        if state:
            kw["search"] = state
        values = {
            'all_categories': all_categs,
            'state': state,
            'all_states': all_states,
            'taxi': taxi_category,
            'vtc': vtc_category,
            'vmdtr': vmdtr_category
        }
        return request.render("website.homepage", values)
        if homepage and (
                homepage.sudo().is_visible or request.env.user.has_group('base.group_user')) and homepage.url != '/':
            return request.env['ir.http'].reroute(homepage.url)

        website_page = request.env['ir.http']._serve_page()
        if website_page:
            return website_page
        else:
            top_menu = request.website.menu_id
            first_menu = top_menu and top_menu.child_id and top_menu.child_id.filtered(lambda menu: menu.is_visible)
            if first_menu and first_menu[0].url not in ('/', '', '#') and (
                    not (first_menu[0].url.startswith(('/?', '/#', ' ')))):
                return request.redirect(first_menu[0].url)

        raise request.not_found()
        values = {'all_categories': all_categs, }
        return request.render("website.homepage", values)

        # --------------------------------------------------------------------------
        # states Search Bar
        # --------------------------------------------------------------------------

    @http.route('/states/autocomplete', type='json', auth='public', website=True)
    def states_autocomplete(self, term, options={}, **kwargs):
        states = request.env['res.country.state'].sudo().search(
            ['&', ('name', 'ilike', term), ('country_id.code', 'ilike', 'FR')])
        fields = ['id', 'name']
        res = {
            'states': states.read(fields),
        }
        return res


class WebsiteSale(WebsiteSale):

    def sitemap_shop(env, rule, qs):
        if not qs or qs.lower() in '/shop':
            yield {'loc': '/shop'}

        Category = env['product.public.category']
        dom = sitemap_qs2dom(qs, '/shop/category', Category._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for cat in Category.sudo().search(dom):
            loc = '/shop/category/%s' % slug(cat)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=sitemap_shop)
    def shop(self, page=0, category=None, state='', taxi_state='', vmdtr_state='',vtc_state='', search='', ppg=False, **post):
        add_qty = int(post.get('add_qty', 1))
        Category = request.env['product.public.category']
        if category and category != 'all':
            category = Category.sudo().search([('id', '=', int(category))], limit=1)
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = Category
        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        attrib_set = {v[1] for v in attrib_values}

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list,
                        order=post.get('order'))

        pricelist_context, pricelist = self._get_pricelist_context()

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        Product = request.env['product.template'].with_context(bin_size=True)

        search_product = Product.sudo().search(domain)
        website_domain = request.website.website_domain()
        categs_domain = [('parent_id', '=', False)] + website_domain
        if search:
            search_categories = Category.sudo().search(
                [('product_tmpl_ids', 'in', search_product.ids)] + website_domain).parents_and_self
            categs_domain.append(('id', 'in', search_categories.ids))
        else:
            search_categories = Category
        categs = Category.sudo().search(categs_domain)

        if category:
            url = "/shop/category/%s" % slug(category)

        product_count = len(search_product)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.sudo().search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
        final_products = []
        if state and state != 'all' and category != 'all':
            states = request.env['res.country.state'].sudo().search(
                ['&', ('name', 'ilike', state), ('country_id.code', 'ilike', 'FR')])
            for product in products:
                if states:
                    for state in states:
                        sql_query = ''' select * from product_template_state_rel where product_template_id=%s and state_id=%s '''
                        request.cr.execute(sql_query, (product.id, state.id))
                        result = request.cr.fetchall()
                        if result:
                            final_products.append(product)
            products = final_products

        # get products where category is taxi and search using state
        if taxi_state and taxi_state != '':
            states = request.env['res.country.state'].sudo().search(
                ['&', ('name', 'ilike', taxi_state), ('country_id.code', 'ilike', 'FR')])
            category = request.env['product.public.category'].sudo().search(
                [('code', 'ilike', 'taxi')], limit=1)
            domain = self._get_search_domain(search, category.id, attrib_values)
            products = Product.sudo().search(domain, limit=ppg, offset=pager['offset'],
                                             order=self._get_search_order(post))
            for product in products:
                if states:
                    for state in states:
                        sql_query = ''' select * from product_template_state_rel where product_template_id=%s and state_id=%s '''
                        request.cr.execute(sql_query, (product.id, state.id))
                        result = request.cr.fetchall()
                        if result:
                            final_products.append(product)
            products = final_products

        # get products where category is vmdtr and search using state
        if vmdtr_state and vmdtr_state != '':
            states = request.env['res.country.state'].sudo().search(
                ['&', ('name', 'ilike', vmdtr_state), ('country_id.code', 'ilike', 'FR')])
            category = request.env['product.public.category'].sudo().search(
                [('code', 'ilike', 'vmdtr')], limit=1)
            domain = self._get_search_domain(search, category.id, attrib_values)
            products = Product.sudo().search(domain, limit=ppg, offset=pager['offset'],
                                             order=self._get_search_order(post))
            for product in products:
                if states:
                    for state in states:
                        sql_query = ''' select * from product_template_state_rel where product_template_id=%s and state_id=%s '''
                        request.cr.execute(sql_query, (product.id, state.id))
                        result = request.cr.fetchall()
                        if result:
                            final_products.append(product)
            products = final_products

        # get products where category is vtc and search using state
        if vtc_state and vtc_state != '':
            states = request.env['res.country.state'].sudo().search(
                ['&', ('name', 'ilike', vtc_state), ('country_id.code', 'ilike', 'FR')])
            category = request.env['product.public.category'].sudo().search(
                [('code', 'ilike', 'vtc')], limit=1)
            domain = self._get_search_domain(search, category.id, attrib_values)
            products = Product.sudo().search(domain, limit=ppg, offset=pager['offset'],
                                             order=self._get_search_order(post))
            for product in products:
                if states:
                    for state in states:
                        sql_query = ''' select * from product_template_state_rel where product_template_id=%s and state_id=%s '''
                        request.cr.execute(sql_query, (product.id, state.id))
                        result = request.cr.fetchall()
                        if result:
                            final_products.append(product)
            products = final_products

        # get products where category is vtc

        if state and state != 'all' and category == 'all':
            states = request.env['res.country.state'].sudo().search(
                ['&', ('name', 'ilike', state), ('country_id.code', 'ilike', 'FR')])

            for product in products:
                if states:
                    for state in states:
                        sql_query = ''' select * from product_template_state_rel where state_id=%s '''
                        request.cr.execute(sql_query, (state.id))
                        result = request.cr.fetchall()
                        if result:
                            final_products.append(product)
            products = final_products

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            attributes = ProductAttribute.sudo().search([('product_tmpl_ids', 'in', search_product.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        layout_mode = request.session.get('website_sale_shop_layout_mode')
        if not layout_mode:
            if request.website.viewref('website_sale.products_list_view').active:
                layout_mode = 'list'
            else:
                layout_mode = 'grid'

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'add_qty': add_qty,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg, ppr),
            'ppg': ppg,
            'ppr': ppr,
            'categories': categs,
            'attributes': attributes,
            'keep': keep,
            'search_categories_ids': search_categories.ids,
            'layout_mode': layout_mode,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)


    @http.route(['/shop/payment/update_amount'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_amount(self, instalment):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=1)

        print('order')
        print(order)
        payment = request.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
        if instalment:
            if payment:
                order.instalment=True
                payment.instalment = True
        else:
            payment.instalment = False
            order.instalment = False
        return True

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        """ Method that should be called by the server when receiving an update
        for a transaction. State at this point :

         - UDPATE ME
        """
        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if transaction_id:
            tx = request.env['payment.transaction'].sudo().browse(transaction_id)
            assert tx in order.transaction_ids()
        elif order:
            order.sale_action_sent()
            tx = order.get_portal_last_transaction()
        else:
            tx = None

        if not order or (order.amount_total and not tx):
            return request.redirect('/shop')

        if order and not order.amount_total and not tx:
            order.sale_action_sent()
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx and tx.state == 'draft':
            return request.redirect('/shop')

        PaymentProcessing.remove_payment_transaction(tx)
        order.sale_action_sent()
        return request.redirect('/shop/confirmation')

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        mode = (False, False)
        can_edit_vat = False
        def_country_id = order.partner_id.country_id
        values, errors = {}, {}

        partner_id = int(kw.get('partner_id', -1))

        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            mode = ('new', 'billing')
            can_edit_vat = True
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                def_country_id = request.env['res.country'].search([('code', '=', country_code)], limit=1)
            else:
                def_country_id = request.website.user_id.sudo().country_id
        # IF ORDER LINKED TO A PARTNER
        else:
            if partner_id > 0:
                if partner_id == order.partner_id.id:
                    mode = ('edit', 'billing')
                    can_edit_vat = order.partner_id.can_edit_vat()
                else:
                    shippings = Partner.search([('id', 'child_of', order.partner_id.commercial_partner_id.ids)])
                    if partner_id in shippings.mapped('id'):
                        mode = ('edit', 'shipping')
                    else:
                        return Forbidden()
                if mode:
                    values = Partner.browse(partner_id)
            elif partner_id == -1:
                mode = ('new', 'shipping')
            else: # no mode - refresh without post?
                return request.redirect('/shop/checkout')

        # IF POSTED
        if 'submitted' in kw:
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)

            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)
                if mode[1] == 'billing':
                    order.partner_id = partner_id
                    order.onchange_partner_id()
                    # This is the *only* thing that the front end user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get('use_same'):
                        kw['callback'] = kw.get('callback') or \
                            (not order.only_services and (mode[0] == 'edit' and '/shop/checkout' or '/shop/address'))
                elif mode[1] == 'shipping':
                    order.partner_shipping_id = partner_id

                order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/shop/confirm_order')

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
        country = country and country.exists() or def_country_id
        fr_country = request.env['res.country'].sudo().search(
            [('code', 'ilike', 'FR')], limit=1)
        render_values = {
            'website_sale_order': order,
            'partner_id': partner_id,
            'mode': mode,
            'checkout': values,
            'can_edit_vat': can_edit_vat,
            'country': country,
            'fr_country': fr_country,
            'countries': country.get_website_sale_countries(mode=mode[1]),
            "states": country.get_website_sale_states(mode=mode[1]),
            'error': errors,
            'callback': kw.get('callback'),
            'only_services': order and order.only_services,
        }
        return request.render("website_sale.address", render_values)


class Taxi(http.Controller):

    @http.route('/taxi', type='http', auth='public', website=True)
    def taxi(self, taxi_state='', **kw, ):
        return request.render("mcm_website_theme.mcm_website_theme_taxi", {})


class VMDTR(http.Controller):

    @http.route('/vmdtr', type='http', auth='public', website=True)
    def taxi(self, vmdtr_state='', **kw, ):
        return request.render("mcm_website_theme.mcm_website_theme_vmdtr", {})


class VTC(http.Controller):

    @http.route('/vtc', type='http', auth='public', website=True)
    def taxi(self, vtc_state='', **kw, ):
        return request.render("mcm_website_theme.mcm_website_theme_vtc", {})
