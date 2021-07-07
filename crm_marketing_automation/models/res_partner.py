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
                self.changestage("Non Traité", self)
            # Si statut cpf validé on classe l'apprenant dans le pipeline du crm  sous etat validé
            if vals['statut_cpf'] == 'validated':
                self.changestage("Validé", self)
            # Si statut cpf accepté on classe l'apprenant dans le pipeline du crm  sous statut  accepté
            if vals['statut_cpf'] == 'accepted':
                self.changestage("Accepté", self)

        # else:

        #     for rec in self:
        #         if rec.statut_cpf == 'untreated':
        #             self.changestage("Non traité")
        #             print('statut',rec.statut_cpf)

        record = super(Partner, self).write(vals)

        return record

    def changestage(self, name, partner):
        stage = self.env['crm.stage'].sudo().search([("name", "=", _(name))])
        
        if stage:

            lead = self.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)],limit=1)
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
                    'mode_financement':partner.mode_de_financement
                })

            if not lead:
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
                    'email_from': partner.email,
                    'type': "opportunity",
                    'stage_id': stage.id,
                    'mode_de_financement':partner.mode_de_financement
                })
                partner = self.env['res.partner'].sudo().search([('id', '=', partner.id)])
                if partner:
                    print("parnterrrr", lead.partner_id)
                    lead.partner_id = partner

    
    # Methode pour classer les apprenants dans crm lead comme non retracté
    # Vérifier tout les conditions nécessaires pour ce classement
    def change_stage_non_retracte(self):
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
                    self.changestage("Rétractation non Coché", partner)

    # Methode pour classer les apprenants existant déja sur odoo

    def change_stage_existant(self):
        partners = self.env['res.partner'].sudo().search([])

        for partner in partners:
            if partner.statut == "indecis":
                # Vérifier le statut  pour classer client  dans crm lead
                if partner.statut_cpf and partner.statut_cpf == "untreated":
                    print('non traité')
                    self.changestage("Non Traité", partner) 
                if partner.statut_cpf and partner.statut_cpf == "validated":
                    print('Validé')
                    self.changestage("Validé", partner)
                if partner.statut_cpf and partner.statut_cpf == "accepted":
                    print('accepté')
                    self.changestage("Accepté", partner)

            #Recuperer le contrat pour vérifier son statut

            sale_order = self.env['sale.order'].sudo().search([('partner_id', '=', partner.id),
                                                               ('session_id', '=', partner.mcm_session_id.id),
                                                               ('module_id', '=', partner.module_id.id),
                                                               ('session_id.date_exam', '>', date.today()),
                                                               ], limit=1, order="id desc")

            # Récupérer les documents
            documents = self.env['documents.document'].sudo().search([('partner_id', '=', partner.id)])
            # Classer client dans crm lead selon le statut de contrat
            if sale_order:
                if sale_order.state == "sent":
                     print('contrat non signé')
                     self.changestage("Contrat non Signé", partner)
                if sale_order.state == "sale" and not(documents):
                    dateexam=str(sale_order.session_id.date_exam)
                    _logger.info('contrat signé %s', dateexam)
                    self.changestage("Contrat Signé", partner)
                
                    # vérifier l'existance des document en etat waiting
                    # pour classer sous document dans crm lead
                if documents and sale_order.state == "sale":
                    waiting=False
                    for document in documents:
                        if (document.state == "waiting"):
                            _logger.info("document waiting")
                            waiting=True
                    if waiting:
                        self.changestage("Document non Validé", partner)
