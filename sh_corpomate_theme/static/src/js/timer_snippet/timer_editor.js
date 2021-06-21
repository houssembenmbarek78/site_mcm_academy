odoo.define('sh_corpomate_theme.offer_timer_editor_js',function(require){
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var weContext = require('web_editor.context');
    var web_editor = require('web_editor.editor');
    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var qweb = core.qweb;
    var _t = core._t;




    ajax.loadXML('/sh_corpomate_theme/static/src/xml/offer_timer_popup.xml', core.qweb);
    

    // SNIPPET OPTION.
    options.registry.js_editor_offer_timer = options.Class.extend({
		
        start: function () {
            var self = this;
            var def = this._super.apply(this, arguments);
            return def;
            
         
            
        },    	

    	
        sh_corpomate_offer_timer_configure: function(previewMode, value){    		
            var self = this;
            if(previewMode === false || previewMode === "click"){
            	
            	// MAKE MODEL
            	self.$modal = $(qweb.render("sh_corpomate_theme.sh_popup_model_offer_timer_config"));
                
            	// REMOVE PREVIOUS APPENDED MODEL
            	$('body > #js_id_model_sh_corpomate_offer_config').remove();
                
            	// ADD MODEL TO BODY IN ORDER TO OPEN IT.
            	self.$modal.appendTo('body');
                
                // CLICK ON SAVE CHANGES BUTTON ADD CODE TO PAGE.
                self.$modal.on('click', ".js_cls_btn_apply_sh_offer_timer_config", function(){
                	
                	// START DATE
                	var date_start = self.$modal.find('input[name="date_start"]').val();              	
                	
                	// END DATE
                	var date_end = self.$modal.find('input[name="date_end"]').val();    
                	

                	
                	//self.$target.data('date_start',date_start);
                	//self.$target.data('date_end',date_end);
                	self.$target.attr("data-date_start", date_start);
                	self.$target.attr("data-date_end",date_end );
                	// PUT/ADD CODE IN ODOO PAGE.
                	//self.$target.empty().append( js + style +  html );
                	

                	           	
                	
                	self.$modal.find('.js_cls_btn_close_sh_offer_timer_config').click();             	
                	
/*                	self._rpc({
                        model: "sh.snippet.builder",
                        method: "create",
                        args: [{'html':html, 'js':js, 'css':style, 'name':name}],
                    })
                    .then(
                    		self.$modal.find('.js_cls_btn_close_sh_snippet_builder_config').click()
                    		
                    	);*/
                                    	
                	
                	
                	
                	// CLOSE THE MODEL
                	//self.$modal.find('.js_cls_btn_close_sh_snippet_builder_config').click();
                
                });                
                
                // REMOVE MODEL
                self.$modal.modal();
                
                
            }
            return self;
        },
        
        onBuilt: function(){
        	var self = this;
            this._super();
            this.sh_corpomate_offer_timer_configure('click');
        }
    });

});
