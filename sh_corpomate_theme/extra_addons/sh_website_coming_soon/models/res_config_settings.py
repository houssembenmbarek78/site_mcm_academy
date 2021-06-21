# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import fields, models
from odoo.tools.translate import html_translate


class Website(models.Model):
    _inherit = "website"

    sh_website_coming_soon_is_coming_soon = fields.Boolean(
        string="Website Coming Soon")

    sh_website_coming_soon_title = fields.Char(
        string="Title",
        default="Coming Soon",
        translate=True)

    sh_website_coming_soon_desc = fields.Html(
        string="Description",
        translate=html_translate
    )

    sh_website_coming_soon_bg_img = fields.Binary(
        string="Background Image",
    )

    sh_website_coming_soon_launch_date = fields.Datetime(
        string="Launch Date",
    )

    sh_website_coming_soon_style = fields.Selection([
        ("tmpl_1", "Style 1"),
        ("tmpl_2", "Style 2"),
        ("tmpl_3", "Style 3"),
        ("tmpl_4", "Style 4"),
        ("tmpl_5", "Style 5"),
        ("tmpl_6", "Style 6"),
        ("tmpl_7", "Style 7"),
        ("tmpl_8", "Style 8"),
        ("tmpl_9", "Style 9"),
        ("tmpl_10", "Style 10"),
        ("tmpl_11", "Style 11"),
        ("tmpl_12", "Style 12"),
        ("tmpl_13", "Style 13"),
        ("tmpl_14", "Style 14"),
        ("tmpl_15", "Style 15"),
        ("tmpl_16", "Style 16"),
        ("tmpl_17", "Style 17"),
        ("tmpl_18", "Style 18"),
        ("tmpl_19", "Style 19"),
        ("tmpl_20", "Style 20"),
        ("tmpl_21", "Style 21"),
        ("tmpl_22", "Style 22"),
        ("tmpl_23", "Style 23"),
        ("tmpl_24", "Style 24"),
        ("tmpl_25", "Style 25"),
        ("tmpl_26", "Style 26"),
        ("tmpl_27", "Style 27"),
        ("tmpl_28", "Style 28"),
        ("tmpl_29", "Style 29"),
        ("tmpl_30", "Style 30"),

    ], string="Style", default="tmpl_1")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sh_website_coming_soon_is_coming_soon = fields.Boolean(
        string="Website Coming Soon",
        related="website_id.sh_website_coming_soon_is_coming_soon",
        readonly=False)

    sh_website_coming_soon_title = fields.Char(
        string="Title",
        related="website_id.sh_website_coming_soon_title",
        translate=True,
        readonly=False)

    sh_website_coming_soon_desc = fields.Html(
        string="Description",
        related="website_id.sh_website_coming_soon_desc",
        translate=html_translate,
        readonly=False)

    sh_website_coming_soon_bg_img = fields.Binary(
        string="Background Image",
        related="website_id.sh_website_coming_soon_bg_img",
        readonly=False)

    sh_website_coming_soon_launch_date = fields.Datetime(
        string="Launch Date",
        related="website_id.sh_website_coming_soon_launch_date",
        readonly=False)

    sh_website_coming_soon_style = fields.Selection(
        string="Style",
        related="website_id.sh_website_coming_soon_style",
        readonly=False)
