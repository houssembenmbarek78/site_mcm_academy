# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models, _
import calendar
from datetime import date, datetime


class Partner(models.Model):
    _inherit = 'res.partner'



    def write(self, vals):
        if 'statut_cpf' in vals:
            # Si statut cpf non traité on classe l'apprenant dans le pipeline du crm  sous etat non traité
            if vals['statut_cpf'] == 'untreated':
                self.changestatut("Non traité")
            # Si statut cpf validé on classe l'apprenant dans le pipeline du crm  sous etat validé
            if vals['statut_cpf'] == 'validated':
                self.changestatut("Validé")
            # Si statut cpf accepté on classe l'apprenant dans le pipeline du crm  sous statut  accepté
            if vals['statut_cpf'] == 'accepted':
                self.changestatut("Accepté")
        else:
            for rec in self:
                if rec.statut_cpf == 'untreated':
                    self.changestatut("Non traité")
                    print('statut',rec.statut_cpf)

        record = super(Partner, self).write(vals)

        return record

    def changestatut(self, name):
        stage = self.env['crm.stage'].sudo().search([("name", "like", _(name))])
        print('stageeeee', stage)
        if stage:

            leads = self.env['crm.lead'].sudo().search([('partner_id', '=', self.id)])
            print('leeaaadd', leads)
            if leads:
                for lead in leads:
                    lead.sudo().write({
                        'stage_id': stage.id,
                        'type': "opportunity",
                    })

            if not leads:
                num_dossier=""
                if self.numero_cpf:
                    num_dossier=self.num_cpf
                print("create lead self", self)
                lead = self.env['crm.lead'].sudo().create({
                    'name': self.name,
                    'partner_name': self.name,
                    'num_dossier': num_dossier,
                    'email': self.email,
                    'type': "opportunity",
                    'stage_id': stage.id
                })
                partner = self.env['res.partner'].sudo().search([('id', '=', self.id)])
                if partner:
                    print("parnterrrr", lead.partner_id)
                    lead.partner_id = partner
