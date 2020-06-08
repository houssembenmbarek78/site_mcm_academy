# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import random

class Session(models.Model):
    _name = 'mcmacademy.session'

    name=fields.Char('Nom du session',required=True)

    type_client=fields.Selection(selection=[
        ('intra', 'INTRA'),
        ('inter_entreprise', 'INTER ENTREPRISE'),
    ], string='Type de client')
    sous_traitance=fields.Boolean("Réalisé en sous traitance d'un autre organisme")
    action_type_id=fields.Many2one('mcmacademy.action',string="Type d'action de formation")
    domaine_formation=fields.Many2one('mcmacademy.domain',string='Domaine de formation')
    diplome_vise=fields.Char('Diplôme visé par la formation')
    module_ids=fields.One2many('mcmacademy.module',inverse_name='session_id',string='Liste des modules')
    client_ids=fields.Many2many('res.partner','session_clients_rel', 'session_id', 'client_id', string='')
    prospect_ids=fields.Many2many('res.partner','session_prospect_rel','session_id','prospect_id',string='')
    canceled_prospect_ids=fields.Many2many('res.partner','session_canceled_prospect_rel','session_id','prospect_id',string='')
    panier_perdu_ids=fields.Many2many('res.partner','session_panier_perdu_rel','session_id','prospect_id',string='')
    stage_id=fields.Many2one('mcmacademy.stage','État')
    color = fields.Integer(string='Color Index')
    date_debut=fields.Date('Date de debut de session')
    date_fin=fields.Date('Date de fin de session')
    count=fields.Integer('Nombre des clients',compute='_count_clients')
    number=fields.Char('Numéro',compute='_get_session_number')
    count_client=fields.Integer('',compute='_compute_count_clients')
    count_stagiaires=fields.Integer('',compute='_compute_count_clients')
    count_perdu=fields.Integer('',compute='_compute_count_clients')
    count_annule=fields.Integer('',compute='_compute_count_clients')
    count_prospect=fields.Integer('',compute='_compute_count_clients')
    count_panier_perdu=fields.Integer('',compute='_compute_count_clients')


    @api.depends('client_ids','prospect_ids','canceled_prospect_ids')
    def _count_clients(self):
        for rec in self:
            rec.count=len(rec.client_ids)+len(rec.prospect_ids)

    def _get_session_number(self):
        for rec in self:
            rec.number='AF'+str(random.randint(1000000000,9999999999))

    def _inverse_date(self):
        for rec in self:
            print(rec.date_debut)
            print(rec.date_fin)

    @api.depends('client_ids','prospect_ids','canceled_prospect_ids')
    def _compute_count_clients(self):
        for rec in self:
            client_counter=0
            stagiaire_counter=0
            for client in rec.client_ids:
                if client.company_type=='person':
                    stagiaire_counter+=1
                else:
                    client_counter+=1
            rec.count_stagiaires=stagiaire_counter
            rec.count_client=client_counter
            perdu_counter=0
            canceled_counter=0
            for client in rec.canceled_prospect_ids:
                if client.statut == 'perdu ':
                    perdu_counter += 1
                elif client.statut=='canceled':
                    canceled_counter += 1
            rec.count_perdu=perdu_counter
            rec.count_annule=canceled_counter
            prospect_counter=0
            rec.count_prospect=len(rec.prospect_ids)
            rec.count_panier_perdu=len(rec.panier_perdu_ids)









