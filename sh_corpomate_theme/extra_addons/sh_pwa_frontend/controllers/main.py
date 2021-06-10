# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
import json
from odoo import http
import base64
from io import BytesIO
from odoo.tools.misc import file_open

class Main(http.Controller):
    
    def _get_manifest_json(self):
        pwa_config = http.request.env['sh.pwa.frontend.config'].sudo().search([] , limit=1)
        vals = {
              "name": "Softhealer-APP",
              "short_name": "SH-APP",
              "scope": "/",
              "start_url": "/",
              "background_color": "purple",
              "display": "standalone",
            }
        if pwa_config:
            if pwa_config.name:
                vals.update({'name' : pwa_config.name })
            if pwa_config.short_name:
                vals.update({'short_name' : pwa_config.short_name })
            if pwa_config.theme_color:
                vals.update({'theme_color' : pwa_config.theme_color })
            if pwa_config.background_color:
                vals.update({'background_color' : pwa_config.background_color })
            if pwa_config.display:
                vals.update({'display' : pwa_config.display }) 
            if pwa_config.orientation:
                vals.update({'orientation' : pwa_config.orientation })
            if pwa_config.start_url:
                vals.update({'start_url' : pwa_config.start_url })
                
            default_icon_list = []
            if pwa_config.icon_small and pwa_config.icon_small_mimetype and pwa_config.icon_small_size :
                default_icon_list.append({
                        'src': '/sh_pwa_frontend/pwa_icon_small',
                        'type': pwa_config.icon_small_mimetype,
                        'sizes': pwa_config.icon_small_size
                    })
            if pwa_config.icon and pwa_config.icon_mimetype and pwa_config.icon_size :
                default_icon_list.append({
                        'src': '/sh_pwa_frontend/pwa_icon',
                        'type': pwa_config.icon_mimetype,
                        'sizes': pwa_config.icon_size
                    })
                
            if len(default_icon_list) == 0:
                default_icon_list =  [
                    {
                      "src": "/sh_pwa_frontend/static/icon/sh.png",
                      "sizes": "192x192",
                      "type": "image/png"
                    }
                  ]
                    
            vals.update({'icons' : default_icon_list})
            
        return vals

    
    @http.route('/manifest.json', type='http', auth="public")
    def manifest_http(self):
        return json.dumps(self._get_manifest_json())
    
    @http.route('/sw.js', type='http', auth="public")
    def sw_http(self):
        js = """
        this.addEventListener('install', function(e) {
         e.waitUntil(
           caches.open('video-store').then(function(cache) {
             return cache.addAll([
                 '/sh_pwa_frontend/static/index.js'
             ]);
           })
         );
        });
        
        this.addEventListener('fetch', function(e) {
          e.respondWith(
            caches.match(e.request).then(function(response) {
              return response || fetch(e.request);
            })
          );
        });
        """     
        return http.request.make_response(js, [('Content-Type', 'text/javascript')])
    
    def get_icon(self, field_icon):
        pwa_config = http.request.env['sh.pwa.frontend.config'].sudo().search([] , limit=1)
        if pwa_config:
            icon = getattr(pwa_config, field_icon)
            icon_mimetype = getattr(pwa_config, field_icon + '_mimetype')
            if icon:
                icon = BytesIO(base64.b64decode(icon))
            return http.request.make_response(
                icon.read(), [('Content-Type', icon_mimetype)])

    @http.route('/sh_pwa_frontend/pwa_icon', type='http', auth="none")
    def icon_small(self):
        return self.get_icon('icon')

    @http.route('/sh_pwa_frontend/pwa_icon_small', type='http', auth="none")
    def icon(self):
        return self.get_icon('icon_small')
    
    @http.route('/iphone_front.json/<string:cid>', type='http', auth="public")
    def iphone_http(self,**post):
        company = post.get('cid')
        pwa_config = http.request.env['sh.pwa.frontend.config'].sudo().search([] , limit=1)
        if pwa_config:
            icon = pwa_config.icon_iphone
           
            icon_mimetype = getattr(pwa_config, 'icon' + '_mimetype')
            if icon:
                icon = BytesIO(base64.b64decode(icon))
                return http.request.make_response(
                    icon.read(), [('Content-Type', icon_mimetype)])
