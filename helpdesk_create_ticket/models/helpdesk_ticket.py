# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,tools
import sys
import logging
_logger = logging.getLogger(__name__)

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    # @api.model_create_multi
    # def create(self, list_value):
    #     now = fields.Datetime.now()
    #     # determine user_id and stage_id if not given. Done in batch.
    #     teams = self.env['helpdesk.team'].browse([vals['team_id'] for vals in list_value if vals.get('team_id')])
    #     team_default_map = dict.fromkeys(teams.ids, dict())
    #     for team in teams:
    #         team_default_map[team.id] = {
    #             'stage_id': team._determine_stage()[team.id].id,
    #             'user_id': team._determine_user_to_assign()[team.id].id
    #         }
    #
    #     # Manually create a partner now since 'generate_recipients' doesn't keep the name. This is
    #     # to avoid intrusive changes in the 'mail' module
    #     # for vals in list_value:
    #     #     if 'partner_name' in vals and 'partner_email' in vals and 'partner_id' not in vals:
    #     #         try:
    #     #             vals['partner_id'] = self.env['res.partner'].find_or_create(
    #     #                 tools.formataddr((vals['partner_name'], vals['partner_email']))
    #     #             )
    #     #         except UnicodeEncodeError:
    #     #             # 'formataddr' doesn't support non-ascii characters in email. Therefore, we fall
    #     #             # back on a simple partner creation.
    #     #             vals['partner_id'] = self.env['res.partner'].create({
    #     #                 'name': vals['partner_name'],
    #     #                 'email': vals['partner_email'],
    #     #             }).id
    #
    #     # determine partner email for ticket with partner but no email given
    #     # partners = self.env['res.partner'].browse([vals['partner_id'] for vals in list_value if 'partner_id' in vals and vals.get('partner_id') and 'partner_email' not in vals])
    #     # partner_email_map = {partner.id: partner.email for partner in partners}
    #     # partner_name_map = {partner.id: partner.name for partner in partners}
    #
    #     for vals in list_value:
    #         if vals.get('team_id'):
    #             team_default = team_default_map[vals['team_id']]
    #             if 'stage_id' not in vals:
    #                 vals['stage_id'] = team_default['stage_id']
    #             # Note: this will break the randomly distributed user assignment. Indeed, it will be too difficult to
    #             # equally assigned user when creating ticket in batch, as it requires to search after the last assigned
    #             # after every ticket creation, which is not very performant. We decided to not cover this user case.
    #             if 'user_id' not in vals:
    #                 vals['user_id'] = team_default['user_id']
    #             if vals.get('user_id'):  # if a user is finally assigned, force ticket assign_date and reset assign_hours
    #                 vals['assign_date'] = fields.Datetime.now()
    #                 vals['assign_hours'] = 0
    #
    #         # set partner email if in map of not given
    #         # if vals.get('partner_id') in partner_email_map:
    #         #     vals['partner_email'] = partner_email_map.get(vals['partner_id'])
    #         # set partner name if in map of not given
    #         # if vals.get('partner_id') in partner_name_map:
    #         #     vals['partner_name'] = partner_name_map.get(vals['partner_id'])
    #
    #         if vals.get('stage_id'):
    #             vals['date_last_stage_update'] = now
    #
    #     # context: no_log, because subtype already handle this
    #     tickets = super(HelpdeskTicket, self).create(list_value)
    #
    #     # make customer follower
    #     for ticket in tickets:
    #         if ticket.partner_id:
    #             ticket.message_subscribe(partner_ids=ticket.partner_id.ids)
    #
    #     # apply SLA
    #     tickets.sudo()._sla_apply()
    #
    #     return tickets

    @api.model_create_multi
    def create(self, list_value):
        tickets = super(HelpdeskTicket, self).create(list_value)
        for rec in list_value:
            if 'partner_id' in rec:
                if rec['partner_id']:
                    user = self.env['res.users'].sudo().search([('partner_id', "=", rec['partner_id'])])
                else:
                    user = self.env['res.users'].sudo().search([('login', "=", rec['partner_email'])])
                if not user:
                    partner = self.env['res.partner'].sudo().search([('id', "=", rec['partner_id'])])
                    if partner:
                        partner.sudo().unlink()
        for ticket in tickets:
            if 'caissedesdepots' in ticket.partner_email:
                team = self.env['helpdesk.team'].sudo().search([('name', 'like', 'Compta'), ('company_id', "=", ticket.company_id.id)],limit=1)
                if team:
                    ticket.team_id=team.id
        return tickets

    def write(self, vals):
        if 'partner_id' in vals:
            partner_id=vals['partner_id']
            user = self.env['res.users'].sudo().search([('partner_id', "=", partner_id)])
            if not user:
                partner = self.env['res.partner'].sudo().search([('id', "=", vals['partner_id'])])
                if partner:
                    partner.sudo().unlink()
                    vals['partner_id']=False

        tickets = super(HelpdeskTicket, self).write(vals)
        rejected_mails = [
            '360learning','@zoom','zoom.us','calendly','no-reply','noreply','aircall','axeptio','@amazon',
            'uipath','dkv-euroservice.co','enjoy.eset.com','e.fiverr.com','paloaltonetworks.com',
            'eset-nod32.fr','nordvpn.com','newsletter','modedigital.online','ovh','envato','codeur','h5p'
            'facebook','google','ne_pas_repondre_Moncompteformation','digimoov.fr','mcm-academy.fr','slack.com'
        ]
        rejected_subject = [
            'nouveau ticket','assigné à vous','assigned to you'
        ]
        for ticket in tickets:
            if any(email in ticket.partner_email for email in rejected_mails):
                ticket.sudo().unlink()
        for ticket in tickets:
            if any(name in rec['name'] for name in rejected_subject):
                ticket.sudo().unlink()

