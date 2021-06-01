# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

from odoo import api, fields, _
from odoo.addons.seo_url_redirect.models.model import Models

class Blog(Models):

    _inherit = 'blog.blog'

    @api.model
    def create(self, vals):
        res = super(Blog, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_blog', res)
        return res


    def write(self, vals):
        for blogObj in self:
            vals = self.env['website.rewrite'].createRedirectForRewrite(vals, blogObj, 'blog.blog', 'pattern_blog')
        res = super(Blog, self).write(vals)
        return res

    def update_seo_url(self):
        blogIds = self._context.get('active_ids')
        blogObjs = self.search([('id', 'in', blogIds)])
        self.env['website.rewrite'].setSeoUrlKey('pattern_blog', blogObjs)
        text = "SEO Url key of {} blog(s) have been successfully updated.".format(len(blogObjs))
        return self.env['wk.wizard.message'].genrated_message(text)

class BlogPost(Models):
    
    _inherit = 'blog.post'

    @api.model
    def create(self, vals):
        res = super(BlogPost, self).create(vals)
        if res.url_key in ['', False, None]:
            self.env['website.rewrite'].setSeoUrlKey('pattern_post', res)
        return res

    def write(self, vals):
        for blogPostObj in self:
            vals = self.env['website.rewrite'].createRedirectForRewrite(vals, blogPostObj, 'blog.post', 'pattern_post')
        res = super(BlogPost, self).write(vals)
        return res

    def update_seo_url(self):
        blogPostIds = self._context.get('active_ids')
        blogPostObjs = self.search([('id', 'in', blogPostIds)])
        self.env['website.rewrite'].setSeoUrlKey('pattern_post', blogPostObjs)
        text = "SEO Url key of {} blog post(s) have been successfully updated.".format(len(blogPostObjs))
        return self.env['wk.wizard.message'].genrated_message(text)
