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
    _inherit = 'res.config.settings'
    _name = 'website.seo.rewrite.settings'
    _description = "website seo rewrite settings"

    use_suffix = fields.Boolean(string="Use Suffix in URL", related="website_id.use_suffix", readonly=False)
    suffix_product = fields.Char(string="Suffix in Product URL", related="website_id.suffix_product", readonly=False)
    suffix_category = fields.Char(string="Suffix in Category URL", related="website_id.suffix_category", readonly=False)
    pattern_product = fields.Char(string="Pattern for Product URL Key", related="website_id.pattern_product", readonly=False)
    pattern_category = fields.Char(string="Pattern for Category URL Key", related="website_id.pattern_category", readonly=False)
    use_category_url = fields.Boolean(string="Use Category URL on Product", help="""Enable to append category along with product URL in Website""", related="website_id.use_category_url", readonly=False)
    use_category_hierarchy = fields.Boolean(string="Use Category hierarchy", help="""Enable to manage category hierarchy option in Website""", related="website_id.use_category_hierarchy", readonly=False)
    use_server_rewrites = fields.Boolean(
            string="Use Web Server Rewrites",
            help="""
            By enabling this feature page key will remove from url
            For Example :
            '/shop/product/catalog-product' => '/catalog-product'
            '/blog/my-blog/post/my-blog-first-post' => '/my-blog-first-post'
            """,
            related="website_id.use_server_rewrites", readonly=False
        )
