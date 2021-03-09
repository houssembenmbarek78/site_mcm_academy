# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, AccessError
from odoo.osv import osv
from odoo import _
import json
import requests
import logging
import datetime
from ..tools import phone_validation
import base64
import time
from datetime import datetime

_logger = logging.getLogger(__name__)


class ResUser(models.Model):
    _inherit = "res.users"

    ax_api_id = fields.Char(string=" Aircall API Id", required=False, )
    ax_api_token = fields.Char(string=" Aircall API Token", required=False, )
    is_auto_create = fields.Boolean(string="Create contact in Aircall,when create in Odoo",  )
    is_auto_update = fields.Boolean(string="update contact in Aircall,when update in Odoo",  )
    ac_user_id = fields.Char(string="AirCall User Id", required=False, )

    def test_connection(self):
        try:
            if not self.ax_api_id or not self.ax_api_token:
                raise osv.except_osv(_("Error!"), (_("Please add Api Id and Api Token")))

            auth = self.ax_api_id + ':' +self.ax_api_token
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
            if 'ping' in response and response['ping']=='pong':
                raise osv.except_osv(_("Success!"), (_("Credentials are Valid!")))
                _logger.info(_("Success!"), (_("Credential are Valid!")))

            else:
                raise UserError(
                    'Invalid Credentials . Please! Check your credential and try again!')
                self.env.cr.commit()

        except Exception as e:
            raise ValidationError(_(str(e)))

    def import_contacts(self):
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')
        if not ax_api_id or not ax_api_token:
            raise osv.except_osv    (_("Error!"), (_("Please add Api Id and Api Token from Aircall setting")))

        auth = ax_api_id + ':' + ax_api_token
        encoded_auth = base64.b64encode(auth.encode()).decode()
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic :{}'.format(encoded_auth)

        }
        response = requests.get(
            'https://api.aircall.io/v1/contacts?order=desc&per_page=50',
            headers=header).content

        response = json.loads(response)

        if response:
            if 'contacts' in response and response['contacts']:

                # call_response = json.loads(requests.get(
                #     'https://api.aircall.io/v1/contacts?order=desc&per_page=50',
                #     headers=header).content)

                # ---------------------- Newly added by Hussam ----------------------#
                new_call_response = requests.get(
                    'https://api.aircall.io/v1/calls?order=desc&per_page=50',
                    headers=header
                )

                if new_call_response.status_code == 400 or new_call_response.status_code == 404:
                    raise ValidationError('Error')

                calls = json.loads(new_call_response.content)

                # Also passing "calls" parameter to "create_contact()" function.
                # --------------------------------------------------------------------- #
                if 'calls' in calls:
                    calls_list=calls['calls']
                for contact in response['contacts']:
                    print(contact)
                    odoo_contacts = self.create_contact(contact, calls)

    def get_tags_and_notes(self, calls, contact):

        tags = set()
        notes = ""

        for call in calls['calls']:

            if call['contact'] is not None:
                fn_call = str(call['contact']['first_name'])
                fn_contact = str(contact['first_name'])
                ln_call = str(call['contact']['last_name'])
                ln_contact = str(contact['last_name'])

                if fn_call == fn_contact and ln_call == ln_contact:
                    for tag in call['tags']:
                        odoo_tag = self.env['res.partner.category'].search([('call_tag_id', '=', tag['id'])])
                        tags.add(odoo_tag.id)
                    for comment in call['comments']:
                        notes += comment['content'] + "\n"
        return list(tags), notes


    def create_contact(self, contact, calls):

        res_user= self.env['res.users']

        odoo_contact = res_user.search([('air_contact_id', '=', contact['id'])])

        tags, notes = self.get_tags_and_notes(calls, contact)

        if odoo_contact:
            odoo_contact.partner_id.write({'name': str(contact['first_name']) + ' ' + str(contact['last_name']),
                                            'air_contact_id': contact['id'],
                                            'email': contact['emails'][0]['value'] if contact['emails'] else None,
                                            'phone': contact['phone_numbers'][0]['value'] if contact['phone_numbers'] else None,
                                # 'category_id': tags,
                                })

        elif 'emails' in contact and contact['emails'] and contact['emails'][0]['value']:
            email = contact['emails'][0]['value']
            odoo_contact = res_user.search([('login', '=', email)])
            if not odoo_contact:
                odoo_contact = self.env['res.users'].sudo().create({
                    'name': str(contact['first_name']) + ' ' + str(contact['last_name']),
                    'login': str(email),
                    'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
                    'email': False,
                    'notification_type': 'email',

                })
                if odoo_contact:
                    odoo_contact.partner_id.phone=contact['phone_numbers'][0]['value'] if contact[
                                                 'phone_numbers'] else None
                    odoo_contact.partner_id.email=contact['emails'][0]['value']

            else:
                odoo_contact.partner_id.write({'name': str(contact['first_name']) + ' ' + str(contact['last_name']),
                                     'air_contact_id': contact['id'],
                                     'email': contact['emails'][0]['value'] if contact['emails'] else None,
                                     'phone': contact['phone_numbers'][0]['value'] if contact[
                                                 'phone_numbers'] else None,
                                     })
        if odoo_contact:
            return odoo_contact.partner_id
        else:
            return False

    def import_calls(self):
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')
        if not ax_api_id or not ax_api_token:
            raise osv.except_osv(_("Error!"), (_("Please add Api Id and Api Token from Aircall setting")))

        auth = ax_api_id + ':' + ax_api_token
        encoded_auth = base64.b64encode(auth.encode()).decode()
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic :{}'.format(encoded_auth)
        }
        call_response = requests.get(
                    'https://api.aircall.io/v1/calls?order=desc&per_page=50',
                    headers=header,
        )

        if call_response.status_code == 400 or call_response.status_code == 404:
            raise ValidationError('Error')
        else:
            calls = json.loads(call_response.content)
            self.call_details(calls)

    def call_details(self, call_response):
        """This function get all call details from Aircall """
        # if call_response['calls']:
            # call_detail = list(filter(lambda d: d['contact'] and d['contact']['id'] == contact['id'], call_response['calls']))

        # if calls exist
        if call_response['calls']:

            for call in call_response['calls']:
                call_rec = self.env['call.detail'].search([('call_id', '=', call['id'])])
                odoo_contact = None
                if (call['number']['name']=='MCM ACADEMY'):
                    print('call '+str(call))
                # Creating a non existant contact
                    if call['contact']:
                        odoo_contact = self.create_contact(call['contact'], call_response)
                    started_at = call['started_at']
                    if started_at:
                        started_at = str(datetime.fromtimestamp(started_at))
                    ended_at = call['ended_at']
                    if ended_at:
                        ended_at = str(datetime.fromtimestamp(ended_at))
                    user_name=''
                    if call['user']:
                        user_name=str(call['user']['name'])
                    else:
                        user_name=''
                    if not call_rec:
                        comments = ''
                        comment = False
                        for note in call['comments']:
                            comments += note['content']
                            comment=str(note['content'])
                            if odoo_contact:
                                subtype_id = self.env.ref('mail.mt_note')
                                print(odoo_contact)
                                entrant_sortant=''
                                if(call['direction']) and call['direction']=='inbound':
                                    entrant_sortant='Appel Entrant'
                                if(call['direction']) and call['direction']=='outbound':
                                    entrant_sortant = 'Appel Sortant'
                                content="<p><b>"+user_name+' '+entrant_sortant+' '+" "+started_at+" "+ended_at+"</b></p>",
                                message=False
                                if odoo_contact and subtype_id:
                                    message = self.env['mail.message'].sudo().search([('subtype_id',"=",subtype_id.id),('model',"=",'res.partner'),('res_id','=',odoo_contact.id),('body','like',comment)])
                                if not message and odoo_contact:
                                    message = self.env['mail.message'].sudo().create({
                                        'subject': user_name+" "+started_at+" "+ended_at,
                                        'model': 'res.partner',
                                        'res_id': odoo_contact.id,
                                        'message_type': 'notification',
                                        'subtype_id': subtype_id.id,
                                        'body': str(content)+str(note['content']),
                                    })
                        date = datetime.fromtimestamp(call['started_at'])
                        call_rec.create({'call_id': call['id'],
                                         'call_status': call['status'],
                                         'call_direction': call['direction'],
                                         'call_date': date,
                                         'phone_number': call['raw_digits'],
                                         'call_contact': odoo_contact.id if odoo_contact else None,
                                         'call_recording': call['asset'],
                                         'digits': call['number']['digits'],
                                         'company_name': call['number']['name'],
                                         'notes': comments
                                         })
                    else:
                        comments = ''
                        comment = False
                        for note in call['comments']:
                            comments += note['content']
                            comment = str(note['content'])
                            subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mt_note')
                            if odoo_contact and subtype_id:
                                print(odoo_contact)
                                message = self.env['mail.message'].sudo().search(
                                    [('subtype_id', "=", subtype_id.id), ('model', "=", 'res.partner'),
                                     ('res_id', '=', odoo_contact.id), ('body', 'like', comment)])
                                if not message:
                                    message = self.env['mail.message'].sudo().create({
                                        'subject': user_name + " " + started_at + " " + ended_at,
                                        'model': 'res.partner',
                                        'res_id': odoo_contact.id,
                                        'message_type': 'notification',
                                        'subtype_id': subtype_id,
                                        'body': str(note['content']),
                                    })
                    if not call_rec.call_contact and odoo_contact:
                        call_rec.write({'call_contact': odoo_contact.id if odoo_contact else None,
                                        })

                    if call['tags']:
                        tags = []
                        for tag in call['tags']:
                            odoo_tag = self.env['res.partner.category'].search(
                                ['|', ('call_tag_id', '=', tag['id']), ('call_tag_id', '=', tag['name'])])
                            if not odoo_tag:
                                odoo_tag = odoo_tag.create({
                                    'call_tag_id': tag['id'],
                                    'name': tag['name'],
                                })

                            call_rec.write({'air_call_tag': [(4, odoo_tag.id)],
                                            'is_imp_tag': True})

class ResUser(models.Model):
    _inherit = 'res.users'

    air_contact_id = fields.Char('AirCall Contact Id')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    air_contact_id = fields.Char('AirCall Contact Id')
    call_count = fields.Integer(compute='_compute_call_count', string='call Count')

    def _compute_call_count(self):
        # retrieve all children partners and prefetch 'parent_id' on them
        self.call_count = 0

    def _phone_get_country(self):
        if 'country_id' in self and self.country_id:
            return self.country_id
        return self.env.company.country_id

    def phone_format(self, number, country=None, company=None):
        country = country or self._phone_get_country()
        if not country:
            return number
        return phone_validation.phone_format(
            number,
            country.code if country else None,
            country.phone_code if country else None,
            force_format='INTERNATIONAL',
            raise_exception=True
        )

    @api.onchange('phone','mobile', 'country_id', 'company_id')
    def _onchange_phone_validation(self):
        if self.phone:
            self.phone = self.phone_format(self.phone)
        if self.mobile:
            self.mobile = self.phone_format(self.mobile)
    #
    # @api.onchange('mobile', 'country_id', 'company_id')
    # def _onchange_mobile_validation(self):
    #     if self.mobile:
    #         self.mobile = self.phone_format(self.mobile)

    @api.model
    def create(self, values):
        # Add code here
        res = super(ResPartner, self).create(values)
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')
        is_auto_create = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_auto_create')
        if ax_api_id and ax_api_token and not 'air_contact_id' in values and is_auto_create and not res.air_contact_id and (res.phone or res.mobile):
            phone_num = []
            if res.phone:
                phone_num = [
                    {
                        "label": "Phone Number",
                        "value": res.phone
                    }
                ]
            elif res.mobile:
                phone_num = [
                    {
                        "label": "Mobile Number",
                        "value": res.mobile
                    }
                ]
            name = values['name'].split(' ')
            data = {
                "first_name": name[0] if name else phone_num,

                "information": "created from Odoo",
                "phone_numbers": phone_num,
                "emails": [
                    {
                        "label": "Odoo email",
                        "value": res.email
                    }
                ]
            }
            if len(name)>1:
                data['last_name']=name[1]

            auth = ax_api_id + ':' + ax_api_token
            encoded_auth = base64.b64encode(auth.encode()).decode()
            header = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic :{}'.format(encoded_auth)

            }
            response = requests.post(
                'https://api.aircall.io//v1/contacts',
                data = json.dumps(data),
                headers=header)

            if response.status_code == 400:
                raise ValidationError(json.loads(response.content)['troubleshoot']+'Please enter Phone/mobile number with country code')

            response = json.loads(response.content)
            if response:
                res.air_contact_id = response['contact']['id']
                return res
        else:
            return res

    def write(self, values):
        # Add code here
        res = super(ResPartner, self).write(values)
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')

        is_auto_update = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_auto_update')
        if 'air_contact_id' not in values:
            if ax_api_id and ax_api_token  and is_auto_update and self.air_contact_id and (self.phone or self.mobile):
                phone_num = []
                emails = []
                if 'phone' in values:
                    phone_num.append({
                            "label": "Phone Number",
                            "value": values['phone']
                        })

                elif 'mobile' in values:
                    phone_num.append( {
                            "label": "Mobile Number",
                            "value": values['mobile']
                        })

                if 'email' in values:
                    emails= [
                            {
                                "label": "Odoo email",
                                "value": self.email
                            }
                        ]

                data = {
                    "first_name": self.name,

                    "information": "created from Odoo",
                    "phone_numbers": phone_num,
                    "emails": [
                        {
                            "label": "Odoo email",
                            "value": self.email
                        }
                    ]
                }

                auth = ax_api_id + ':' + ax_api_token
                encoded_auth = base64.b64encode(auth.encode()).decode()
                header = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic :{}'.format(encoded_auth)

                }

                response = requests.post(
                    'https://api.aircall.io/v1/contacts/{}'.format(self.air_contact_id),

                    data=json.dumps(data),
                    headers=header)

                if response.status_code == 404 or response.status_code == 400:
                    raise ValidationError(json.loads(response.content)['error']+','+json.loads(response.content)['troubleshoot'])

                response = json.loads(response.content)
                # self.air_contact_id = response['contact']['id']
                return  res


            else:
                return res
        else:
            return res

    def export_contact(self):
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')

        if ax_api_id and ax_api_token:
            for contact in self:
                if contact.phone or contact.mobile:

                    phone_num = []
                    emails = []
                    if contact.phone:
                        phone = contact.phone
                        if phone[0]!='+':
                            phone = '+'+phone
                        phone_num.append({
                                "label": "Phone Number",
                                "value": phone.replace(')','').replace('(','').replace('-','')
                            })

                    elif contact.mobile:
                        mbl = contact.phone
                        if mbl[0] != '+':
                            mbl = '+' + mbl
                        phone_num.append( {
                                "label": "Mobile Number",
                                "value": mbl.replace(')','').replace('(','').replace('-','')
                            })

                    if contact.email:
                        emails= [
                                {
                                    "label": "Odoo email",
                                    "value": contact.email
                                }
                            ]

                    data = {
                        "first_name": contact.name,

                        "information": "created from Odoo",
                        "phone_numbers": phone_num,
                        "emails": [
                            {
                                "label": "Odoo email",
                                "value": contact.email
                            }
                        ]
                    }

                    auth = ax_api_id + ':' + ax_api_token
                    encoded_auth = base64.b64encode(auth.encode()).decode()
                    header = {
                        'Content-Type': 'application/json',
                        'Authorization': 'Basic :{}'.format(encoded_auth)

                    }
                    if contact.air_contact_id:
                        response = requests.post(
                            'https://api.aircall.io/v1/contacts/{}'.format(contact.air_contact_id),

                            data=json.dumps(data),
                            headers=header)

                        if response.status_code == 404 or response.status_code == 400:
                            raise ValidationError(json.loads(response.content)['error'])

                        response = json.loads(response.content)
                        self.air_contact_id = response['contact']['id']
                    else:
                        response = requests.post(
                            'https://api.aircall.io/v1/contacts',

                            data=json.dumps(data),
                            headers=header)

                        if response.status_code == 404 or response.status_code == 400:
                            raise ValidationError(json.loads(response.content)['error']+","+json.loads(response.content)['troubleshoot'])

                        response = json.loads(response.content)
                        self.air_contact_id = response['contact']['id']

                else:
                    continue

        else:
            raise ValidationError('AirCall Api id or Api Token not found!Please Ask to admin to add AirCall Credential')


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    call_tag_id = fields.Char(string="Call Tag Id", required=False, )


class MailMessage(models.Model):
    _inherit = 'mail.message'

    call_note_id = fields.Char(string="AirCall Note Id", required=False, )
    is_import = fields.Boolean(string="Is Import ")

    @api.model
    def create(self,value):
        res = super(MailMessage, self).create(value)
        ax_api_id = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_id')
        ax_api_token = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.ax_api_token')
        is_comment = self.env['ir.config_parameter'].sudo().get_param('aircall_connector.is_comment')
        if ('is_import' in value and value['is_import']) or ('message_type' in value and value['message_type']=='notification' or value['message_type']=='user_notification'):
            return res
        if is_comment and value['model']=='call.detail' :
            odoo_call = self.env['call.detail'].search([('id','=',value['res_id'])])
            if odoo_call.call_id :
                if not ax_api_id or not ax_api_token:
                    raise osv.except_osv(_("Error!"), (_("Please add Api Id and Api Token")))

                auth = ax_api_id + ':' + ax_api_token
                encoded_auth = base64.b64encode(auth.encode()).decode()
                header = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic :{}'.format(encoded_auth)

                }
                data = {'content':value['body']}
                response = requests.post(
                    'https://api.aircall.io/v1/calls/{}/comments'.format(odoo_call.call_id),
                    data = json.dumps(data),
                    headers=header)
                if response.status_code == 404:
                    _logger.error(
                        json.loads(response.content)['error'] + "," + json.loads(response.content)['troubleshoot'])
                    raise ValidationError(
                        json.loads(response.content)['error'] + "," + json.loads(response.content)['troubleshoot'])
                elif response.status_code == 400:
                    _logger.error(
                        json.loads(response.content)['error'] + "," + json.loads(response.content)['troubleshoot'])
                    raise ValidationError(
                        json.loads(response.content)['error'] + "," + json.loads(response.content)['troubleshoot'])
                elif response.status_code==201:
                    _logger.info('content has been posted on Aircall.')

        return res



class MailActivity(models.Model):
    _inherit = 'mail.activity'

    call_activity_id = fields.Char(string="AirCall Activity Id", required=False, )


# class PhoneValidation(models.AbstractModel):
#     _name = 'phone.validation'
#     _description = 'Phone Validation'
#
#     def _phone_get_country(self):
#         if 'country_id' in self and self.country_id:
#             return self.country_id
#         return self.env.company.country_id
#
#     def phone_format(self, number, country=None, company=None):
#         country = country or self._phone_get_country()
#         if not country:
#             return number
#         return phone_validation.phone_format(
#             number,
#             country.code if country else None,
#             country.phone_code if country else None,
#             force_format='INTERNATIONAL',
#             raise_exception=False
#         )
#

