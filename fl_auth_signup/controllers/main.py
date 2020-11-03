# -*- coding: utf-8 -*-

import logging
import werkzeug
from odoo import http, _
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class AuthSignupHome(AuthSignupHome):
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password', 'phone')}
        if not values:
            raise UserError(_("Le formulaire n'est pas correctement rempli."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Les mots de passe ne correspondent pas, veuillez les saisir à nouveau."))
        if '+33' not in values['phone']:
            phone=values['phone']
            phone=phone[1:]
            phone='+33'+str(phone)
            values['phone']=phone
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        values['lang'] = 'fr_FR'
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        # qcontext['states'] = request.env['res.country.state'].sudo().search([])
        # qcontext['countries'] = request.env['res.country'].sudo().search([])

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Un autre utilisateur est déjà enregistré avec cette adresse courriel.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Vous ne pouvez pas créer un nouveau compte.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
