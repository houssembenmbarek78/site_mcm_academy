# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api,_
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.http import request

class resPartner(models.Model):
    _inherit = "res.partner"

    diplome=fields.Char("Diplôme")


    @api.model
    def create(self, values):
        partner= super(resPartner, self).create(values)
        if partner.mcm_session_id:
            check_portal = False
            if partner.user_ids:
                for user in self.partner_id.user_ids:
                    groups = user.groups_id
                    for group in groups:
                        if (group.name == _('Portail')):
                            check_portal = True
            if check_portal:
                if partner.statut == 'won' or partner.statut == 'finalized':
                    list = []
                    for client in partner.mcm_session_id.client_ids:
                        list.append(client.id)
                    list.append(partner.id)
                    partner.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.prospect_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.canceled_prospect_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.panier_perdu_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                if partner.statut == 'indecis':
                    list = []
                    for client in partner.mcm_session_id.prospect_ids:
                        list.append(client.id)
                    list.append(partner.id)
                    partner.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.client_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.canceled_prospect_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.panier_perdu_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                if partner.statut == 'panier_perdu':
                    list = []
                    for client in partner.mcm_session_id.panier_perdu_ids:
                        list.append(client.id)
                    list.append(partner.id)
                    partner.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.client_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.canceled_prospect_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.prospect_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})

                if partner.statut == 'perdu' or partner.statut == 'canceled':
                    list = []
                    for client in partner.mcm_session_id.canceled_prospect_ids:
                        list.append(client.id)
                    list.append(partner.id)
                    partner.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})
                    list = []
                    for client in partner.mcm_session_id.client_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.panier_perdu_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                    list = []
                    for client in partner.mcm_session_id.panier_perdu_ids:
                        if client.id != partner.id:
                            list.append(client.id)
                    partner.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})
        return partner

    def write(self, vals):
        User = self.env.user
        check_portal = False
        group_portal = self.env.ref('base.group_portal')
        if User.user_has_groups('base.group_portal'):
            check_portal = True
        if 'statut' in vals and 'module_id' not in vals:
            if check_portal == False:
                if vals['statut'] == 'won':
                    if (self.module_id.number_places_available <= 0):
                        raise ValidationError(_(
                            'Le nombre de places disponibles est atteint, basculer le condidat vers la prochaine session.'))
        if 'module_id' in vals and 'statut' not in vals:
            if check_portal == False:
                # if self.statut == 'won' and self.statut == 'finalized':
                module = self.env['mcmacademy.module'].sudo().search([('id', '=', vals['module_id'])])
                if module:
                    if (self.module_id.id != module.id):
                        if (module.number_places_available <= 0):
                            raise ValidationError(_(
                                'Le nombre de places disponibles est atteint, basculer le condidat vers la prochaine session.'))
        if 'module_id' in vals and 'statut' in vals:
            print('test3')
            if check_portal == False:
                module = self.env['mcmacademy.module'].sudo().search([('id', '=', vals['module_id'])])
                if module:
                    if ((vals['statut'] == 'won') and (module.number_places_available <= 0)):
                        raise ValidationError(_(
                            'Le nombre de places disponibles est atteint, basculer le condidat vers la prochaine session.'))
        partner = super(resPartner, self).write(vals)
        if self.mcm_session_id:
            check_portal = False
            if self.user_ids:
                for user in self.user_ids:
                    groups = user.groups_id
                    for group in groups:
                        if (group.name == _('Portail')):
                            check_portal = True
            if check_portal:
                if self.statut == 'won' or self.statut == 'finalized':
                    list = []
                    for client in self.mcm_session_id.client_ids:
                        list.append(client.id)
                    list.append(self.id)
                    self.mcm_session_id.write({'client_ids': [(6, 0, list)]})
                    if self.module_id:
                        compteur = 0
                        for client in self.mcm_session_id.client_ids:
                            if client.module_id == self.module_id:
                                compteur += 1
                        self.module_id.number_places_available = self.module_id.max_number_places - compteur

                    list = []
                    for client in self.mcm_session_id.prospect_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.canceled_prospect_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.panier_perdu_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                if self.statut == 'indecis':
                    list = []
                    for client in self.mcm_session_id.prospect_ids:
                        list.append(client.id)
                    list.append(self.id)
                    self.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.client_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.canceled_prospect_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.panier_perdu_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                if self.statut == 'panier_perdu':
                    list = []
                    for client in self.mcm_session_id.panier_perdu_ids:
                        list.append(client.id)
                    list.append(self.id)
                    self.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.client_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.canceled_prospect_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.prospect_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})
                if self.statut == 'perdu' or self.statut == 'canceled':
                    list = []
                    for client in self.mcm_session_id.canceled_prospect_ids:
                        list.append(client.id)
                    list.append(self.id)
                    self.mcm_session_id.write({'canceled_prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.client_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'client_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.prospect_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'prospect_ids': [(6, 0, list)]})

                    list = []
                    for client in self.mcm_session_id.panier_perdu_ids:
                        if client.id != self.id:
                            list.append(client.id)
                    self.mcm_session_id.write({'panier_perdu_ids': [(6, 0, list)]})
        return partner