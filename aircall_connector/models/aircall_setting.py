from odoo import _
from odoo import models, fields, api
from odoo.osv import osv
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, AccessError
import requests
import base64
import json
import logging

_logger = logging.getLogger(__name__)


class ACSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ax_api_id = fields.Char(string=" Aircall API Id", required=False, )
    ax_api_token = fields.Char(string=" Aircall API Token", required=False)
    is_auto_create = fields.Boolean(string="Create contact in Aircall")
    is_auto_update = fields.Boolean(string="update contact in Aircall")
    is_aircall_setting = fields.Boolean(string="AirCall Configuration")
    is_comment = fields.Boolean(string="Add Comments to AirCall")
    is_tag = fields.Boolean(string="Add Tags to AirCall")
    # ac_user_id = fields.Char(string="AirCall User Id", required=False, )

    def set_values(self):

        res = super(ACSettings, self).set_values()
        self.test_connection()
        # self.env['ir.config_parameter'].get_param('aircall_connector.ax_api_id', self.ax_api_id)
        self.env['ir.config_parameter'].set_param('aircall_connector.ax_api_token', self.ax_api_token)
        self.env['ir.config_parameter'].set_param('aircall_connector.is_comment', self.is_comment)
        self.env['ir.config_parameter'].set_param('aircall_connector.is_tag', self.is_tag)
        self.env['ir.config_parameter'].set_param('aircall_connector.is_auto_create', self.is_auto_create)
        self.env['ir.config_parameter'].set_param('aircall_connector.is_auto_update', self.is_auto_update)
        self.env['ir.config_parameter'].set_param('aircall_connector.is_aircall_setting', self.is_aircall_setting)
        self.env['ir.config_parameter'].set_param('aircall_connector.ax_api_id', self.ax_api_id)
        return res

    @api.model
    def get_values(self):
        res = super(ACSettings, self).get_values()
        res.update(
            ax_api_id=self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id'),
            is_tag=self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_tag'),
            is_comment=self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_comment'),
            ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token'),
            is_auto_create = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_auto_create'),
            is_auto_update = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_auto_update'),
            is_aircall_setting = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_aircall_setting'),
        )
        return res

    def test_connection(self):
        try:
            if self.is_aircall_setting:
                if not self.ax_api_id or not self.ax_api_token:
                    raise osv.except_osv(_("Error!"), (_("Please add Api Id and Api Token")))

                auth = self.ax_api_id + ':' + self.ax_api_token
                encoded_auth = base64.b64encode(auth.encode()).decode()
                header = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic :{}'.format(encoded_auth)

                }
                response = requests.get(
                    'https://api.aircall.io/v1/ping',
                    headers=header).content

                response = json.loads(response)
                # if 'error' in response and json.response['error']:
                if 'ping' in response and response['ping'] == 'pong':
                    _logger.info(_("Success!"), (_("Credentials are Valid!")))
                    context = dict(self._context)
                    # self.env['office.usersettings'].login_url
                    context['message'] = 'Credentials are Valid!'
                    return self.message_wizard(context)

                else:
                    raise UserError(
                        'Invalid Credentials . Please! Check your AirCall credentials and try again!')
                    self.env.cr.commit()

        except Exception as e:
            raise ValidationError(_(str(e)))

            raise ValidationError('Connection Failed : Please check Username & API_Key !')
        # .format(str(e.args[0]['detail']))

    def message_wizard(self, context):

        return {
            'name': ('Success'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }
