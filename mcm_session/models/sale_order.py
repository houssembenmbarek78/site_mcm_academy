# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"


    session_id=fields.Many2one('mcmacademy.session',required=False)
    module_id=fields.Many2one('mcmacademy.module',required=False)
    conditions =fields.Boolean(default=False)
    failures = fields.Boolean(default=False)
    accompagnement = fields.Boolean(default=False)

    def action_link_contract(self):
        orders = self.env['sale.order'].sudo().search([])
        for order in orders:
            if len(order.partner_id.sale_order_ids)==1:
                order.module_id=order.partner_id.module_id
                if not order.session_id:
                    order.session_id=order.partner_id.mcm_session_id
                product=False
                for line in order.order_line:
                    product=line.product_id.product_tmpl_id
                if product:
                    module_id = self.env['mcmacademy.module'].sudo().search(
                        [('product_id', '=', product.id), ('session_id', '=', order.session_id.id)])
                    if module_id:
                            for module in module_id:
                                if order.partner_id.module_id==module:
                                    order.module_id=module
        return True
    def _create_payment_transaction(self, vals):
        '''Similar to self.env['payment.transaction'].create(vals) but the values are filled with the
        current sales orders fields (e.g. the partner or the currency).
        :param vals: The values to create a new payment.transaction.
        :return: The newly created payment.transaction record.
        '''
        # Ensure the currencies are the same.
        currency = self[0].pricelist_id.currency_id
        if any([so.pricelist_id.currency_id != currency for so in self]):
            raise ValidationError(_('A transaction can\'t be linked to sales orders having different currencies.'))

        # Ensure the partner are the same.
        partner = self[0].partner_id
        if any([so.partner_id != partner for so in self]):
            raise ValidationError(_('A transaction can\'t be linked to sales orders having different partners.'))

        # Try to retrieve the acquirer. However, fallback to the token's acquirer.
        acquirer_id = vals.get('acquirer_id')
        payment_token_id = vals.get('payment_token_id')
        acquirer=False
        if payment_token_id:
            payment_token = self.env['payment.token'].sudo().browse(payment_token_id)

            # Check payment_token/acquirer matching or take the acquirer from token

            if acquirer_id:
                acquirer = self.env['payment.acquirer'].browse(acquirer_id)
                if payment_token and payment_token.acquirer_id != acquirer:
                    raise ValidationError(_('Invalid token found! Token acquirer %s != %s') % (
                        payment_token.acquirer_id.name, acquirer.name))
                if payment_token and payment_token.partner_id != partner:
                    raise ValidationError(_('Invalid token found! Token partner %s != %s') % (
                        payment_token.partner.name, partner.name))
            else:
                acquirer = payment_token.acquirer_id

        # Check an acquirer is there.
        if not acquirer_id and not acquirer:
            raise ValidationError(_('A payment acquirer is required to create a transaction.'))

        if not acquirer:
            acquirer = self.env['payment.acquirer'].browse(acquirer_id)

        # Check a journal is set on acquirer.
        if not acquirer.journal_id:
            raise ValidationError(_('A journal must be specified of the acquirer %s.' % acquirer.name))

        if not acquirer_id and acquirer:
            vals['acquirer_id'] = acquirer.id
        amount = sum(self.mapped('amount_total'))
        if self.instalment and amount>1000 and self.company_id.id==1:
            amount=amount/3
        print('_create_payment_transaction')
        print(self.instalment)
        print(self.company_id.id)
        if self.instalment and self.company_id.id==2:
            amount=amount/int(self.instalment_number)
        vals.update({
            'amount': amount,
            'currency_id': currency.id,
            'partner_id': partner.id,
            'sale_order_ids': [(6, 0, self.ids)],
        })
        transaction = self.env['payment.transaction'].create(vals)


        # Process directly if payment_token
        if transaction.payment_token_id:
            transaction.s2s_do_transaction()

        return transaction