# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,SUPERUSER_ID
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self,values):
        order=super(SaleOrder,self).write(values)
        if 'signed_by' in values and 'signed_on' in values and 'signature' in values and self.state != 'cancel' and self.state != 'draft' and self.company_id.id==1:
            if self.env.su:
                # sending mail in sudo was meant for it being sent from superuser
                self = self.with_user(SUPERUSER_ID)
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('contract_send_documents.mail_template_client_info_document'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id(
                    'contract_send_documents.mail_template_client_info_document', raise_if_not_found=False)
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('contract_send_documents.mail_template_client_info_document',
                                                                        raise_if_not_found=False)
            if template_id:
                for order in self:
                    order.with_context(force_send=True).message_post_with_template(template_id,
                                                                                   composition_mode='comment',
                                                                                   email_layout_xmlid="contract_send_documents.portal_contract_document_mail")
            subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mt_note')
            message = self.env['mail.message'].sudo().create({
                'subject': 'Contrat signé',
                'model': 'res.partner',
                'res_id': self.partner_id.id,
                'message_type': 'notification',
                'subtype_id': subtype_id,
                'body': 'Contrat signé par ' + str(values['signed_by']),
            })
        if 'signed_by' in values and 'signed_on' in values and 'signature' in values and self.state != 'cancel' and self.state != 'draft' and self.company_id.id==2:
            if self.env.su:
                # sending mail in sudo was meant for it being sent from superuser
                self = self.with_user(SUPERUSER_ID)
            template_id = int(self.env['ir.config_parameter'].sudo().get_param('contract_send_documents.mail_template_client_info_document_digimoov'))
            template_id = self.env['mail.template'].search([('id', '=', template_id)]).id
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id(
                    'contract_send_documents.mail_template_client_info_document_digimoov', raise_if_not_found=False)
                if template_id:
                    template = self.env['mail.template'].search([('id', '=', template_id)])
                    template.attachment_ids = False
                    attachment = self.env['ir.attachment'].search(
                        [("name", "=", "cerfa_11414-05.pdf"), ("description", "=", "cerfa_mail_template_attachment")],limit=1)
                    if attachment:
                        template.sudo().write({'attachment_ids': [(6, 0, attachment.ids)]})
            if not template_id:
                template_id = self.env['ir.model.data'].xmlid_to_res_id('contract_send_documents.mail_template_client_info_document_digimoov',
                                                                        raise_if_not_found=False)
            if template_id:
                for order in self:
                    order.with_context(force_send=True).message_post_with_template(template_id,
                                                                                   composition_mode='comment',
                                                                                   email_layout_xmlid="contract_send_documents.portal_contract_document_mail")
            subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mt_note')
            attachments = self.env['ir.attachment'].search(
                [("name", "=", "cerfa_11414-05.pdf"), ("description", "=", "cerfa_mail_template_attachment"),
                 ('res_model', "=", "sale.order")])
            for attachment in attachments:
                attachment.sudo().unlink()
            message = self.env['mail.message'].sudo().create({
                'subject': 'Contrat signé',
                'model': 'res.partner',
                'res_id': self.partner_id.id,
                'message_type': 'notification',
                'subtype_id': subtype_id,
                'body': 'Contrat signé par ' + str(values['signed_by']),
            })
        return order