# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.http import request

from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.tools import ustr
class Slider(models.Model):
    _name = "sh.emate.slider"
    _description = "Slider"
    
    name = fields.Char(string = "Name", required = True)
    slider_type = fields.Selection([
        ('product','Product'),
        ('blog','Blog'),    
        ('event','Event'),            
        ],default = "product", string = "Config For", required = True)
    
    filter_type = fields.Selection([
        ('domain','Domain'),
        ('manual','Manually')
        ],default = "manual", string = "Filter Type", required = True)


                       
    product_filter_id = fields.Many2one(comodel_name="ir.filters", string = "Product Filter", domain='[("model_id","=","product.template" )]' )
    product_ids = fields.Many2many(comodel_name='product.template', 
                                   relation='sh_emate_slider_product_rel',
                                   domain='[("sale_ok", "=", True),("website_published","=",True)]',                                   
                                   string='Products')      
 


    blog_post_filter_id = fields.Many2one(comodel_name="ir.filters", string = "Blog Post Filter", domain='[("model_id","=","blog.post" )]') 
    blog_post_ids = fields.Many2many(comodel_name="blog.post", string = "Blog Posts")
    



    event_filter_id = fields.Many2one(comodel_name="ir.filters", string = "Event Filter", domain='[("model_id","=","event.event" )]') 
    event_ids = fields.Many2many(comodel_name="event.event", string = "Events")
    
    
    
    limit = fields.Integer(string = "Limit", default = 3)


    pricelist_id = fields.Many2one(comodel_name="product.pricelist", string = "Pricelist")



    def get_data(self,is_show_product_desc,is_show_sale_price,tmpl_item_name):
        
        
        if not tmpl_item_name:
            raise UserError(_('Programming Error: In order to render dynamic snippet you must define template item'))
                        
        products = self.env["product.template"]        
        blog_posts = self.env["blog.post"] 
        events = self.env["event.event"] 
        pricelist_currency_id = self.env.user.company_id.currency_id        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
       

        sort = []
        limit = None
        output = b'''
  <div class="js_cls_sh_mail_snippet_general">  
  
  </div>        
        
        '''  
     
        if self.limit > 0:
            limit = self.limit
                                     
        if self.slider_type == 'product':
            domain = [
                ("sale_ok", "=", True)
            ]

            if self.filter_type == 'manual':  
                if self.product_ids:
                    products = self.product_ids
                    
                    
            elif self.filter_type == 'domain':                    
                if self.product_filter_id.sudo():
                    domain += safe_eval(self.product_filter_id.sudo().domain)                     
                    sort = safe_eval(self.product_filter_id.sudo().sort) 
                           
                    # TODO: remove limit or make dynamic when done.
                    products = products.search(domain,order = sort, limit = limit)
                                    
            dic_products = {}
            if products:
                # if selected price list
                if self.pricelist_id:
                    pricelist_currency_id = self.pricelist_id.currency_id
                                
                for product in products:
                    price = product.list_price
                    price_unit = False
                    if self.pricelist_id:
                        price_unit = self.pricelist_id._compute_price_rule(
                            [(product, 1, self.env.user.partner_id)], date=fields.Date.context_today(self) , uom_id=product.uom_id.id)
                    if price_unit:
                        res_tuple = price_unit.get(product.id)
                        price = res_tuple[0]
                                             
                    dic_products.update({
                        product.id : price
                        })   
                                
            try:
                template_id = "sh_emate." + tmpl_item_name
                output = self.env["ir.ui.view"].render_template(template_id, values={
                    'products': products,    
                    'dic_products':dic_products,                      
                    'is_show_product_desc':is_show_product_desc,
                    'is_show_sale_price':is_show_sale_price,
                    'currency_id': self.env.user.company_id.currency_id,
                    'pricelist_currency_id':pricelist_currency_id,
                    'base_url':base_url
                })
            except Exception as e:
                raise UserError(_('%s') % ( ustr(e) ))               
            
        elif self.slider_type == 'blog':
            
            domain = [
                ('website_published', '=', True),  
            ]            
            
            if self.filter_type == 'manual':  
                if self.blog_post_ids:
                    blog_posts = self.blog_post_ids
                    
                    
            elif self.filter_type == 'domain':                    
                if self.blog_post_filter_id.sudo():
                    domain += safe_eval(self.blog_post_filter_id.sudo().domain)                     
                    sort = safe_eval(self.blog_post_filter_id.sudo().sort) 
                           
                    # TODO: remove limit or make dynamic when done.
                    blog_posts = blog_posts.search(domain,order = sort, limit = limit)
                                    


            dic_blog_posts = {}
            for blog_post in blog_posts:
                cover_properties = safe_eval(blog_post.cover_properties or {})
                
                image_url = cover_properties.get("background-image",False)
                if image_url:
                    first_part_url = "url('"
                    last_part_url = image_url[5:]
                    last_part_url = base_url + last_part_url
                    cover_properties.update({
                        "background-image": first_part_url + last_part_url
                        })
                    
                dic_blog_posts.update({
                    blog_post.id : cover_properties
                    })
                
                            
            try:                                    
                template_id = "sh_emate." + tmpl_item_name
                output = self.env["ir.ui.view"].render_template(template_id, values={
                    'blog_posts': blog_posts,
                    'dic_blog_posts':dic_blog_posts,
                    'base_url':base_url                
                }) 
            except Exception as e:
                raise UserError(_('%s') % ( ustr(e) ))  
                        
            
            
            
        elif self.slider_type == 'event':
            
            domain = [
                ('website_published', '=', True),  
            ]            
            
            if self.filter_type == 'manual':  
                if self.event_ids:
                    events = self.event_ids
                    
                    
            elif self.filter_type == 'domain':                    
                if self.event_filter_id.sudo():
                    domain += safe_eval(self.event_filter_id.sudo().domain)                     
                    sort = safe_eval(self.event_filter_id.sudo().sort) 
                           
                    # TODO: remove limit or make dynamic when done.
                    events = events.search(domain,order = sort, limit = limit)
                                    
            dic_events = {}
            for event in events:
                cover_properties = safe_eval(event.cover_properties or {})
                
                
                image_url = cover_properties.get("background-image",False)
                if image_url != 'none':
                    
                    first_part_url = "url('"
                    last_part_url = image_url[5:]
                    last_part_url = base_url + last_part_url
                    cover_properties.update({
                        "background-image": first_part_url + last_part_url
                        })
                    
                dic_events.update({
                    event.id : cover_properties
                    })
                
                
            try:            
                template_id = "sh_emate." + tmpl_item_name
                output = self.env["ir.ui.view"].render_template(template_id, values={
                    'events': events,
                    'dic_events':dic_events,
                    'base_url':base_url                
                })              
            except Exception as e:
                raise UserError(_('%s') % ( ustr(e) ))
                        
         
        output = output.decode("utf-8")    

        return output
         
        

        
    