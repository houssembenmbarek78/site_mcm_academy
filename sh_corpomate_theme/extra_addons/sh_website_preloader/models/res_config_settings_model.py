# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class website(models.Model):
    _inherit = 'website'

    sh_is_website_preloader = fields.Boolean(string="Website Preloader")
    sh_back_color = fields.Char(string="Background Color", help="Choose background color", size=7)
    sh_progressbar_color = fields.Char(string="Progressbar Color", help="Choose progressbar color", size=7)

    sh_style = fields.Selection([
        ('ball-pulse', 'Ball Pulse'),
        ('ball-grid-pulse', 'Ball Grid Pulse'),
        ('ball-clip-rotate', 'Ball Clip Rotate'),
        ('ball-clip-rotate-pulse', 'Ball Clip Rotate Pulse'),
        ('square-spin', 'Square Spin'),
        ('ball-clip-rotate-multiple', 'Ball Clip Rotate Multiple'),
        ('ball-pulse-rise', 'Ball Pulse Rise'),
        ('ball-rotate', 'Ball Rotate'),
        ('cube-transition', 'Cube Transition'),
        ('ball-zig-zag', 'Ball Zig Zag'),
        ('ball-zig-zag-deflect', 'Ball Zig Zag Deflect'),
        ('ball-triangle-path', 'Ball Triangle Path'),
        ('ball-scale', 'Ball Scale'),
        ('line-scale', 'Line Scale'),
        ('line-scale-party', 'Line Scale Party'),
        ('ball-scale-multiple', 'Ball Scale Multiple'),
        ('ball-pulse-sync', 'Ball Pulse Sync'),
        ('ball-beat', 'Ball Beat'),
        ('line-scale-pulse-out', 'Line Scale Pulse Out'),
        ('line-scale-pulse-out-rapid', 'Line Scale Pulse Out Rapid'),
        ('ball-scale-ripple', 'Ball Scale Ripple'),
        ('ball-scale-ripple-multiple', 'Ball Scale Ripple Multiple'),
        ('ball-spin-fade-loader', 'Ball Spin Fade Loader'),
        ('line-spin-fade-loader', 'Line Spin Fade Loader'),
        ('triangle-skew-spin', 'Triangle Skew Spin'),
        ('pacman', 'Pacman'),
        ('semi-circle-spin', 'Semi Circle Spin'),
        ('ball-grid-beat', 'Ball Grid Beat'),
        ('ball-scale-random', 'Ball Scale Random')
        
        ], string="Style", default='ball-pulse')


class res_config_settings(models.TransientModel):
    _inherit = "res.config.settings"
    
    sh_is_website_preloader = fields.Boolean(related="website_id.sh_is_website_preloader", string="Website Preloader", readonly=False)
    sh_back_color = fields.Char(related="website_id.sh_back_color", string="Background Color", help="Choose background color", size=7, readonly=False)
    sh_progressbar_color = fields.Char(related="website_id.sh_progressbar_color", string="Progressbar Color", help="Choose progressbar color", size=7, readonly=False)
    
    sh_style = fields.Selection([
        ('ball-pulse', 'Ball Pulse'),
        ('ball-grid-pulse', 'Ball Grid Pulse'),
        ('ball-clip-rotate', 'Ball Clip Rotate'),
        ('ball-clip-rotate-pulse', 'Ball Clip Rotate Pulse'),
        ('square-spin', 'Square Spin'),
        ('ball-clip-rotate-multiple', 'Ball Clip Rotate Multiple'),
        ('ball-pulse-rise', 'Ball Pulse Rise'),
        ('ball-rotate', 'Ball Rotate'),
        ('cube-transition', 'Cube Transition'),
        ('ball-zig-zag', 'Ball Zig Zag'),
        ('ball-zig-zag-deflect', 'Ball Zig Zag Deflect'),
        ('ball-triangle-path', 'Ball Triangle Path'),
        ('ball-scale', 'Ball Scale'),
        ('line-scale', 'Line Scale'),
        ('line-scale-party', 'Line Scale Party'),
        ('ball-scale-multiple', 'Ball Scale Multiple'),
        ('ball-pulse-sync', 'Ball Pulse Sync'),
        ('ball-beat', 'Ball Beat'),
        ('line-scale-pulse-out', 'Line Scale Pulse Out'),
        ('line-scale-pulse-out-rapid', 'Line Scale Pulse Out Rapid'),
        ('ball-scale-ripple', 'Ball Scale Ripple'),
        ('ball-scale-ripple-multiple', 'Ball Scale Ripple Multiple'),
        ('ball-spin-fade-loader', 'Ball Spin Fade Loader'),
        ('line-spin-fade-loader', 'Line Spin Fade Loader'),
        ('triangle-skew-spin', 'Triangle Skew Spin'),
        ('pacman', 'Pacman'),
        ('semi-circle-spin', 'Semi Circle Spin'),
        ('ball-grid-beat', 'Ball Grid Beat'),
        ('ball-scale-random', 'Ball Scale Random')

        ], string="Style", default='ball-pulse', related="website_id.sh_style", readonly=False)
    
