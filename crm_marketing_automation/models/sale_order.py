# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models,_
import calendar
from datetime import date,datetime
import logging
_logger = logging.getLogger(__name__)

class Sale(models.Model):
    _inherit='sale.order'

    @api.model
    def create(self, vals):
        print('drafttt', vals)
        partner_id = vals['partner_id']
        partner = self.env['res.partner'].sudo().search([('id', '=', partner_id)],limit=1)
        print('partner', partner)
        self.change_stage_lead("Prospection", partner)
        res = super(Sale, self).create(vals)

        return res
    
    def write(self, vals):
        record = super(Sale, self).write(vals)
        #Si le contrat a changé d'état 
        # on change le statut de l'apprenant dans le lead 
        if 'state' in vals:
            if vals['state'] == 'sent':
                partner = self.partner_id
                print('sent', partner)
                print('change statut', partner.mcm_session_id.id, partner.session_id.id)
                if (partner.mcm_session_id.id) and (partner.mcm_session_id.id == self.session_id.id):

                    self.change_stage_lead("Contrat non Signé", partner)
            if vals['state'] == 'sale':
                partner = self.partner_id
                print('sale', partner)
                print('change statut', partner.mcm_session_id.id, partner.session_id.id)
                if (partner.mcm_session_id.id) and (partner.mcm_session_id.id == self.session_id.id):
        
                    self.change_stage_lead("Contrat Signé", partner)

        return record

    def change_stage_lead(self, statut, partner):
            print('if verifié')
            stage = self.env['crm.stage'].sudo().search([("name", "=", _(statut))])
            print('stageeeee', stage)
            if stage:

                lead= self.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)],limit=1)
            
                if lead:
               
                    num_dossier = ""
                    if partner.numero_cpf:
                        num_dossier = partner.numero_cpf
                    lead.sudo().write({
                        'name': partner.name,
                        'partner_name': partner.name,
                        'num_dossier': num_dossier,
                        'num_tel': partner.phone,
                        'email': partner.email,
                        'email_from': partner.email,
                        'type': "opportunity",
                        'stage_id': stage.id,
                        'mode_de_financement':partner.mode_de_financement
                    })

                if not lead:
                    num_dossier = ""
                    if partner.numero_cpf:
                        num_dossier = partner.numero_cpf
                    print("create lead self", partner.name, partner.email, num_dossier)
                    lead = self.env['crm.lead'].sudo().create({
                        'name': partner.name,
                        'partner_name': partner.name,
                        'num_dossier': num_dossier,
                        'num_tel': partner.phone,
                        'email': partner.email,
                        'email_from': partner.email,
                        'type': "opportunity",
                        'stage_id': stage.id,
                        'mode_de_financement':partner.mode_de_financement
                    })
                    print('leaddddd', partner)
                    lead.partner_id = partner