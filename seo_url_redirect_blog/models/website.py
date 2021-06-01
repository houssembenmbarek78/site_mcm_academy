# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   If not, see <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import api, models, fields, _
from odoo.http import request
import logging

_log = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = "website"

    suffix_blog = fields.Char(string="Suffix in Blog URL", default=".html")
    suffix_post = fields.Char(string="Suffix in Post URL", default=".html")
    pattern_blog = fields.Char(string="Pattern for Blog URL Key", default="display_name")
    pattern_post = fields.Char(string="Pattern for Blog Post URL Key", default="display_name")


class WebsiteRedirect(models.Model):
    _inherit = "website.rewrite"

    @api.model
    def _get_rewrites(self):
        res = super(WebsiteRedirect, self)._get_rewrites()
        res.append(('blog.blog', 'Blog'))
        res.append(('blog.post', 'Blog Post'))
        return res

    def getSuffix(self, modelname):
        suffix = super(WebsiteRedirect, self).getSuffix(modelname)
        website_id = request.env['website'].get_current_website()
        if modelname == 'blog.post':
            suffix = website_id.suffix_post
        if modelname == 'blog.blog':
            suffix = website_id.suffix_blog
        return suffix

    def unsetUrlSuffix(self, value):
        value = super(WebsiteRedirect, self).unsetUrlSuffix(value)
        website_id = request.env['website'].get_current_website()
        suffix = website_id.suffix_post
        if suffix:
            value = value.replace(suffix, '')
        suffix = website_id.suffix_blog
        if suffix:
            value = value.replace(suffix, '')
        return value

    def getSlugUrlKeyModel(self, value, model):
        model = super(WebsiteRedirect, self).getSlugUrlKeyModel(value, model)
        res = request.env['blog.post'].sudo().search([('url_key', '=', value)])
        if not res:
            res = request.env['blog.blog'].sudo().search([('url_key', '=', value)])
        if res:
            model = res._name
        return model
