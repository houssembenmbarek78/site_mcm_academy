# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta

from odoo import models, api, fields,_
import werkzeug
import json
import requests
from datetime import timedelta, datetime,date
import logging
_logger = logging.getLogger(__name__)


class Api(models.Model):
    _name = 'calendly.api'
    _description = "Calendly API"

    client_id = fields.Char(string="Calendly client ID", required=True,
                            default='90d14d3507c35d579924cf87a6de7fbc560211289ee1812e554c683c346f3a9c')
    client_secret = fields.Char(string="Calendly client Secret", required=True,
                                default='b863ae64bfa9ebd0d8aa8010028f3bf1041e1f678b682b710d4dec928d0fcca8')
    redirect_uri = fields.Char(string="Calendly redirect URI", required=True, default='https://www.mcm-academy.fr/')
    access_token = fields.Char(string="Calendly access token", required=True)
    refresh_token = fields.Char(string="Calendly refresh token", required=True)

    def _refresh_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        url = "http://calendly.com/oauth/token"

        calendly = self.env['calendly.api'].sudo().search([])
        if calendly:
            data = {'client_id': calendly.client_id,
                    'client_secret': calendly.client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': calendly.refresh_token}
            r = requests.post(url, data=data, headers=headers, timeout=65)
            response = werkzeug.utils.unescape(r.content.decode())
            json_data = json.loads(r.text)
            print(json_data)
            now = date.today()
            min_start_time=str(now)+'T00:00:00Z'
            if "access_token" in json_data:
                access=str(json_data["access_token"])
                refresh=str(json_data["refresh_token"])
                self._cr.execute("""UPDATE calendly_api SET access_token = %s WHERE id=%s""", (access,calendly.id,))
                self._cr.commit()
                self._cr.execute("""UPDATE calendly_api SET refresh_token = %s WHERE id=%s""", (refresh,calendly.id,))
                self._cr.commit()
                calendly = self.env['calendly.api'].sudo().search([])
                headers = {
                    'Authorization': 'Bearer ' + str(json_data["access_token"]),
                }
                data = {
                    'min_start_time': min_start_time,
                    'order': 'desc'
                }

                response = requests.get('https://calendly.com/api/v2/users/me/events', headers=headers,data=data)
                json_data_events = json.loads(response.text)

                headers1 = {
                    'X-TOKEN': 'OGIKABGGLJGSFHATPAZZ4DQ4KSM4XV3N',
                }

                response1 = requests.get('https://calendly.com/api/v1/users/me/event_types', headers=headers1)
                json_data_type_events=json.loads(response1.text)
                if "collection" in json_data_events:
                    collection = json_data_events["collection"]
                    print('-----------------collection-------------')
                    print(collection)
                    for event in collection:
                        event_type = event["event_type"]
                        uuid_type = event_type["uuid"]
                        if uuid_type == 'ADFC5PM4NYKEQ3TZ':
                            if "uuid" in event:
                                uuid = event["uuid"]
                                url_event = 'https://calendly.com/api/v2/events/' + str(uuid) + '/invitees'
                                event_response = requests.get(url_event,
                                                              headers=headers)
                                json_data_event = json.loads(event_response.text)
                                # lead = self.env['crm.lead'].sudo().search(
                                #     [('uuid', "=", str(uuid))])
                                # start_date = str(event["start_time"])
                                # start_time = start_date[12:19]
                                # start_date = start_date[:10]
                                # end_date = str(event["end_time"])
                                # end_time = end_date[12:19]
                                # end_date = end_date[:10]
                                # invitees_counter = event["invitees_counter"]
                                # invitees_active = invitees_counter["active"]
                                # invitees_limit = invitees_counter["limit"]
                                # type_evenement = event["event_type"]
                                # type_evenement = type_evenement["name"]
                                # start_date = datetime.strptime(str(start_date), '%Y-%m-%d')
                                # end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                                # stage = ''
                                # if (start_date.date() == date.today()):
                                #     stage = self.env['crm.stage'].sudo().search(
                                #         [('name', "=", _('Jour J'))])
                                # elif (start_date.date() > date.today()):
                                #     stage = self.env['crm.stage'].sudo().search(
                                #         [('name', "=", _('À Venir'))])
                                # elif (start_date.date() < date.today()):
                                #     stage = self.env['crm.stage'].sudo().search(
                                #         [('name', "=", _('Passé'))])
                                # if not lead:
                                #     lead = self.env['crm.lead'].sudo().create({
                                #         'name': "Session d'info",
                                #         'uuid': str(uuid),
                                #         'type_evenement': str(type_evenement),
                                #         'invitees_limit': int(invitees_limit),
                                #         'invitees_active': int(invitees_active),
                                #         'start_time': str(start_time),
                                #         'end_time': str(end_time),
                                #         'start_date': start_date.date(),
                                #         'end_date': end_date.date(),
                                #         'stage_id': stage.id if stage else ''
                                #     })
                                # else:
                                #     lead.type_evenement=str(type_evenement)
                                #     lead.invitees_limit=int(invitees_limit)
                                #     lead.invitees_active=int(invitees_active)
                                #     lead.start_time=str(start_time)
                                #     lead.end_time=str(end_time)
                                #     lead.start_date=start_date.date()
                                #     lead.end_date=end_date.date()
                                #     lead.stage_id=stage.id if stage else ''
                                if "collection" in json_data_event:
                                    collection = json_data_event["collection"]
                                    for invitee in collection:
                                        email = invitee["email"]
                                        user = self.env['res.users'].sudo().search(
                                            [('login', 'ilike', str(email))])
                                        if not user:
                                            email = invitee["email"].replace(' ', '')
                                            email = email.lower()
                                            client = self.env['res.partner'].sudo().search(
                                                [('email', 'ilike', str(email))])
                                            user = self.env['res.users'].sudo().search(
                                                [('login', 'ilike', str(email))])
                                            # if not client:
                                            #     contact = self.env['res.partner'].sudo().create({
                                            #         'name': str(invitee["name"]),
                                            #         'email': str(invitee["email"]),
                                            #         'company_type': 'person'
                                            #     })
                                            phone_mobile = ''
                                            if not user:
                                                infos = invitee["questions_and_answers"]
                                                for inf in infos:
                                                    if (str(inf["question"]) == "Numéro de téléphone "):
                                                        phone_mobile = str(inf["answer"])
                                                        client = self.env['res.partner'].sudo().search(
                                                            ['|', ('mobile', "=", phone_mobile),
                                                             (('phone', "=", phone_mobile))],limit=1)
                                                        if client:
                                                            user = self.env['res.users'].sudo().search(
                                                                [('partner_id', "=", client.id)])
                                                        else:
                                                            phone_mobile = phone_mobile.replace(' ', '')
                                                            client = self.env['res.partner'].sudo().search(
                                                                ['|', ('mobile', "=", phone_mobile),
                                                                 (('phone', "=", phone_mobile))],limit=1)
                                                            if client:
                                                                user = self.env['res.users'].sudo().search(
                                                                    [('partner_id', "=", client.id)])
                                                            phone_mobile = phone_mobile[3:]
                                                            phone_mobile = "0" + str(phone_mobile)
                                                            client = self.env['res.partner'].sudo().search(
                                                                ['|', ('mobile', "=", phone_mobile),
                                                                 (('phone', "=", phone_mobile))],limit=1)
                                                            if client:
                                                                user = self.env['res.users'].sudo().search(
                                                                    [('partner_id', "=", client.id)])
                                            if not user:
                                                client = self.env['res.partner'].sudo().search(
                                                    [('email', 'ilike', invitee["email"])])
                                                group_portal = self.env.ref('base.group_portal')
                                                user = self.env['res.users'].sudo().create({
                                                    'name': str(invitee["name"]),
                                                    'login': str(invitee["email"]),
                                                    'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
                                                    'email': False,
                                                    'notification_type': 'email',

                                                })
                                            user = self.env['res.users'].sudo().search(
                                                [('login', "=", invitee["email"])])
                                            client= False
                                            if user:
                                                client = self.env['res.partner'].sudo().search(
                                                        [('id', "=" , user.partner_id.id)])
                                                if client:
                                                    x = str(user.login)
                                                    client.email = x
                                                    infos = invitee["questions_and_answers"]
                                                    print('infos')
                                                    print(infos)
                                                    for inf in infos:
                                                        if (str(inf["question"]) == "Ville"):
                                                            if str(inf["answer"]):
                                                                client.city = str(inf["answer"])
                                                        if (str(inf["question"]) == "Votre adresse postale"):
                                                            if str(inf["answer"]):
                                                                client.street = str(inf["answer"])
                                                        if (str(inf[
                                                                    "question"]) == "Date de naissance : JJ / MM / AAAA"):
                                                            if str(inf["answer"]):
                                                                date_str = str(inf["answer"])
                                                                if (len(date_str) == 10 and date_str[2] == '/' and
                                                                        date_str[
                                                                            5] == '/'):
                                                                    date_object = datetime.strptime(date_str,
                                                                                                    '%d/%m/%Y').date()
                                                                    client.birthday = date_object
                                                        if (str(inf["question"]) == "Code postale"):
                                                            if str(inf["answer"]):
                                                                client.zip = str(inf["answer"])
                                                        if (str(inf["question"]) == "Formation :" or str(
                                                                inf["question"]) == "Formation : "):
                                                            if str(inf["answer"]):
                                                                formation_type = str(inf["answer"]).lower()
                                                                if (
                                                                        formation_type == 'taxi' or formation_type == 'vtc'):
                                                                    client.formation_type = formation_type
                                                        if (str(inf["question"]) == "Quel est votre financement"):
                                                            if str(inf["answer"]):
                                                                if (str(inf["answer"]) == "Mon Compte Formation, CPF"):
                                                                    client.funding_type = 'cpf'
                                                                if (str(inf["answer"]) == "Pass'formation"):
                                                                    client.funding_type = 'passformation'
                                                                if (str(inf["answer"]) == "Personnel"):
                                                                    client.funding_type = 'perso'
                                                                if (str(inf["answer"]) == "Pôle emploi(AIF)"):
                                                                    client.funding_type = 'pole_emploi'
                                                        if (str(inf["question"]) == "ID POLE EMPLOI"):
                                                            if str(inf["answer"]):
                                                                client.pole_emploi = str(inf["answer"])
                                                        if (str(inf["question"]) == "Numéro de sécurité social"):
                                                            if str(inf["answer"]):
                                                                client.social_security_number = str(inf["answer"])
                                                        if (str(inf["question"]) == "Numéro de téléphone "):
                                                            if str(inf["answer"]):
                                                                client.mobile = str(inf["answer"])
                                                        if (str(inf[
                                                                    "question"]) == "Veuillez répondre aux questions(Case vide = Non éligible pour la formation)"):
                                                            if str(inf["answer"]):
                                                                requis = str(inf["answer"])
                                                                if "J'ai 3 ans de permis ou plus" in requis:
                                                                    client.driver_licence = True
                                                                if "J'ai aucun retrait définitif du permis ces 10 dernières années" in requis:
                                                                    client.license_suspension = True
                                                                if "J'ai un casier judiciaire vierge B2" in requis:
                                                                    client.criminal_record = True
                                                                if client.driver_licence and client.license_suspension and client.criminal_record:
                                                                    client.statut_calendly = 'valid'
                                                                else:
                                                                    client.statut_calendly = 'waiting'
                                                    # list = []
                                                    # for partner in lead.partner_ids:
                                                    #     list.append(partner.id)
                                                    # list.append(client.id)
                                                    # lead.write({'partner_ids': [(6, 0, list)]})
                                                    return True