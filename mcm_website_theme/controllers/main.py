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
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import OR
from collections import OrderedDict
from operator import itemgetter
from odoo.exceptions import ValidationError
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.osv import expression
from datetime import datetime, date

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


class Website(Home):

    @http.route(['''/''', '''/<string:partenaire>''', ]
        , type='http', auth="public", website=True)
    def index(self, state='', partenaire='', **kw, ):
        # homepage=super(Website, self).index()
        all_categs = request.env['product.public.category'].sudo().search([('parent_id', '=', False)])
        all_states = request.env['res.country.state'].sudo().search([('country_id.code', 'ilike', 'FR')],
                                                                    order='id asc')
        taxi_category = request.env['product.public.category'].sudo().search([('name', 'ilike', 'Formation TAXI')])
        vtc_category = request.env['product.public.category'].sudo().search([('name', 'ilike', 'Formation VTC')])
        vmdtr_category = request.env['product.public.category'].sudo().search([('name', 'ilike', 'Formation VMDTR')])

        digimoov_products = request.env['product.product'].sudo().search([('company_id', '=', 2)], order="list_price")
        basic_price = False
        avancee_price = False
        premium_price = False
        if digimoov_products:
            for product in digimoov_products:
                if (product.default_code == 'basic'):
                    basic_price = round(product.list_price)
                if (product.default_code == 'avancée'):
                    avancee_price = round(product.list_price)
                if (product.default_code == 'premium'):
                    premium_price = round(product.list_price)
        promo = False
        user_connected = request.env.user
        user_connected.partner_from = False
        if (request.website.id == 2 and partenaire in ['ubereats', 'deliveroo', 'coursierjob', 'box2home']):
            user_connected.partner_from = str(partenaire)
            promo = request.env['product.pricelist'].sudo().search(
                [('company_id', '=', 2), ('code', 'ilike', partenaire.upper())])
        if state:
            kw["search"] = state
        values = {
            'all_categories': all_categs,
            'state': state,
            'all_states': all_states,
            'taxi': taxi_category,
            'vtc': vtc_category,
            'vmdtr': vmdtr_category,
            'digimoov_products': digimoov_products,
            'basic_price': basic_price if basic_price else '',
            'avancee_price': avancee_price if avancee_price else '',
            'premium_price': premium_price if premium_price else '',
        }
        if (partenaire in ['', 'ubereats', 'deliveroo', 'coursierjob', 'box2home'] and request.website.id == 2):
            values['partenaire'] = partenaire
            if (promo):
                values['promo'] = promo
            else:
                values['promo'] = False
            return request.render("website.homepage", values)
        if (request.website.id == 1):
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
    ], type='http', auth="public", website=True, sitemap=False)
    def shop(self, page=0, category=None, state='', taxi_state='', vmdtr_state='', vtc_state='', search='', ppg=False,
             **post):
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
            tx = order.get_portal_last_transaction()
        else:
            tx = None

        if not order or (order.amount_total and not tx):
            return request.redirect('/shop')

        if order and not order.amount_total and not tx:
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx and tx.state == 'draft':
            return request.redirect('/shop')
        if tx and tx.state == 'done' and tx.amount > 0 and order.state != 'sale':
            order.sale_action_sent()
        PaymentProcessing.remove_payment_transaction(tx)
        if order.company_id.id == 1:
            return request.redirect("/shop/confirmation")
        else:
            product_id = False
            pricelist = False
            if order:
                for line in order.order_line:
                    product_id = line.product_id
            if tx:
                state = str(tx.state)
                if product_id:
                    slugname = (product_id.name).strip().strip('-').replace(' ', '-').lower()
                    if order.pricelist_id and order.pricelist_id.name in ['ubereats', 'deliveroo', 'coursierjob',
                                                                          'box2home']:
                        return request.redirect(
                            "/%s/%s/shop/confirmation/%s" % (slugname, order.pricelist_id.name, state))
                    else:
                        return request.redirect("/%s/shop/confirmation/%s" % (slugname, state))
                else:
                    return request.redirect("/shop/confirmation")
            else:
                return request.redirect("/shop/confirmation")

    @http.route(['''/<string:product>/<string:partenaire>/shop/address''', '''/<string:product>/shop/address''',
                 '''/shop/address'''], type='http', methods=['GET', 'POST'], auth="user", website=True, sitemap=False)
    def address(self, partenaire=None, product=None, **kw):
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
        partner = Partner.browse(partner_id)

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
            else:  # no mode - refresh without post?
                return request.redirect('/shop/checkout')

        # IF POSTED
        if 'submitted' in kw:
            partner.addresse_facturation = str(kw.get('adresse_facturation')) if kw.get('adresse_facturation') else ''
            partner.numero_permis = str(kw.get('numero_permis')) if kw.get('numero_permis') else ''
            partner.siret = str(kw.get('siret')) if kw.get('siret') else ''
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg)
            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw)
                if kw.get('adresse_facturation') and kw.get('adresse_facturation') == 'societe':
                    if not partner.parent_id:
                        company = Partner.sudo().create({
                            'name': kw.get('company_name'),
                            'siret': kw.get('siret'),
                            'company_type': 'company',
                            'phone': partner.phone,
                            'street': partner.street,
                        })
                        partner.parent_id = company.id
                if mode[1] == 'billing':
                    order.partner_id = partner_id
                    order.onchange_partner_id()
                    # This is the *only* thing that the front end user will see/edit anyway when choosing billing address
                    order.partner_invoice_id = partner_id
                    if not kw.get('use_same'):
                        kw['callback'] = kw.get('callback') or \
                                         (not order.only_services and (
                                                 mode[0] == 'edit' and '/shop/checkout' or '/shop/address'))
                elif mode[1] == 'shipping':
                    order.partner_shipping_id = partner_id

                order.message_partner_ids = [(4, partner_id), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/shop/confirm_order')

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(
            int(values['country_id']))
        country = country and country.exists() or def_country_id
        fr_country = request.env['res.country'].sudo().search(
            [('code', 'ilike', 'FR')], limit=1)
        if partner:
            values['addresse_facturation'] = order.partner_id.addresse_facturation
            values['siret'] = order.partner_id.siret
            values['name'] = order.partner_id.name
            values['phone'] = order.partner_id.phone
        render_values = {
            'website_sale_order': order,
            'partner_id': partner_id,
            'mode': mode,
            'checkout': values,
            'fact': order.partner_id.addresse_facturation,
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

    def checkout_form_validate(self, mode, all_form_values, data):
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]
        # Required fields from mandatory field function
        required_fields += mode[
                               1] == 'shipping' and self._get_mandatory_shipping_fields() or self._get_mandatory_billing_fields()
        # Check if state required
        country = request.env['res.country']
        if data.get('country_id'):
            country = country.browse(int(data.get('country_id')))
            if 'state_code' in country.get_address_fields() and country.state_ids:
                required_fields += ['state_id']

        # error message for empty required fields
        for field_name in required_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        if not data.get('numero_permis') and request.website.id == 1:
            error["numero_permis"] = 'error'
            error_message.append(_('Numéro de permis doit être rempli'))
        if not data.get('adresse_facturation'):
            error["adresse_facturation"] = 'error'
            error_message.append(_("l'Adresse de facturation doit être rempli"))
        if 'adresse_facturation' in data:
            if str(data['adresse_facturation']) == 'societe':
                if not data.get('company_name'):
                    error["company_name"] = 'error'
                    error_message.append(_('Nom de la société doit être rempli'))
                if not data.get('siret'):
                    error["siret"] = 'error'
                    error_message.append(_('Numéro Siret doit être rempli'))

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))
        # vat validation
        Partner = request.env['res.partner']
        # if data.get("vat") and hasattr(Partner, "check_vat"):
        #     if data.get("country_id"):
        #         data["vat"] = Partner.fix_eu_vat_number(data.get("country_id"), data.get("vat"))
        #     partner_dummy = Partner.new({
        #         'vat': data['vat'],
        #         'country_id': (int(data['country_id'])
        #                        if data.get('country_id') else False),
        #     })
        #     try:
        #         partner_dummy.check_vat()
        #     except ValidationError:
        #         error["vat"] = 'error'

        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message


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


class Payment3x(http.Controller):
    @http.route(['/shop/payment/update_amount'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_amount(self, instalment):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=1)
        payment = request.env['payment.acquirer'].sudo().search(
            [('name', 'ilike', 'stripe'), ('company_id', "=", request.website.company_id.id)])
        if instalment:
            if payment:
                order.instalment = True
                payment.instalment = True
                if (order.company_id.id == 2 and order.pricelist_id.name == 'ubereats'):
                    for line in order.order_line:
                        if line.product_id.default_code == 'access':
                            order.amount_total = 450
                            line.price_unit = 450
        else:
            payment.instalment = False
            order.instalment = False
            if (order.company_id.id == 2 and order.pricelist_id.name == 'ubereats'):
                for line in order.order_line:
                    if line.product_id.default_code == 'access':
                        order.amount_total = 380
                        line.price_unit = 380
        return True

    @http.route(['/shop/payment/update_cpf'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_cpf(self, cpf):
        order = request.website.sale_get_order(force_create=1)
        if cpf:
            order.partner_id.date_cpf = datetime.now()
            order.partner_id.mode_de_financement = 'cpf'
            order.partner_id.statut_cpf = 'untreated'
        return True


class Conditions(http.Controller):

    @http.route(['/shop/payment/update_condition'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_condition(self, condition):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=0)
        if order:
            if condition:
                order.conditions = True
            else:
                order.conditions = False
        return True

    @http.route(['/shop/payment/update_failures'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_failures(self, failures):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=0)
        if order:
            if failures:
                order.failures = True
            else:
                order.failures = False
        return True

    @http.route(['/shop/payment/update_accompagnement'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_accompagnement(self, accompagnement):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order(force_create=0)
        if order:
            if accompagnement:
                order.accompagnement = True
            else:
                order.accompagnement = False
        return True


class CustomerPortal(CustomerPortal):
    """
    @override function 'portal_my_tasks' to add domain
    'users_tasks_domain' to restrict users to display tasks
    assigned to them.
    """
    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                        search_in='content', groupby='project', **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'project': {'input': 'project', 'label': _('Project')},
        }

        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].search([])
        print(projects)
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group([('project_id', 'not in', projects.ids)],
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            if search_in in ('stage', 'all'):
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])
            domain += search_domain

        # Display tasks of active user
        users = request.env.user
        users_tasks_domain = ['|', ('parent_id.user_id', '=', users.id), ('user_id', '=', users.id)]
        # task count
        task_count = request.env['project.task'].search_count(users_tasks_domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            url_args={'date_begin': date_begin},
            total=task_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        if groupby == 'project_id':
            order = "project_id, %s" % order  # force sort on project first to group by project in view
        tasks = request.env['project.task'].search(users_tasks_domain, order=order, limit=self._items_per_page,
                                                   offset=(page - 1) * self._items_per_page)
        request.session['my_tasks_history'] = tasks.ids[:100]
        if groupby == 'project':
            grouped_tasks = [request.env['project.task'].concat(*g) for k, g in
                             groupbyelem(tasks, itemgetter('project_id'))]
        else:
            grouped_tasks = [tasks]
        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'task',
            'archive_groups': archive_groups,
            'default_url': '/my/tasks',
            'pager': pager,
            'searchbar_sortings': [],
            'searchbar_groupby': [],
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'sortby': False,
            'groupby': False,
            'searchbar_filters': False,
            'filterby': False,
        })
        return request.render("project.portal_my_tasks", values)

    # @override Function to Add Filter to invoice_count in portal invoice view
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        invoice_count = request.env['account.move'].search_count([
            ('type', 'in', ('out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt', 'in_receipt')),
            ('type_facture', '=', 'web')
        ])
        values['invoice_count'] = invoice_count
        #add users_tasks_domain to filter tasks in portal view
        users = request.env.user
        users_tasks_domain = ['|', ('parent_id.user_id', '=', users.id), ('user_id', '=', users.id)]
        values['task_count'] = request.env['project.task'].search_count(users_tasks_domain)
        return values

    # @override Second Function to Add Filter to invoice_count in portal invoice view
    def _prepare_home_portal_values(self):
        values = super(CustomerPortal, self)._prepare_home_portal_values()
        invoice_count = request.env['account.move'].search_count([
            ('type', 'in', ('out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt', 'in_receipt')),
            ('type_facture', '=', 'web')
        ]) if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0
        values['invoice_count'] = invoice_count
        # add users_tasks_domain to filter tasks in portal view
        users = request.env.user
        users_tasks_domain = ['|', ('parent_id.user_id', '=', users.id), ('user_id', '=', users.id)]
        values['task_count'] = request.env['project.task'].search_count(users_tasks_domain)
        return values

    """@override this function to add filter can display 
    all invoices Not CPF type linked to specific portal"""
    @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        AccountInvoice = request.env['account.move']

        domain = [
            ('type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')),
            ('type_facture', '=', 'web')]

        searchbar_sortings = {
            'date': {'label': _('Invoice Date'), 'order': 'invoice_date desc'},
            'duedate': {'label': _('Due Date'), 'order': 'invoice_date_due desc'},
            'name': {'label': _('Reference'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('account.move', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        invoice_count = AccountInvoice.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/invoices",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=invoice_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected

        """ Add filter to client view to display all invoices 
        contains type WEB also the cpf_solde_invoice, cpf_acompte_invoice
        should be not ckecked using lambda """

        invoices = AccountInvoice.search(domain, order=order, limit=self._items_per_page, offset=pager['offset']).filtered(lambda facture: facture.type_facture == 'web')
        request.session['my_invoices_history'] = invoices.ids[:100]
        values.update({
            'date': date_begin,
            'invoices': invoices,
            'page_name': 'invoice',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/invoices',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("account.portal_my_invoices", values)
