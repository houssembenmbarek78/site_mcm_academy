# -*- coding: utf-8 -*-

import logging
import werkzeug
import odoo
from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from odoo.addons.web.controllers import main

_logger = logging.getLogger(__name__)


class AuthSignupHome(AuthSignupHome):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'firstname', 'password', 'phone')}
        values['login'] = values['login'].replace(' ', '').lower()
        if not values:
            raise UserError(_("Le formulaire n'est pas correctement rempli."))
        if '+33' not in values['phone']:
            phone = values['phone']
            phone = phone[1:]
            phone = '+33' + str(phone)
            values['phone'] = phone
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Les mots de passe ne correspondent pas, veuillez les saisir à nouveau."))
        values['name'] = values['firstname'] + ' ' + values['name']
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        values['lang'] = 'fr_FR'
        if request.website.id == 2:
            values['company_ids'] = [1, 2]
            values['company_id'] = 2
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        # qcontext['states'] = request.env['res.country.state'].sudo().search([])
        # qcontext['countries'] = request.env['res.country'].sudo().search([])
        qcontext['login'] = str(qcontext.get('login')).replace(' ', '').lower()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                qcontext['login'] = qcontext['login'].replace(' ', '').lower()
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):

                    user_sudo = request.env['res.users'].sudo().search(
                        [('login', "=", qcontext.get('login').replace(' ', '').lower())])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                    user_sudo = request.env['res.users'].sudo().search(
                        [('login', "=", qcontext.get('login').replace(' ', '').lower())])
                    if user_sudo:
                        user_sudo.street = str(request.website.name)
                kw['login'] = qcontext.get('login').replace(' ', '').lower()
                print('kw: ', kw)
                print('args: ', args)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search(
                        [("login", "=", qcontext.get("login").replace(' ', '').lower())]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class Home(Home):

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        if 'login' in request.params:
            request.params['login'] = request.params['login'].replace(' ','').lower()
        response=super(Home, self).web_login(redirect=redirect,**kw)
        return response
