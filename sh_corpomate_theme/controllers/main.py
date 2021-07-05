# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo.http import request
from odoo import http, fields, _
from odoo.exceptions import UserError

from odoo.addons.website.controllers.main import Website


class Website(Website):
    

    @http.route(['/website/theme_customize'], type='json', auth="public", website=True)
    def theme_customize(self, enable, disable, get_bundle=False):
             
        # ==============================================================
        # FOR READYMADE THEME 
        # ==============================================================
        list_readymade_tmpl = [
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_1',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_2',   
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_3',   
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_4',   
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_5',      
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_6',   
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_7',  
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_8',  
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_9',     
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_10',  
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_11',     
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_12',   
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_13',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_14',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_15',
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_16',                                                              
            'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_none',                                                                                                                 
        ]
        
        # ======================================================        
        # STEP 1: CHECK IF CHANGED IN READYMADE THEME
        # ======================================================        
        selected_readymade_tmpl = ''
        is_readymade_theme_changed = False
        for item in list_readymade_tmpl:
            if item in enable:
                selected_readymade_tmpl = item
                is_readymade_theme_changed = True
                break
        
#         multiwebsite_domain = [
#             ("website_id",'=', request.website.id),    
#         ]
        
        multiwebsite_domain = request.website.website_domain()                
        
        if is_readymade_theme_changed:
            
            # ======================================================
            # MANAGE LIST OF OUR PAGES VIEW KEY
            # ======================================================            

            list_page_theme_1 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_1',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_1',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_1',                                                                                          
            ]
            list_page_theme_2 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_2',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_2',   
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_2',                                                                                                            
            ]

            list_page_theme_3 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_3',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_3',   
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_3',                                                                                                            
            ]

            list_page_theme_4 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_4',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_4', 
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_4',                                                                                                              
            ]

            list_page_theme_5 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_5',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_5',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_5',                                                                                                             
            ]

            list_page_theme_6 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_6',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_6', 
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_6',                                                                                                              
            ]
            
            list_page_theme_7 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_7',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_7',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_7',                                                                                                             
            ]            
            

            list_page_theme_8 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_8',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_8',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_8',                                                                                                              
            ]    
            

            list_page_theme_9 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_9',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_9',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_9',                                                                                                              
            ]    
            

            list_page_theme_10 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_10',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_10',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_10',                                                                                                              
            ]                
            
            list_page_theme_11 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_11',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_11',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_11',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_11',
#                 'sh_corpomate_theme.sh_corpomate_tmpl_our_team_11',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_11',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_11',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_11',  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_11',                                                                                                              
            ]
            
            
            
            list_page_theme_12 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_faq_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_privacy_policy_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_12',
                'sh_corpomate_theme.sh_corpomate_tmpl_terms_and_conditions_12',  
                'sh_corpomate_theme.sh_corpomate_tmpl_project_12',                  
                'sh_corpomate_theme.sh_corpomate_tmpl_mega_menu_12',                                                                                                              
            ]
            
            list_page_theme_13 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_13',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_13',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_13',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_13',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_13',                                                                                                                    
            ]

            list_page_theme_14 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_14',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_14',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_14',
                'sh_corpomate_theme.sh_corpomate_tmpl_our_team_14',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_14',                                                                                                                    
            ]

            list_page_theme_15 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_15',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_15',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_15',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_15',                                                                                                                    
            ]

            list_page_theme_16 = [
                'sh_corpomate_theme.sh_corpomate_tmpl_about_us_16',
                'sh_corpomate_theme.sh_corpomate_tmpl_contact_us_16',
                'sh_corpomate_theme.sh_corpomate_tmpl_home_16',
                'sh_corpomate_theme.sh_corpomate_tmpl_service_16',                                                                                                                    
            ]
                                                           
                        
            theme_none_list_page = list_page_theme_1 + list_page_theme_2 + list_page_theme_3 + list_page_theme_4 + \
            list_page_theme_5 + list_page_theme_6 + list_page_theme_7 + list_page_theme_8 + list_page_theme_9 + list_page_theme_10 + \
            list_page_theme_11 + list_page_theme_12 + list_page_theme_13 + list_page_theme_14 + list_page_theme_15 + list_page_theme_16
            
            dic_page_list = {
                'theme_1': list_page_theme_1,
                'theme_2': list_page_theme_2,
                'theme_3': list_page_theme_3,
                'theme_4': list_page_theme_4,
                'theme_5': list_page_theme_5,   
                'theme_6': list_page_theme_6,
                'theme_7': list_page_theme_7,  
                'theme_8': list_page_theme_8,  
                'theme_9': list_page_theme_9,  
                'theme_10': list_page_theme_10,        
                'theme_11': list_page_theme_11,          
                'theme_12': list_page_theme_12,   
                'theme_13': list_page_theme_13,  
                'theme_14': list_page_theme_14,
                'theme_15': list_page_theme_15, 
                'theme_16': list_page_theme_16,                                                                                 
                'theme_none': theme_none_list_page                                                                                     
                }
            
            
            # FIND VIEW IDS FOR ALL THEME AND MAKE DICTIONARY
            dic_page_view_ids_list = {}
            for key, value in dic_page_list.items():
                list_view_ids = []
                view_pages = request.env['ir.ui.view'].sudo().search([
                    ('key','in',value)
                    ])
                if view_pages.sudo():
                    list_view_ids = view_pages.sudo().ids
                
                dic_page_view_ids_list.update({
                    key: list_view_ids
                    })
                
            
            if dic_page_view_ids_list:

                # ======================================================
                # STEP 2 HIDE OUR ALL PAGES
                # ======================================================                    
                ids  = sum(dic_page_view_ids_list.values(), []) 
                page_domain = [ ('view_id', 'in', ids) ]        
                     
                # UNPUBLISH ALL OUR PAGES.
                pages = request.env['website.page'].sudo().search(page_domain + multiwebsite_domain)
                if pages:
#                     pages.sudo().write({
#                         'website_published': False,
#                         })
                    
                    # delete all menu here    
                    menu_ids_list = []
                    for page in pages:
                        if page.menu_ids:
                            menu_ids_list += page.menu_ids.ids
                                                    
                    menu_domain = [
                        ('id','in', menu_ids_list),
                        ("website_id",'=', request.website.id),  
                    ]
                    menus = request.env['website.menu'].sudo().search(menu_domain)

                    if menus:
                        menus.sudo().unlink()
                    
                # delete all menu here                    
                # ======================================================
                # STEP 2 HIDE OUR ALL PAGES
                # ======================================================                        
                    
                    
                # ======================================================
                # STEP 3 SHOW SELECTED THEME PAGES
                # ======================================================              
                
                if selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_1':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_1", []) )]           

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_2':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_2", []) )]              
                
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_3':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_3", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_4':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_4", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_5':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_5", []) )]                                                   

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_6':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_6", []) )]    
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_7':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_7", []) )]                        
                     
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_8':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_8", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_9':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_9", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_10':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_10", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_11':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_11", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_12':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_12", []) )]   
                    
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_13':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_13", []) )]   

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_14':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_14", []) )]    

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_15':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_15", []) )]  

                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_16':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_16", []) )]        
                
                elif selected_readymade_tmpl == 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_none':
                    page_domain = [ ('view_id', 'in', dic_page_view_ids_list.get("theme_none", []) )]   
                    
                    theme_none_domain = [
                        ('view_id.key','=','website.homepage'),
                        ('website_id','=',request.website.id),                      
                    ]
                     
                    page_home = request.env['website.page'].sudo().search(theme_none_domain)   
                    if page_home:
                        page_home.sudo().is_homepage = True
                                      
                # PUBLISH SPECIFIED THEME PAGES.
                pages = request.env['website.page'].sudo().search(page_domain + multiwebsite_domain)
                if pages and selected_readymade_tmpl != 'sh_corpomate_theme.sh_corpomate_theme_layout_readymade_none':

#                     pages.sudo().write({
#                         'website_published': True,
#                         })
                    
                    
                    
                    # Create Menu Here
                    for page in pages:
                        menu_vals = {
                            'page_id': page.id,
                            'name': page.name,
                            'url' : page.url,
                            'parent_id': request.website.menu_id.id,                         
                            'website_id':request.website.id,
                        }
                        
                        # search menu
                        domain = [
                            ('website_id','=',request.website.id),
                            ('page_id','=',page.id),
                            ('url','=',page.url),                         
                        ]
                        
                        search_menu = request.env['website.menu'].sudo().search(domain)
                        if not search_menu:
                            
                            # search menu
                            domain = [
                                ('website_id','=',False),
                                ('page_id','=',page.id),
                                ('url','=',page.url),                         
                            ]                            
                            search_menu = request.env['website.menu'].sudo().search(domain, limit = 1)
                            
                            if search_menu:
                                # TODO: ADD HOMEPAGE AND SEQUENCE IN BELOW DICTIONARY.
                                
                                menu_vals.update({
                                    "sh_website_mega_menu_html" : search_menu.sh_website_mega_menu_html,
                                    "sequence" : search_menu.sequence,                                    
                                    })
                                                            
                            
                            menus = request.env['website.menu'].sudo().create(menu_vals)
                            
                            # ========================
                            # Make Home Page Here

                            if page.view_id and 'sh_corpomate_theme.sh_corpomate_tmpl_home_' in page.view_id.key:
                                page.sudo().is_homepage = True

                                
                                
                            
                            
                        
                    # Create Menu Here                       
                    
                            
                # ======================================================
                # STEP 3 SHOW SELECTED THEME PAGES
                # ======================================================                   
                    
        
        # ==============================================================
        # FOR READYMADE THEME 
        # ==============================================================        
            

                        
        response = super(Website, self).theme_customize(enable, disable, get_bundle=False)
        
        return response


class main(http.Controller):
    
    @http.route('/sh_corpomate_theme/render_testimonial', type='json', auth="none", method = ['post'], website = True)
    def render_testimonial(self,template_id = False):                    
        
        domain_testimonial = [
            ('active','=',True),
        ]        
        
        testimonial_order = "sequence desc"
                     
        testimonials =  request.env['sh.corpomate.theme.testimonial'].sudo().search(
            domain_testimonial,
            order = testimonial_order,
            )
                                    
        data = """
        
     <div class="owl-carousel owl-theme">
        
        """
        
        if testimonials:
            for testimonial in testimonials:
                
                                
                html = request.env.ref(template_id).render({
                    'testimonial':testimonial,
                    
                })
                
                data += html.decode("utf-8")                 
                     
                 
        data += """
           </div>
             
        """
        return data
    

    
    
    
    
    
    
    @http.route('/sh_corpomate_theme/render_our_partner', type='json', auth="none", method = ['post'], website = True)
    def render_our_partner(self,template_id = False):                    
        
        domain_our_partner = [
            ('active','=',True),
        ]        
        
        our_partner_order = "sequence desc"
                     
        our_partners =  request.env['sh.corpomate.theme.our.partner'].sudo().search(
            domain_our_partner,
            order = our_partner_order,
            )
                                    
        data = """
        
     <div class="owl-carousel owl-theme carousel-main">
        
        """
        
        if our_partners:
            for our_partner in our_partners:
                            
                html = request.env.ref(template_id).render({
                    'our_partner':our_partner,
                    
                })
                
                data += html.decode("utf-8")                 
                     
                 
        data += """
           </div>
             
        """
        
        return data

    # @http.route('/home1', type='http', auth="public", website=True)
    # def home1(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_1", {})
    
    
    # @http.route('/home2', type='http', auth="public", website=True)
    # def home2(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_2", {})
   
    # @http.route('/home3', type='http', auth="public", website=True)
    # def home3(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_3", {})
    
    # @http.route('/home4', type='http', auth="public", website=True)
    # def home4(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_4", {})
    
    # @http.route('/home5', type='http', auth="public", website=True)
    # def home5(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_5", {})
    
    # @http.route('/home6', type='http', auth="public", website=True)
    # def home6(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_6", {})
    
    # @http.route('/home7', type='http', auth="public", website=True)
    # def home7(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_7", {})
   
    # @http.route('/home8', type='http', auth="public", website=True)
    # def home8(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_8", {})
   
    # @http.route('/home9', type='http', auth="public", website=True)
    # def home9(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_9", {})
   
    # @http.route('/home10', type='http', auth="public", website=True)
    # def home10(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_10", {})
    
    # @http.route('/home11', type='http', auth="public", website=True)
    # def home11(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_11", {})
    
    # @http.route('/home12', type='http', auth="public", website=True)
    # def home12(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_12", {})
    
    # @http.route('/home13', type='http', auth="public", website=True)
    # def home13(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_13", {})
        
    # @http.route('/home14', type='http', auth="public", website=True)
    # def home14(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_14", {})
    
    # @http.route('/home15', type='http', auth="public", website=True)
    # def home15(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_15", {})
    
    # @http.route('/home16', type='http', auth="public", website=True)
    # def home16(self):
    #     return request.render("sh_corpomate_theme.sh_corpomate_tmpl_home_16", {})
    
    
 
    
    
        
    

