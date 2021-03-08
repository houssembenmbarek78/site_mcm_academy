 # -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_

class event_event(models.Model):
    _inherit = "event.event"
    
    sh_emate_short_description = fields.Text(string = "Short Description (Emate)")
  
    