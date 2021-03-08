odoo.define('sh_emate.js_sh_emate_get_product_editor', function (require) {
'use strict';

var core = require('web.core');
var sOptions = require('web_editor.snippets.options');

var _t = core._t;



sOptions.registry.js_sh_emate_get_product_select_slider = sOptions.Class.extend({
    /**
     * @override
     */
    start: function () {
        var self = this;
        var res = this._super.apply(this, arguments);

        return res;
    },


    
    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    
    
    /**
     * @override
     */
    selectClass: function (previewMode, value, $opt) {
    	var self = this;        
    	this._super(previewMode, value, $opt);

    	// get all class
        var className = this.$target.attr('class') || '';

        var tmpl_item_name = className.match(/\bsh_emate_s_item_.*?\b/g);
        if (tmpl_item_name){
        	tmpl_item_name = tmpl_item_name[0];
        	tmpl_item_name = tmpl_item_name.replace("sh_emate_s_item_", "");        	
        }
        
        //get a match to match the pattern sh_emate_slider_id_somenumber and extract that classname
        className = className.match(/sh_emate_slider_id_\d+/); 


        if (className) {
            className = className[0];
            className = className.replace("sh_emate_slider_id_", "");
            className = parseInt(className);

            //SEARCH PRODUCT HERE
        	var is_show_product_desc = false;
        	var is_show_sale_price = false;   
        	
    		//product description
    		if(this.$target.hasClass( "is_show_product_desc" )){
    			is_show_product_desc = true;
    		}

    		//sale price
    		if(this.$target.hasClass( "is_show_sale_price" )){
    			is_show_sale_price = true;
    		} 	    
    		
            self._rpc({
                model: 'sh.emate.slider',
                method: 'get_data',
                args: [className,is_show_product_desc,is_show_sale_price,tmpl_item_name],            
            }).then(function (result) {
            	self.$target.find('.js_cls_sh_mail_snippet_general').replaceWith(result);
            })
           
            //SEARCH PRODUCT HERE                
            
        }
        
        
    },
    
        
    
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    toggleClass: function (previewMode, value, $opt) {
        //this._super.apply(this, arguments);    	
        
    	var self = this;        
    	this._super(previewMode, value, $opt);

    	// get all class
        var className = this.$target.attr('class') || '';

        var tmpl_item_name = className.match(/\bsh_emate_s_item_.*?\b/g);
        if (tmpl_item_name){
        	tmpl_item_name = tmpl_item_name[0];
        	tmpl_item_name = tmpl_item_name.replace("sh_emate_s_item_", "");        	
        }
        
        //get a match to match the pattern sh_emate_slider_id_somenumber and extract that classname
        className = className.match(/sh_emate_slider_id_\d+/); 


        if (className) {
            className = className[0];
            className = className.replace("sh_emate_slider_id_", "");
            className = parseInt(className);

            //SEARCH PRODUCT HERE
        	var is_show_product_desc = false;
        	var is_show_sale_price = false;   
        	
    		//product description
    		if(this.$target.hasClass( "is_show_product_desc" )){
    			is_show_product_desc = true;
    		}

    		//sale price
    		if(this.$target.hasClass( "is_show_sale_price" )){
    			is_show_sale_price = true;
    		} 	    
    		
            self._rpc({
                model: 'sh.emate.slider',
                method: 'get_data',
                args: [className,is_show_product_desc,is_show_sale_price,tmpl_item_name],            
            }).then(function (result) {
            	self.$target.find('.js_cls_sh_mail_snippet_general').replaceWith(result);
            })
           
            //SEARCH PRODUCT HERE                
            
        }        
        
        
        
    },    
    
    
    
   
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _setActive: function () {
        this._super.apply(this, arguments);
    	
        this.$el.find('[data-filter-by-slider-id]').removeClass('active')
            .filter('[data-filter-by-slider-id=' + this.$target.attr('data-filter-by-slider-id') + ']').addClass('active');
    },    
    
    
    
});


});
