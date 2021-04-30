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
            if 'caissedesdepots' in ticket.partner_email: # transferer les emails envoyés par caissedesdepots au service comptabilité
                team = self.env['helpdesk.team'].sudo().search([('name', 'like', 'Compta'), ('company_id', "=", ticket.company_id.id)],limit=1)
                if team:
                    ticket.team_id=team.id
            if 'billing' in ticket.partner_email: # transferer les emails envoyés par billing au service comptabilité
                team = self.env['helpdesk.team'].sudo().search([('name', 'like', 'Compta'), ('company_id', "=", ticket.company_id.id)],limit=1)
                if team:
                    ticket.team_id=team.id
            if 'servicefinance@dkv-euroservice.com' in ticket.partner_email: # transferer les emails envoyés par servicefinance@dkv-euroservice.com au service comptabilité
                team = self.env['helpdesk.team'].sudo().search(
                    [('name', 'like', 'Compta'), ('company_id', "=", ticket.company_id.id)], limit=1)
                if team:
                    ticket.team_id = team.id
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
        tickets = self.env["helpdesk.ticket"].sudo().search([], order="id DESC", limit=100) # récupérer les 100 derniers tickets créers 
        # list des terms ou emails rejetés ( supprimer les tickets envoyés par ces emails )
        rejected_mails = [
            'no-reply@360learning.com','zoom.us','notifications@calendly.com','product-feedback@calendly.com','no-reply','customermarketing@aircall.io','newsletter@axeptio.eu','order-update@amazon.fr',
            'uipath@discoursemail.com','info@dkv-euroservice.com','serviceclient@enjoy.eset.com','noreply@e.fiverr.com','hello@emails.paloaltonetworks.com',
            'francois.g@eset-nod32.fr','support@nordvpn.com','noreply@jotform.com','newsletter','communication@modedigital.online','support@ovh.com','do-not-reply@market.envato.com','cody@codeur.com','svein-tore.griff@joubel.com',
            'h5p','security@mail.instagram.com','notification@facebookmail.com','advertise-noreply@support.facebook.com','google','ne_pas_repondre_Moncompteformation','digimoov.fr','mcm-academy.fr','slack.com'
        ]
        # list des terms  rejetés ( supprimer les tickets qui ont l'un de ces terms comme objet )
        rejected_subject = [
            'nouveau ticket','assigné à vous','assigned to you'
        ]
        list_ids_deleted_tickets=[] # préparer une liste vide qui sera par les id des tickets à supprimer
        for ticket in tickets: #parcourir les 100 derniers tickets
            if any(email in ticket.partner_email for email in rejected_mails): #vérifier si l'email de client contient l'un des emails/terms rejetés mis à la liste rejected_mails
                list_ids_deleted_tickets.append(ticket.id) #ajouter l'id de ticket à list des tickets à supprimer
            else:
                rejected_notes = [
                    'Devis vu', 'Contrat signé', 'Quotation viewed by'
                ] # liste des terms des notes système créer en ticket à vérifier

                notes = self.env["mail.message"].sudo().search([('model',"=",'helpdesk.ticket'),('res_id',"=",ticket.id)]) #recupère tous les notes créer dans le ticket
                for note in notes: # parcourir les notes de la ticket
                    if any(term in note.body for term in rejected_notes): # vérifier si l'un des notes est parmis la liste rejected notes
                        list_ids_deleted_tickets.append(ticket.id) #ajouter l'id de ticket à list des tickets à supprimer
        for ticket in tickets:
            if any(name in ticket.name for name in rejected_subject): # vérifier si le nom de ticket contient un term parmis les termes de la liste rejected subject
                list_ids_deleted_tickets.append(ticket.id) #ajouter l'id de ticket à list des tickets à supprimer
        if list_ids_deleted_tickets: # vérifier si la liste des tickets à supprimer est vide ou non
            for rejected_ticket in list_ids_deleted_tickets: # parcourir la liste des tickets à supprimer
                ticket = self.env["helpdesk.ticket"].sudo().search([('id',"=",rejected_ticket)]) # récuperer la ticket à supprimer en utilisant l'id recupérer de la liste
                if ticket: # vérifier s'il y a une ticket avec cette id
                    ticket.sudo().unlink() #supprimer la ticket

