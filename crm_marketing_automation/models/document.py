# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models,_
import calendar
from datetime import date,datetime

class Document(models.Model):
    _inherit='documents.document'


    def write(self,vals):

        if 'state' in vals and not('partner_id' in vals):
            if vals['state'] =='waiting':
                partner=self.partner_id
                print('waite',partner)
                self.change_statut_lead("Document", partner)

        if 'state' in vals and  'partner_id' in vals:
            if vals['state'] == 'waiting':
                partner = vals['partner_id']
                print('waite', partner)
                self.change_statut_lead("Document", partner)

        if not('state' in vals) and 'partner_id' in vals:
            if self.state == 'waiting':
                partner = vals['partner_id']
                print('waite', partner)
                self.change_statut_lead("Document", partner)
        record = super(Document, self).write(vals)
        return record


    def change_statut_lead(self,statut,partner):


        print('if verifié')
        stage = self.env['crm.stage'].sudo().search([("name", "like", _(statut))])
        print('stageeeee', stage)
        if stage:

            leads = self.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
            print('leeaaadd', leads)
            if leads:
                for lead in leads:
                    lead.sudo().write({
                        'stage_id': stage.id,
                        'type': "opportunity",
                    })

            if not leads:
                num_dossier = ""
                if partner.numero_cpf:
                    num_dossier = partner.numero_cpf
                print("create lead self", partner.name,partner.email,num_dossier)
                lead = self.env['crm.lead'].sudo().create({
                    'name': partner.name,
                    'partner_name': partner.name,
                    'num_dossier': num_dossier,
                    'email': partner.email,
                    'type': "opportunity",
                    'stage_id': stage.id
                })

                lead.partner_id = partner.id
