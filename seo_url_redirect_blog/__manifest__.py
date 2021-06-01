# -*- coding: utf-8 -*-
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
{
  "name"                 :  "SEO-URL Redirect/Rewrite For Blog",
  "summary"              :  """SEO-URL Redirect/Rewrite For Event  provides redirect URL feature to your Odoo website Blogs.""",
  "category"             :  "Website",
  "version"              :  "1.7",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-SEO-URL-Redirect-Rewrite-For-Blog.html",
  "description"          :  """SEO
                            Search Engine Optimization
                            URL
                            SEO URL
                            Redirect/Rewrite
                            Rewrite
                            Redirect
                            SEO-URL Redirect/Rewrite
                            Odoo SEO-URL Redirect/Rewrite
                            URL Redirect/Rewrite
                            URL Rewrite
                            URL Redirect
                            SEO-URL Redirect/Rewrite For Event
                            SEO-URL Redirect/Rewrite For Blog
                            Odoo SEO-URL Redirect/Rewrite For Event
                            Odoo SEO-URL Redirect/Rewrite For Blog
                            Rewrite For Blog
                            Redirect For Blog
                            URL Rewrite For Blog
                            URL Rewrite for Blog""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=seo_url_redirect_blog",
  "depends"              :  [
                             'website_blog',
                             'seo_url_redirect',
                            ],
  "data"                 :  [
                             'views/website_blog_views.xml',
                             'views/rewrite_view.xml',
                             'views/rewrite_menu.xml',
                             'views/res_config_views.xml',
                             'data/seo_server_actions.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
  "post_init_hook"       :  "_update_blog_seo_url",
}
