# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta

from odoo import models, api, fields
import werkzeug
import json
import requests
from datetime import timedelta, datetime
import logging
_logger = logging.getLogger(__name__)


class Api(models.Model):
    _name = 'calendly.api'
    _description = "Calendly API"

    client_id = fields.Char(string="Calendly client ID", required=True,
                            default='30619c87f05a76ccd4f44ee59d4281a3714395299a4b277492c7f0d149e09462')
    client_secret = fields.Char(string="Calendly client Secret", required=True,
                                default='86bd046a39760594cc2fdd7036571842db01ac3122c4e4df8d6b4e43933ea2ba')
    redirect_uri = fields.Char(string="Calendly redirect URI", required=True, default='https://test.mcm-academy.fr/')
    access_token = fields.Char(string="Calendly access token", required=True,
                               default='e5c6c2422786d08cc58c5cface0fe510fad175f5350f370932eaa86d7104b2ac')
    refresh_token = fields.Char(string="Calendly access token", required=True,
                                default='a961a7d268365568dc1e03ec603f7e45059778cbfd81b58705636cc47eb9bea0')

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
                response = requests.get('https://calendly.com/api/v2/users/me/events', headers=headers)
                json_data_events = json.loads(response.text)

                if "collection" in json_data_events:
                    collection = json_data_events["collection"]

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
                                if "collection" in json_data_event:
                                    collection = json_data_event["collection"]
                                    for invitee in collection:
                                        client = self.env['res.partner'].sudo().search(
                                            [('email', 'ilike', invitee["email"])])
                                        user = self.env['res.users'].sudo().search(
                                            [('login', 'ilike', invitee["email"])])
                                        # if not client:
                                        #     contact = self.env['res.partner'].sudo().create({
                                        #         'name': str(invitee["name"]),
                                        #         'email': str(invitee["email"]),
                                        #         'company_type': 'person'
                                        #     })
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
                                        client = self.env['res.partner'].sudo().search(
                                                [('id', '=', user.partner_id.id)])
                                        if client:
                                                client.email=user.login
                                                infos = invitee["questions_and_answers"]
                                                for inf in infos:
                                                    if (str(inf["question"]) == "Ville"):
                                                        client.city = str(inf["answer"])
                                                    if (str(inf["question"]) == "Votre adresse postale"):
                                                        client.street = str(inf["answer"])
                                                    if (str(inf["question"]) == "Date de naissance : JJ / MM / AAAA"):
                                                        date_str = str(inf["answer"])
                                                        if(len(date_str)==10 and date_str[2]=='/' and date_str[5]=='/'):
                                                            date_object = datetime.strptime(date_str, '%d/%m/%Y').date()
                                                            client.birthday = date_object
                                                    if (str(inf["question"]) == "Code postale"):
                                                        client.zip = str(inf["answer"])
                                                    if (str(inf["question"]) == "Formation :" or str(inf["question"]) == "Formation : "):
                                                        formation_type=str(inf["answer"]).lower()
                                                        if (formation_type=='taxi' or formation_type=='vtc'):
                                                            client.formation_type = str(inf["answer"]).lower()
                                                    if (str(inf["question"]) == "Quel est votre financement"):
                                                        if (str(inf["answer"]) == "Mon Compte Formation, CPF"):
                                                            client.funding_type = 'cpf'
                                                        if (str(inf["answer"]) == "Pass'formation"):
                                                            client.funding_type = 'passformation'
                                                        if (str(inf["answer"]) == "Personnel"):
                                                            client.funding_type = 'perso'
                                                        if (str(inf["answer"]) == "Pôle emploi(AIF)"):
                                                            client.funding_type = 'pole_emploi'
                                                    if (str(inf["question"]) == "ID POLE EMPLOI"):
                                                        client.pole_emploi = str(inf["answer"])
                                                    if (str(inf["question"]) == "Numéro de sécurité social"):
                                                        client.social_security_number = str(inf["answer"])
                                                    if (str(inf["question"]) == "Numéro de téléphone"):
                                                        client.phone = str(inf["answer"])
                                                    if (str(inf["question"]) == "Veuillez répondre aux questions(Case vide = Non éligible pour la formation)"):
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
