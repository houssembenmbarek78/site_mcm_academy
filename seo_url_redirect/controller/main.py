import logging

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.seo_url_redirect.models.ir_http import slug
from odoo.http import route, request
from odoo import _

_logger = logging.getLogger(__name__)

class Website_Sale(WebsiteSale):

    @route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        result = super(Website_Sale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        qcontext = result.qcontext
        url = "/shop"

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if category:
                url = "/shop/category/%s" % slug(category)

        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        if qcontext.get("search_count"):
            pager = request.website.pager(url=url, total=qcontext.get("search_count"), page=page, step=ppg, scope=7, url_args=post)
            result.qcontext.update(pager=pager)

        return result

    @route()
    def add_product(self, name=None, category=None, **post):
        # result = super(Website_Sale, self).add_product(name=name, category=category, **post)
        product = request.env['product.product'].create({
            'name': name or _("New Product"),
            'public_categ_ids': category,
            'website_id': request.website.id,
        })
        return "%s?enable_editor=1" % slug(product.product_tmpl_id)
