# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _,tools
import logging
from lxml import etree
from lxml import etree as ElementTree
from odoo.addons.http_routing.models.ir_http import slugify
from odoo.exceptions import ValidationError
from odoo.tools.view_validation import valid_view

_logger = logging.getLogger(__name__)

from lxml import etree, html

class View(models.Model):
    _inherit = 'ir.ui.view'
    
    @api.model
    def sh_snippet_builder_snippet_save_view_values_hook(self):
        res = {}
        website_id = self.env.context.get('website_id')
        if website_id:
            res['website_id'] = website_id
        
        print("\n\n\n\n res ==>",res)
        return res

    

    @api.model
    def sh_snippet_builder_save_js_assets_snippet(self, name, arch, snippet_key):        
        arch = """<?xml version="1.0"?>
<data inherit_id="website.assets_frontend">
    <xpath expr="//script[last()]" position="after">

            %s

    </xpath>
</data>
        
        """ % arch or ''
              
        website_assets_frontend = self.env.ref("website.assets_frontend")
        # html to xml to add '/' at the end of self closing tags like br, ...
#         xml_arch = etree.tostring(html.fromstring(arch), encoding='utf-8')                
        new_snippet_view_values = {
            'name': name,
            'key': snippet_key,
            'type': 'qweb',
            'arch': arch,
            'inherit_id':website_assets_frontend.id,            
        }
        new_snippet_view_values.update(self.sh_snippet_builder_snippet_save_view_values_hook())
        view = self.search([('key', '=', snippet_key)], limit=1)
        if view:
            view.sudo().write({
                'arch':new_snippet_view_values['arch']
                })
        else:         
            view = self.create(new_snippet_view_values)       
        return view

    
    @api.model
    def sh_snippet_builder_save_snippet(self, name, arch, snippet_key):
        # html to xml to add '/' at the end of self closing tags like br, ...
        xml_arch = etree.tostring(html.fromstring(arch), encoding='utf-8')
        new_snippet_view_values = {
            'name': name,
            'key': snippet_key,
            'type': 'qweb',
            'arch': xml_arch,
        }
        new_snippet_view_values.update(self.sh_snippet_builder_snippet_save_view_values_hook())
        return self.create(new_snippet_view_values)
            
    
#     @api.constrains('arch_db')
#     def _check_xml(self):
#         # Sanity checks: the view should not break anything upon rendering!
#         # Any exception raised below will cause a transaction rollback.
#         for view in self:
#             if not view.arch:
#                 continue
#             try:
#                 view_arch = etree.fromstring(view.arch.encode('utf-8'))
#                 view._valid_inheritance(view_arch)
#                 view_def = view.read_combined(['arch'])
#                 view_arch_utf8 = view_def['arch']
#                 if view.type == 'qweb':
#                     continue
#                 view_doc = etree.fromstring(view_arch_utf8)
#                 # verify that all fields used are valid, etc.
#                 view.postprocess_and_fields(view_doc, validate=True)
#                 # RNG-based validation is not possible anymore with 7.0 forms
#                 view_docs = [view_doc]
#                 if view_docs[0].tag == 'data':
#                     # A <data> element is a wrapper for multiple root nodes
#                     view_docs = view_docs[0]
#                 for view_arch in view_docs:
#                     check = valid_view(view_arch, env=self.env, model=view.model)
#                     view_name = ('%s (%s)' % (view.name, view.xml_id)) if view.xml_id else view.name
#                     if not check:
#                         raise ValidationError(_(
#                             'Invalid view %(name)s definition in %(file)s',
#                             name=view_name, file=view.arch_fs
#                         ))
#                     if check == "Warning":
#                         _logger.warning('Invalid view %s definition in %s \n%s', view_name, view.arch_fs, view.arch)
#             except ValueError as e:
#                 raise ValidationError(_(
#                     "Error while validating view:\n\n%(error)s",
#                     error=tools.ustr(e),
#                 )).with_traceback(e.__traceback__) from None
#  
#         return True
#     
  
    
class sh_snippet_builder(models.Model):
    _name = "sh.snippet.builder"
    _description = "Snippet Builder"
    _order = "id desc"
    
    name = fields.Char(string = "Name", required = True)
    html = fields.Text(string = "HTML")
    css = fields.Text(string="CSS",default="<style></style>")
    js = fields.Text(string = "JS", default="<script></script>")
    view_id = fields.Many2one(string = "View", comodel_name="ir.ui.view")
    
    js_asset_view_id = fields.Many2one(string = "JS Assets View", comodel_name="ir.ui.view")
    
    def action_noupdate_tmpl(self):
        ir_model_data_obj = self.env['ir.model.data'].sudo()
                
        search_rec = ir_model_data_obj.sudo().search([
            ('module','=','sh_snippet_builder'),
            ('name','=','sh_snippet_builder_snippets'),            
            ], limit = 1)
            
        if search_rec:
            vals = {
            'noupdate'  : True,
                }
            search_rec.sudo().write(vals)
     
    @api.model
    def create(self,vals):
        global_js_view_arch = vals.get("js",'')
        res = super(sh_snippet_builder,self).create(vals)
#         vals.pop("js")           
        
        IrUiView = self.env["ir.ui.view"]    
        name = "sh_snippet_builder_ud_tmpl_" + str(res.id)
        key = "sh_snippet_builder." + name
        view_arch = """<?xml version="1.0"?>
        <t name="Snippet Builder %(id)s" t-name="sh_snippet_builder.sh_snippet_builder_ud_tmpl_%(id)s">
            <section class="sh_snippet_builder_section_user_defined">        
        """ % {
            'id' : res.id
            }
        if res.css:
            view_arch += res.css
        if res.html:
            view_arch += res.html        
        view_arch += """
            </section>
        </t>
        """
        view = IrUiView.sh_snippet_builder_save_snippet(res.name, view_arch, key)
        res.write({
            'view_id':view.id,
            })

        # =========================================================================           
        # Link custom snippet template in our website.snippets inherited template.
        # =========================================================================    
        snippet_panel_view = IrUiView.sudo().search([
            ('key','=','sh_corpomate_theme.sh_snippet_builder_snippets')
            ],order='id desc' ,limit=1)
        if snippet_panel_view and snippet_panel_view.arch:
            doc = etree.XML(snippet_panel_view.arch)
            for node in doc.xpath("//div[@class='o_panel_body']"):
                new_node = """
               <t t-snippet="%(key)s" 
               t-thumbnail="/sh_corpomate_theme/static/src/img/extra_addons/sh_snippet_builder/s_1.png"/> 
                """ %{
                    'key' : key
                    }
                new_node = ElementTree.fromstring( new_node )
                node.insert(1, new_node)
                break
            snippet_panel_view.arch = etree.tostring(doc, encoding='unicode')       
        # =========================================================================           
        # Link custom snippet template in our website.snippets inherited template.
        # =========================================================================           
        
        # -------------------------------------------
        # Make Assets template for JS
        # -------------------------------------------    
        if global_js_view_arch in ["<script></script>","<script/>"]:
            global_js_view_arch = "<script>      </script>"
                            
        name = "sh_snippet_builder_website_assets_frontend_" + str(res.id)
        key = "sh_snippet_builder." + name
        view = IrUiView.sh_snippet_builder_save_js_assets_snippet(res.name, global_js_view_arch, key)
        res.write({
            'js_asset_view_id' : view.id
            })        
        # -------------------------------------------
        # Make Assets template for JS
        # -------------------------------------------
        return res
    
    
    
    def write(self,vals):
        res = super(sh_snippet_builder,self).write(vals)
        IrUiView = self.env["ir.ui.view"]          
        for rec in self:
            view_arch = """<?xml version="1.0"?>
            <t name="Snippet Builder %(id)s" t-name="sh_snippet_builder.sh_snippet_builder_ud_tmpl_%(id)s">
                <section class="sh_snippet_builder_section_user_defined">
            """ % {
                'id' : rec.id
                }
#             if rec.js:
#                 view_arch += rec.js
            if rec.css:
                view_arch += rec.css
            if rec.html:
                view_arch += rec.html        
            
            view_arch += """
                </section>
            </t>
            """  
            
            xml_arch = etree.tostring(html.fromstring(view_arch), encoding='utf-8')            
            name = "sh_snippet_builder_ud_tmpl_" + str(rec.id)
            key = "sh_snippet_builder." + name            
            view = IrUiView.search([('key', '=', key)], limit=1)
            if view:
                view.sudo().write({
                    'arch':xml_arch
                    })
                
            # -------------------------------------------
            # Write Assets template for JS
            # -------------------------------------------        
            js = rec.js
            if js in ["<script></script>","<script/>"]:
                js = "<script>      </script>"
            
            name = "sh_snippet_builder_website_assets_frontend_" + str(rec.id)
            key = "sh_snippet_builder." + name
            arch = """<?xml version="1.0"?>
    <data inherit_id="website.assets_frontend">
        <xpath expr="//script[last()]" position="after">
    
                %s
    
        </xpath>
    </data>
            
            """ % js or ''            
#             xml_arch = etree.tostring(html.fromstring(arch), encoding='utf-8')
            view = IrUiView.search([('key', '=', key)], limit=1)
            if view:
                view.sudo().write({
                    'arch':arch
                    })

            # -------------------------------------------
            # Write Assets template for JS
            # -------------------------------------------

        return res    
    



    def unlink(self):
        IrUiView = self.env["ir.ui.view"] 
        for snippet_record in self:
            
            name = "sh_snippet_builder_ud_tmpl_" + str(snippet_record.id)
            key = "sh_snippet_builder." + name
            # =========================================================================           
            # Remove links in Snippet Panel View
            # =========================================================================     
            snippet_panel_view = IrUiView.sudo().search([
                ('key','=','sh_corpomate_theme.sh_snippet_builder_snippets')
                ],order='id desc',limit = 1)
            if snippet_panel_view and snippet_panel_view.arch:
                doc = etree.XML(snippet_panel_view.arch)
                xpath = '//t[@t-snippet="'+ key +'"]' 
                for node in doc.xpath(xpath):               
                    node.getparent().remove(node)  
                snippet_panel_view.arch = etree.tostring(doc, encoding='unicode')
            # =========================================================================           
            # Remove links in Snippet Panel View
            # ========================================================================= 
                         
            # =================================================
            # Remove ir ui view Qweb 
            # =================================================        
#             domain = [
#                 ('key','=',key),
#                 ('type','=','qweb'),
#             ]
            if snippet_record.view_id:
                snippet_record.view_id.unlink()
#                 view = IrUiView.search(domain, limit=1)
#             if view:
#                 view.unlink()    
                
            # =================================================
            # Remove ir ui view Qweb 
            # =================================================    
            
            # ----------------------------------------------------------------------------
            # Delete assets template.
            # ----------------------------------------------------------------------------                        
            if snippet_record.js_asset_view_id:
                snippet_record.js_asset_view_id.unlink()
            # ----------------------------------------------------------------------------
            # Delete assets template.
            # ----------------------------------------------------------------------------                        
                                    
        return super(sh_snippet_builder, self).unlink()