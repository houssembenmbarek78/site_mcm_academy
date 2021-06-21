# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields

class sh_nb_notice_board(models.Model):
    _name = 'sh.nb.notice.board'
    _description = 'Notice board for display news on website'
    _order = 'id desc'    

    name = fields.Char('Title', required=True)
    desc = fields.Text('Description')
    active = fields.Boolean(string = 'Active', default=True)    
    
