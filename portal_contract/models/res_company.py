# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class resComapny(models.Model):
    _inherit = "res.company"

    mcm_responsable_id=fields.Many2one('res.partner','Responsable')

    @api.model
    def action_open_sale_onboarding_sample_quotation(self):
        action=super(resComapny,self).action_open_sale_onboarding_sample_quotation()
        """ Onboarding step for sending a sample quotation. Open a window to compose an email,
            with the edi_invoice_template message loaded by default. """
        sample_sales_order = self._get_sample_sales_order()
        template = self.env.ref('portal_contract.mcm_email_template_edi_sale', False)
        action = self.env.ref('sale.action_open_sale_onboarding_sample_quotation').read()[0]
        action['context'] = {
            'default_res_id': sample_sales_order.id,
            'default_use_template': bool(template),
            'default_template_id': template and template.id or False,
            'default_model': 'sale.order',
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': 'mail.mail_notification_paynow',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'mail_notify_author': True,
        }
        return action