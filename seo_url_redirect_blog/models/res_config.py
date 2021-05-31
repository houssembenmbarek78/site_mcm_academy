# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   If not, see <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import api, fields, models, _

class WebsiteSeoRewriteSettings(models.TransientModel):
    _inherit = 'website.seo.rewrite.settings'

    suffix_blog = fields.Char(string="Suffix in Blog URL", related="website_id.suffix_blog", readonly=False)
    suffix_post = fields.Char(string="Suffix in Post URL", related="website_id.suffix_post", readonly=False)
    pattern_blog = fields.Char(string="Pattern for Blog URL Key", related="website_id.pattern_blog", readonly=False)
    pattern_post = fields.Char(string="Pattern for Blog Post URL Key", related="website_id.pattern_post", readonly=False)

