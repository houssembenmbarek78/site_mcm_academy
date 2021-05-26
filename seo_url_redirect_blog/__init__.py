#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from . import models
from odoo import api, SUPERUSER_ID

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import Warning
    version_info = common.exp_version()
    server_serie =version_info.get('server_serie')
    if server_serie!='13.0':raise Warning('Module support Odoo series 13.0 found {}.'.format(server_serie))

def _update_blog_seo_url(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    try:
        blogBlogObjs = env['blog.blog'].search([])
        env['website.rewrite'].setSeoUrlKey('pattern_blog', blogBlogObjs)
        blogPostObjs = env['blog.post'].search([])
        env['website.rewrite'].setSeoUrlKey('pattern_post', blogPostObjs)
    except Exception as e:
        pass
