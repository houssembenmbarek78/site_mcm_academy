from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, AccessError
from odoo.osv import osv
from odoo import _
import json
import base64
import time
from datetime import datetime
import requests


class AirCall(models.Model):
    _name = 'call.detail'
    _rec_name = 'call_contact'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Call/Details'

    call_id = fields.Char(string="Air Call Id", required=False, )
    call_direction = fields.Char(string="AirCall Direction", required=False, )
    call_status = fields.Char(string="Status", required=False, )
    call_recording = fields.Char(string="Recording_url", required=False, )
    call_contact = fields.Many2one(comodel_name="res.partner", string="Contact", required=False, )
    user_id = fields.Many2one(comodel_name="res.users", string="Task Assigned To",
                              required=False, )
    phone_number = fields.Char(string="Phone Number", required=False, )
    user_name = fields.Char(string="User Name", required=False)
    company_name = fields.Char(string="Company Name", required=False)
    digits = fields.Char(string="Company Number", required=False)
    call_date = fields.Datetime(string="Call Date", required=False, )
    is_imp_tag = fields.Boolean(string="is aircall tag")
    air_call_tag = fields.Many2many(comodel_name="res.partner.category", relation="call_tags_relation", column1="call_tag_id", column2="call_id", string="Tags", )
    notes = fields.Text(strng="Notes", required=False)

    def write(self,values):
        res = super(AirCall, self).write(values)
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        is_tag = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_tag')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')

        if is_tag and 'is_imp_tag' in values and not values['is_imp_tag']:
            tag_ids = []
            auth = ax_api_id + ':' + ax_api_token
            encoded_auth = base64.b64encode(auth.encode()).decode()
            header = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic :{}'.format(encoded_auth)
            }
            for tag in values['air_call_tag'][0][2]:

                odoo_tag = self.env['res.partner.category'].search([('id', '=', tag)])
                if not odoo_tag.call_tag_id:
                    data = {
                        "name": odoo_tag.name,
                        "color": odoo_tag.color if odoo_tag.color else "#00B388"
                    }

                    response = requests.post(
                        'https://api.aircall.io/v1/tags'.format(self.call_id),
                        data=json.dumps(data),
                        headers=header)

                    if response.status_code == 400:
                        raise ValidationError(json.loads(response.content)['troubleshoot'])

                    response = json.loads(response.content)
                    if response:
                        print(response)
                        odoo_tag.call_tag_id = response['tag']['id']
                        # self.env.cr.commit()

                tag_ids.append(odoo_tag.call_tag_id)

            if not self.user_id.ac_user_id:
                phone_num = []
                data = {
                    'tags': tag_ids
                        }

                response = requests.post(
                    'https://api.aircall.io/v1/calls/{}/tags'.format(self.call_id),
                    data=json.dumps(data),
                    headers=header)

                if response.status_code == 400:
                    raise ValidationError(json.loads(response.content)[
                                              'troubleshoot'])

                if response.status_code == 201:
                    pass

        return res








