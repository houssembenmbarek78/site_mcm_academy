# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models, _
import calendar
from datetime import date, datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    def create(self, vals):

        partner = super(Partner, self).create(vals)
        return partner

    def write(self, vals):
        if 'statut_cpf' in vals:
            # Si statut cpf non traité on classe l'apprenant dans le pipeline du crm  sous etat non traité
            if vals['statut_cpf'] == 'untreated':
                self.changestatut("Non traité", self)
            # Si statut cpf validé on classe l'apprenant dans le pipeline du crm  sous etat validé
            if vals['statut_cpf'] == 'validated':
                self.changestatut("Validé", self)
            # Si statut cpf accepté on classe l'apprenant dans le pipeline du crm  sous statut  accepté
            if vals['statut_cpf'] == 'accepted':
                self.changestatut("Accepté", self)

        # else:

        #     for rec in self:
        #         if rec.statut_cpf == 'untreated':
        #             self.changestatut("Non traité")
        #             print('statut',rec.statut_cpf)

        record = super(Partner, self).write(vals)

        return record

    def changestatut(self, name, partner):
        stage = self.env['crm.stage'].sudo().search([("name", "like", _(name))])
        _logger.info('stageeeee %s' %stage.name)
        if stage:

            leads = self.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
            print('leeaaadd', leads)
            if leads:
                for lead in leads:
                    if parnter.numero_cpf:
                        num_dossier = partner.numero_cpf
                    lead.sudo().write({
                        'name': partner.name,
                        'partner_name': partner.name,
                        'num_dossier': num_dossier,
                        'num_tel': partner.phone,
                        'email': partner.email,
                        'type': "opportunity",
                        'stage_id': stage.id
                    })

            if not leads:
                num_dossier = ""
                if partner.numero_cpf:
                    num_dossier = partner.numero_cpf
                print("create lead self", partner)
                lead = self.env['crm.lead'].sudo().create({
                    'name': partner.name,
                    'partner_name': partner.name,
                    'num_dossier': num_dossier,
                    'num_tel': partner.phone,
                    'email': partner.email,
                    'type': "opportunity",
                    'stage_id': stage.id
                })
                partner = self.env['res.partner'].sudo().search([('id', '=', partner.id)])
                if partner:
                    print("parnterrrr", lead.partner_id)
                    lead.partner_id = partner

    def change_statut_non_retracte(self):
        partners = self.env['res.partner'].sudo().search([('statut', "=", "won")])

        for partner in partners:
            # Pour chaque apprenant extraire la session et la formation reservé pour passer l'examen
            sale_order = self.env['sale.order'].sudo().search([('partner_id', '=', partner.id),
                                                               ('session_id', '=', partner.mcm_session_id.id),
                                                               ('module_id', '=', partner.module_id.id),
                                                               ('state', '=', 'sale'),
                                                               ('session_id.date_exam', '>', date.today())
                                                               ], limit=1, order="id desc")

            _logger.info('partner  %s' % partner.name)
            _logger.info('sale order %s' % sale_order.name)
            # Récupérer les documents et vérifier s'ils sont validés ou non
            documents = self.env['documents.document'].sudo().search([('partner_id', '=', partner.id)])
            document_valide = False
            count = 0
            for document in documents:
                if (document.state == "validated"):
                    count = count + 1
                    print('valide')
            print('count', count, 'len', len(documents))
            if (count == len(documents) and count != 0):
                document_valide = True
            # Vérifier si partner a signé son contrat et si ses documents sont validés
            if ((sale_order) and (document_valide)):
                # delai de retractation
                failure = sale_order.failures
                renonciation = partner.renounce_request
                # date_signature=""
                # if sale_order.signed_on:
                date_signature = sale_order.signed_on
                #
                # # Calculer date d'ajout sur 360 apres 14jours de date de signature
                # date_ajout = date_signature + timedelta(days=14)
                today = datetime.today()
                # si l'apprenant a fait une renonce  ou a passé 14jours apres la signature de contrat
                # On le supprime de crm car il va etre ajouté sur 360
                if (failure) or (renonciation):
                    print('parnter à supprimer  sale', partner.name, sale_order)
                    leads = self.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
                    _logger.info('partner if failure to delete  %s' % partner.name)
                    if leads:
                        for lead in leads:
                            _logger.info('lead order %s' % lead.name)
                            lead.sudo().unlink()
                elif (date_signature and (date_signature + timedelta(days=14)) <= (today)):
                    print('parnter à supprimer  date', partner.name, sale_order)
                    leads = self.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
                    print('leeaaadd', leads)
                    if leads:
                        for lead in leads:
                            _logger.info('lead signature %s' % lead.name)
                            lead.sudo().unlink()
                # Si non il est classé comme apprenant non retracté
                else:
                    _logger.info('non retracté' )
                    self.changestatut("Non Retracté", partner)
