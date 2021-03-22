from odoo import _, api, fields, models, tools
from datetime import datetime, date


class PartnerDocuments(models.Model):
    _name = 'partner.documents'

    name = fields.Char(string='Title', required=True)
    attachment_id=fields.Many2one('ir.attachment','Pièce jointe',required=True)
    partner_id=fields.Many2one('res.partner','Client',required=True)
    attachment_number=fields.Char('Numéro')
    confirmation=fields.Boolean('Je confirme avoir soumis le recto et le verso')
    code=fields.Char('code document')
    state=fields.Selection(selection=[
        ('refuse', 'Refusé'),
        ('attente', 'En Attente de validation'),
        ('valide', 'Validé'),
    ], string='Statut',default='attente')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    def action_refuse_document(self):
        self.state='refuse'
        lang = self.env.context.get('lang')
        template_id = self.env['ir.model.data'].xmlid_to_res_id('mcm_contact_documents.mail_template_refused_document',                                                          raise_if_not_found=False)
        print('template')
        print(template_id)
        ctx = {
            'default_model': 'partner.documents',
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
    def action_validate_document(self):
        self.state = 'valide'