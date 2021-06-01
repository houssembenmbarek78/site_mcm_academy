# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, models, _
from odoo.addons.seo_url_redirect.models.model import Models

class ProductPublicCategory(Models):

    _inherit = "product.public.category"

    @api.model
    def create(self, vals):
        res = super(ProductPublicCategory, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_category', res)
        return res

    def write(self, vals):
        for catObj in self:
            vals = self.env['website.rewrite'].createRedirectForRewrite(vals, catObj, 'product.public.category', 'pattern_category')
        res = super(ProductPublicCategory, self).write(vals)
        return res

    def update_seo_url(self):
        categoryIds = self._context.get('active_ids')
        categoryObjs = self.search([('id', 'in', categoryIds)])
        self.env['website.rewrite'].setSeoUrlKey('pattern_category', categoryObjs)
        text = "SEO Url key of {} category(s) have been successfully updated.".format(len(categoryObjs))
        return self.env['wk.wizard.message'].genrated_message(text)
