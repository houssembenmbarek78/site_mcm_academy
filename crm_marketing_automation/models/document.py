# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models,_
import calendar
from datetime import date,datetime
import logging

_logger = logging.getLogger(__name__)
class Document(models.Model):
    _inherit='documents.document'


    def write(self,vals):
        _logger.info(' write ' )
        if 'state' in vals and not('partner_id' in vals):
            if vals['state'] =='waiting':
                partner=self.partner_id
                _logger.info('if state in write  %s' % partner.name)
                self.change_stage_lead("Document non Validé", partner)

        if 'state' in vals and  'partner_id' in vals:
            if vals['state'] == 'waiting':
                partner = vals['partner_id']
                print('waite', partner)
                self.change_stage_lead("Document non Validé", partner)

        if not('state' in vals) and 'partner_id' in vals:
            if self.state == 'waiting':
                partner = vals['partner_id']
                print('waite', partner)
                self.change_stage_lead("Document non Validé", partner)
        record = super(Document, self).write(vals)
        return record


    def change_stage_lead(self,statut,partner):
        sale_order = self.env['sale.order'].sudo().search([('partner_id', '=', partner.id),
                                                           ('session_id', '=', partner.mcm_session_id.id),
                                                           ('module_id', '=', partner.module_id.id),
                                                           ('state', '=', 'sale'),
                                                           ('session_id.date_exam', '>', date.today())
                                                           ], limit=1, order="id desc")

        _logger.info('partner  %s' % partner.name)
        _logger.info('sale order %s' % sale_order.name)
        if sale_order:
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
                    print("create lead self", partner.name,partner.email,num_dossier)
                    lead = self.env['crm.lead'].sudo().create({
                        'name': partner.name,
                        'partner_name': partner.name,
                        'num_dossier': num_dossier,
                        'email': partner.email,
                        'email_from': partner.email,
                        'type': "opportunity",
                        'stage_id': stage.id,
                        'mode_de_financement':partner.mode_de_financement
                    })
    
                    lead.partner_id = partner.id
