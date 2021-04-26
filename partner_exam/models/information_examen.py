# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import datetime, base64
from odoo.exceptions import ValidationError



class NoteExamen(models.Model):
    _name = "info.examen"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Les Notes et les informations des examens"

    partner_id = fields.Many2one('res.partner', string="Client")
    epreuve_a = fields.Float(string="Epreuve A(QCM):")
    epreuve_b = fields.Float(string="Epreuve B(QRO)")
    moyenne_generale = fields.Float(compute="_compute_moyenne_generale", string="Moyenne Générale")
    mention = fields.Selection(selection=[
        ('recu', 'reçu'),
        ('ajourne', 'ajourné')],
        string="Mention", default=False)
    resultat = fields.Selection(selection=[
        ('recu', 'Reçu'),
        ('ajourne', 'Ajourné')], string="Résultat")
    date_exam = fields.Date(related="partner_id.mcm_session_id.date_exam", string="Date Examen")
    active = fields.Boolean('Active', default=True)
    module_ids = fields.One2many('mcmacademy.module', 'info_examen_id')
    date_today = fields.Date(string="Date d'envoi de relevée de note: ", default=datetime.today())
    company_id = fields.Many2one(
        'res.company', string='Company', change_default=True,
        default=lambda self: self.env.company,
        required=False, readonly=False)
    nombre_de_passage = fields.Selection(selection=[
        ('premier', 'premier'),
        ('deuxieme', 'deuxième'),
        ('troisieme', 'troisième')],
        string="Nombre De Passage", default="premier")

    presence = fields.Selection(selection=[
        ('present', 'Présent'),
        ('Absent', 'Absent')],
        string="Présence", default="present")

    def action_get_attachment(self):
        """ this method called from button action in view xml """
        pdf = self.env.ref('partner_exam.report_id').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        # save pdf as attachment
        name = self.partner_id.name
        return self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            'datas': b64_pdf,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })

    def action_send_email(self):
        '''
        This function opens a window to compose an email, with the emai template message loaded by default
        '''

        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
                ir_model_data.get_object_reference('partner_exam', 'email_template_edi_invoice_id')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'info.examen',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }

        lang = self.env.context.get('lang')
        if {'default_template_id', 'default_model', 'default_res_id'} <= ctx.keys():
            template = self.env['mail.template'].browse(ctx['default_template_id'])
            if template and template.lang:
                lang = template._render_template(template.lang, ctx['default_model'], ctx['default_res_id'])

        self = self.with_context(lang=lang)

        # for record in records:
        #     attachment = self.env['ir.attachment'].create( \
        #         {'name': 'Tax Exemption',
        #          'type': 'binary',
        #          'datas': record.x_tax_exemption,
        #          'res_model': 'crm.lead',
        #          'res_id': record.id, })

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.onchange('epreuve_a', 'epreuve_b', 'moyenne_generale')
    def _compute_moyenne_generale(self):
        """ This function used to auto display some result
        like the "Moyenne Generale" & "Mention" & "Resultat" """
        for rec in self:
            rec.moyenne_generale = (rec.epreuve_a + rec.epreuve_b) / 2
            if rec.epreuve_a >= 10 and rec.epreuve_b >= 8 and rec.moyenne_generale >= 12:
                rec.mention = 'recu'
                rec.resultat = 'recu'
            else:
                rec.mention = 'ajourne'
                rec.resultat = 'ajourne'
                """ This code commented, if we need optimisation for presence field """
            #     rec.mention = 'ajourne'
            #     rec.resultat = 'ajourne'

    @api.onchange('epreuve_a', 'epreuve_b', 'moyenne_generale', 'presence')
    def _raise_error(self):
        if self.epreuve_a < 1 and self.epreuve_b < 1 and self.moyenne_generale < 1 and self.presence in 'present':
            raise ValidationError(
                _("Vérifier les constraintes, les notes sont inferieur à 1 mais il est présent!!'"))
        if self.epreuve_a > 1 and self.epreuve_b > 1 and self.moyenne_generale > 1 and self.presence in 'Absent':
            raise ValidationError(
                _("Vérifier les constraintes, les notes sont supperieur à 1 mais il est absent!!'"))


