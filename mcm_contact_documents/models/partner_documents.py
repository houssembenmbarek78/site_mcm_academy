# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,_


class Documents(models.Model):
    _inherit = "documents.document"

    attachment_number=fields.Char('Numéro')
    confirmation=fields.Boolean('Je confirme avoir soumis le recto et le verso')
    state=fields.Selection(selection=[
        ('refused', 'Refuser'),
        ('waiting', 'Vérification en cours'),
        ('validated', 'Valider'),
    ], string='État de document',default="waiting")
    code_document = fields.Char('code document')

    def action_refuse_document(self):
        self.state='refused'
        lang = self.env.context.get('lang')
        template_id = self.env['ir.model.data'].xmlid_to_res_id('mcm_contact_documents.mail_template_refused_document',raise_if_not_found=False)
        subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mt_note')
        body = str(self.name).replace(str(self.owner_id.name), '') + ' a été refusé'
        message = self.env['mail.message'].sudo().create({
            'subject': 'Document refusé',
            'model': 'res.partner',
            'res_id': self.owner_id.partner_id.id,
            'message_type': 'notification',
            'subtype_id': subtype_id,
            'body': body,
        })
        ctx = {
            'default_model': 'documents.document',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    def wait_document(self):
        for rec in self:
            rec.write({'state': 'waiting'})
    def validate_document(self):
        for rec in self:
            rec.write({'state': 'validated'})

    def transfert_document(self):
        team=self.env['helpdesk.team'].sudo().search([('name', "=" , 'Administration Client')],limit=1)
        print(team)
        ctx = {
            'default_model': 'helpdesk.ticket',
            'default_res_id': self.ids[0],
            'default_name':self.name,
            'default_team_id':int(team),
            'default_partner_id':False,
            'default_partner_email':False,
            'default_description':''
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'helpdesk.ticket',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

