# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,tools
import sys
import logging
_logger = logging.getLogger(__name__)

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

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
                        partner.sudo().unlink() # supprimer la fiche contact de client si le client n'a pas de compte
        for ticket in tickets:
            if 'caissedesdepots' in ticket.partner_email:
                team = self.env['helpdesk.team'].sudo().search([('name', 'like', 'Compta'), ('company_id', "=", ticket.company_id.id)],limit=1)
                if team:
                    ticket.team_id=team.id
            if 'billing' in ticket.partner_email:
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
                    partner.sudo().unlink() # supprimer la fiche contact de client si le client n'a pas de compte
                    vals['partner_id']=False

        return super(HelpdeskTicket, self).write(vals)

    def unlink_ticket_rejected_mails(self):
        tickets = self.env["helpdesk.ticket"].sudo().search([], order="id DESC", limit=100)
        rejected_mails = [
            'no-reply@360learning.com','no-reply@zoom.us','notifications@calendly.com','no-reply','noreply','customermarketing@aircall.io','newsletter@axeptio.eu','order-update@amazon.fr',
            'uipath@discoursemail.com','dkv-euroservice.co','enjoy.eset.com','e.fiverr.com','paloaltonetworks.com',
            'eset-nod32.fr','nordvpn.com','newsletter','modedigital.online','ovh','envato','codeur','h5p'
            'facebook','google','ne_pas_repondre_Moncompteformation','digimoov.fr','mcm-academy.fr','slack.com'
        ]
        rejected_subject = [
            'nouveau ticket','assigné à vous','assigned to you'
        ]
        list_ticket=[]
        for ticket in tickets:
            if any(email in ticket.partner_email for email in rejected_mails):
                list_ticket.append(ticket.id)

        for ticket1 in tickets:
            if any(name in ticket1.name for name in rejected_subject):
                list_ticket.append(ticket.id)
        if list_ticket:
            for rejected_ticket in list_ticket:
                ticket = self.env["helpdesk.ticket"].sudo().search([('id',"=",rejected_ticket)])
                if ticket:
                    ticket.sudo().unlink()

