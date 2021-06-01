# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models, _
import logging
from odoo.addons.seo_url_redirect.models.model import Models

_logger = logging.getLogger(__name__)

class ProductTemplate(Models):

    _inherit = "product.template"

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_product', res)
        return res

    def write(self, vals):
        for proObj in self:
            if vals.get('url_key'):
                vals = self.env['website.rewrite'].createRedirectForRewrite(vals, proObj, 'product.template', 'pattern_category')
        res = super(ProductTemplate, self).write(vals)
        return res

    def update_seo_url(self):
        productIds = self._context.get('active_ids')
        productObjs = self.search([('id', 'in', productIds)])
        resp = self.env['website.rewrite'].setSeoUrlKey('pattern_product', productObjs)
        text = "SEO Url key of {} product(s) have been successfully updated.".format(len(productObjs))
        if resp:
            failedIds = ", ".join(resp)
            updatedProducts = len(productObjs) - len(resp)
            text = "Products with internal reference [{}] are failed to update. Reason : SEO URL Key must be unique!".format(failedIds)
            if updatedProducts:
                text = "SEO Url key of {} product(s) have been successfully updated and products with internal reference [{}] are failed to update. Reason : SEO URL Key must be unique!".format(updatedProducts, failedIds)
        return self.env['wk.wizard.message'].genrated_message(text)


    def open_website_url(self):
        res = super(ProductTemplate, self).open_website_url()
        website_id = self.env["website"].get_current_website()

        if website_id.use_server_rewrites and res.get("url"):
            url = self.url_key
            if website_id.use_suffix:
                url += website_id.suffix_product
            res.update({"url": url})
        return res

    def _compute_website_url(self):
        website_id = self.env["website"].get_current_website()
        super(ProductTemplate, self)._compute_website_url()
        for product in self:
            url = product.url_key
            if website_id.use_suffix:
                url += website_id.suffix_product
            product.website_url = '/shop/product/%s'%url
