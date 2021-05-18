odoo.define('sh_snippet_adv.snippets.options', function (require) {
'use strict';

var core = require('web.core');
var Dialog = require('web.Dialog');
var weWidgets = require('wysiwyg.widgets');
var options = require('web_editor.snippets.options');

var ColorpickerDialog = require('web.ColorpickerDialog');


var _t = core._t;
var qweb = core.qweb;



function _rgbToHex(cssColor) {
    var rgba = cssColor.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/);
    if (!rgba) {
        return cssColor;
    }
    if (rgba[4]) {
        return cssColor;
    }
    var hex = ColorpickerDialog.convertRgbToHex(
        parseInt(rgba[1]),
        parseInt(rgba[2]),
        parseInt(rgba[3])
    );
    if (!hex) {
        return cssColor; // TODO handle error
    }
    return hex.hex.toUpperCase();
}






var colorpicker = options.registry.colorpicker.include({
    events: _.extend({}, options.registry.colorpicker.prototype.events || {}, {
        'click .sh-custom-color': '_SHonCustomColorButtonClick',

    }),
    
    custom_events: _.extend({}, options.registry.colorpicker.prototype.custom_events, {
        "colorpicker:saved": "_SHonCustomColorSave",
    }),
    
    
   
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * 
     * Called when a user click on custom color button to open colorpicker dialog
     *
     */
    
    
    _SHonCustomColorButtonClick: function () {

    	
    	var color = this.$target.css("background-color");

    	// Make sure opacity is not zero if bg color is not set.
    	if ( color == 'rgba(0, 0, 0, 0)'){
    		color = _.str.sprintf('rgba(%s, %s, %s, %s)',
    		        0,
    		        0,
    		        0,
    		        1,
    		    );
    	}
    	
    	// define color picker dialog with default color
        var colorpicker = new ColorpickerDialog(this, {
            defaultColor: color,
        });
        
    	
    	//open colorpicker dialog
        colorpicker.open();
        
    },

    /**
     * 
     * Called when a user save custom color button in colorpicker dialog
     *
     */        
    
    _SHonCustomColorSave: function (event) {

        var color = event.data.cssColor;
        
        // create custom color button
        var $button = $('<button class="o_custom_color" style="background-color: ' + color + '" />');
        
        // add new color in custom color palette        
        var $custom = this.$el.find('.sh-custom-color-palette[data-name="sh-custom-color-palette"]');
        $custom.append($button);
        
        // Click on newly created color button to apply that color 
        $button.mouseenter().click();
    },
    

    
});









options.registry.shborderstyle = options.Class.extend({
    custom_events: _.extend({}, options.registry.colorpicker.prototype.custom_events, {
        "colorpicker:saved": "_SHonBorderColorSave",
    }),
    
    
    
    /**
     * 
     * Called when a user save custom color button in colorpicker dialog
     *
     */        
    
    _SHonBorderColorSave: function (event) {

        // Get selected Color
    	var color = event.data.cssColor;
                
        // Apply Border color
    	this.$target.css('border-color', color);
    },
    
    
    
	/**
     * @override
     */
    /*
    start: function () {
        var self = this;
        this.$target.on('snippet-option-change snippet-option-preview', function () {
            self._refreshPublicWidgets();
        });
        return this._super.apply(this, arguments);
    },
    */
    
  
    /**
     * @override
     */
  
    /*
    onFocus: function () {
    	     
    	this.trigger_up('option_update', {
            optionNames: ['background', 'background_position'],
            name: 'target',
            data: this.$target.find('> .s_parallax_bg'),
        });
    
        // Refresh the parallax animation on focus; at least useful because
        // there may have been changes in the page that influenced the parallax
        // rendering (new snippets, ...).
        // TODO make this automatic.
        this._refreshPublicWidgets();
    },
   */
    
    /**
     * @override
     */


    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    /**
     * Changes the border style  of the selected element.
     *
     * @see this.selectClass for parameters
     */
    border_style: function (previewMode, value) {
        //this.$target.attr('border_style', value);
        this.$target.css('border-style', value);
		
        //this._refreshPublicWidgets();
    },

    
    /**
     * Changes the border width  of the selected element.
     *
     * @see this.selectClass for parameters
     */
    border_width: function (previewMode, value) {
        //this.$target.attr('border_style', value);
        this.$target.css('border-width', value);
		
        //this._refreshPublicWidgets();
    },
    
    /**
     * Changes the border Color  of the selected element.
     *
     * @see this.selectClass for parameters
     */
    border_color: function (previewMode, value) {
        
    	var color = this.$target.css("border-color");

    	// Make sure opacity is not zero if bg color is not set.
    	if ( color == 'rgba(0, 0, 0, 0)'){
    		color = _.str.sprintf('rgba(%s, %s, %s, %s)',
    		        0,
    		        0,
    		        0,
    		        1,
    		    );
    	}
    	
    	// define color picker dialog with default color
        var colorpicker = new ColorpickerDialog(this, {
            defaultColor: color,
        });
        
    	
    	//open colorpicker dialog
        colorpicker.open();
        

		
        //this._refreshPublicWidgets();
    },
    
    
    
    /**
     * Changes the border radius  of the selected element.
     *
     * @see this.selectClass for parameters
     */
    border_radius: function (previewMode, value) {
    	   	
        var self = this;
        
        // Content
        var radius_full = '<div class="form-group row"> \
        	<label class="col-md-3 col-form-label" for="sh_border_radius_opt_lbl">Full Radius</label> \
            <div class="col-md-5"> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_radius_opt_input_full" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';

        // Top Left
        var radius_top_left = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_radius_opt_lbl">Top Left</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_radius_opt_input_top_left" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';

        
        // Top Right
        var radius_top_right = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_radius_opt_lbl">Top Right</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_radius_opt_input_top_right" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';
        
        // Bottom Left
        var radius_bottom_left = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_radius_opt_lbl">Bottom Left</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_radius_opt_input_bottom_left" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';
        
        // Bottom Right
        var radius_bottom_right = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_radius_opt_lbl">Bottom Right</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_radius_opt_input_bottom_right" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';
        
        
        
        var content_border_radius_opt = ' \
            <form class="sh_border_radius_opt_form" data-value="custom"> \
        <fieldset>';
        
        
        content_border_radius_opt += radius_full;
        
        content_border_radius_opt += radius_top_left;
        content_border_radius_opt += radius_top_right;
        content_border_radius_opt += radius_bottom_left;
        content_border_radius_opt += radius_bottom_right;
        
        
        content_border_radius_opt += ' \
        </fieldset> \
    </form> ';
        		
        		
        // Dialog		
        this.modal_border_radius_opt = new Dialog(null, {
            title: _t("Border Radius"),
            size: 'medium',
            //$content:$(qweb.render('sh_snippet_adv.dialog.border_radius')),            
            $content:content_border_radius_opt,              
            
            buttons: [
                {text: _t("Apply"), classes: 'btn-primary', close: true, click: _.bind(this._saveChanges_border_radius_opt, this)},
                //{text: _t("Discard"), close: true, click: _.bind(this._discardChanges, this)},
            ],
            
            
        }).open();
        
        
        
        
        // Set Default Value
        this.modal_border_radius_opt.opened().then(function () {
        	// Fetch data form $target
        	var border_radius = self.$target.css('border-radius') || '0px 0px 0px 0px';
        	        	
            var arr = border_radius.split(" ");
            var arr_length = arr.length;
        	
        	arr[0] = arr[0] || '0px';
        	arr[1] = arr[1] || '0px';
        	arr[2] = arr[2] || '0px';
        	arr[3] = arr[3] || '0px';        	
        	
            var top_left = arr[0].replace('px', '');
            var top_right = arr[1].replace('px', '');        
            var bottom_right = arr[2].replace('px', '');   
            var bottom_left = arr[3].replace('px', '');  
            var full = 0;
            
            if (arr_length <= 1) {
            	full = top_left;
            	top_right = top_left;
            	bottom_right = top_left;
            	bottom_left = top_left;            	
            	
            }
            
            self.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_full').val(full);
            self.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_top_left').val(top_left);
            self.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_top_right').val(top_right);        
            self.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_bottom_right').val(bottom_right);   
            self.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_bottom_left').val(bottom_left);  
            
                   	
            self.modal_border_radius_opt.$el.on('change', '#js_id_sh_border_radius_opt_input_full', function (e) {
                var full_value = $(e.currentTarget).val();
            	self._onChange_sh_border_radius_opt_input_full(full_value);
            });
            
        	

        });
    
        
        
        
        
    	
    	
    },
    

    
    /**
     * Onchange Full Radius property update left, right, top, bottom values.
     *
     * @private
     */
    _onChange_sh_border_radius_opt_input_full: function (full_value) {
      
    	this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_top_left').val(full_value);
    	this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_top_right').val(full_value);
    	this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_bottom_left').val(full_value);
    	this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_bottom_right').val(full_value);
                
    },  
    
    
    
    
    
    /**
     * Updates the target element border radius property.
     *
     * @private
     */
    _saveChanges_border_radius_opt: function () {
        //this._clean();
            	
        var top_left = this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_top_left').val();
        var top_right = this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_top_right').val();        
        var bottom_right = this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_bottom_right').val();   
        var bottom_left = this.modal_border_radius_opt.$('#js_id_sh_border_radius_opt_input_bottom_left').val();   
        
        var final_radius = (top_left ? top_left + 'px' : 'auto')  + ' ' + (top_right ? top_right + 'px' : 'auto') + ' ' + (bottom_right ? bottom_right + 'px' : 'auto') + ' ' + (bottom_left ? bottom_left + 'px' : 'auto'); 
                
        this.$target.css({
            'border-radius': final_radius,
        });        
                
    },    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    /**
     * Changes the border width custom  of the selected element.
     *
     * @see this.selectClass for parameters
     */
    border_width_custom: function (previewMode, value) {
    	   	
        var self = this;
        
        // Content
        var width_full = '<div class="form-group row"> \
        	<label class="col-md-3 col-form-label" for="sh_border_width_opt_lbl">Full width</label> \
            <div class="col-md-5"> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_width_opt_input_full" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';

        // Top
        var width_top = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_width_opt_lbl">Top</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_width_opt_input_top" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';

        
        // Right
        var width_right = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_width_opt_lbl">Right</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_width_opt_input_right" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';
        
        // Bottom
        var width_bottom = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_width_opt_lbl">Bottom</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_width_opt_input_bottom" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';
        
        // Left
        var width_left = '<div class="form-group" style="width: 50%;display: inline-block;padding: 5px;"> \
        	<label class="col-form-label" for="sh_border_width_opt_lbl">Left</label> \
            <div class=""> \
                <div class="input-group"> \
                    <input type="number" min="0" class="form-control" id="js_id_sh_border_width_opt_input_left" placeholder="auto"/> \
                    <div class="input-group-append"> \
                        <div class="input-group-text">px</div> \
                    </div> \
                </div> \
            </div> \
                </div>';
        
        
        
        var content_border_width_opt = ' \
            <form class="sh_border_width_opt_form" data-value="custom"> \
        <fieldset>';
        
        
        content_border_width_opt += width_full;
        
        content_border_width_opt += width_top;
        content_border_width_opt += width_right;
        content_border_width_opt += width_bottom;
        content_border_width_opt += width_left;
        
        
        content_border_width_opt += ' \
        </fieldset> \
    </form> ';
        		
        		
        // Dialog		
        this.modal_border_width_opt = new Dialog(null, {
            title: _t("Border Width"),
            size: 'medium',
            //$content:$(qweb.render('sh_snippet_adv.dialog.border_width')),            
            $content:content_border_width_opt,              
            
            buttons: [
                {text: _t("Apply"), classes: 'btn-primary', close: true, click: _.bind(this._saveChanges_border_width_opt, this)},
                //{text: _t("Discard"), close: true, click: _.bind(this._discardChanges, this)},
            ],
            
            
        }).open();
        
        
        
        
        // Set Default Value
        this.modal_border_width_opt.opened().then(function () {
        	// Fetch data form $target        	
        	
        	/*
        	var top = self.$target.css('border-top-width') || '0px';
    		var right = self.$target.css('border-right-width') || '0px';
        	var bottom = self.$target.css('border-bottom-width') || '0px';
        	var left = self.$target.css('border-left-width') || '0px';
        	
        	top = top.replace('px', '');
        	right = right.replace('px', '');
        	bottom = bottom.replace('px', '');
        	left = left.replace('px', '');
        	
            var full = 0;
            
            if (top == right == bottom == left) {
            	full = top;        	
            	
            }
            
            */
        	
        	
        	var border_width = self.$target.css('border-width') || '0px 0px 0px 0px';
        	
            var arr = border_width.split(" ");
            var arr_length = arr.length;
        	
        	arr[0] = arr[0] || '0px';
        	arr[1] = arr[1] || '0px';
        	arr[2] = arr[2] || '0px';
        	arr[3] = arr[3] || '0px';        	
        	
            var top = arr[0].replace('px', '');
            var right = arr[1].replace('px', '');        
            var bottom = arr[2].replace('px', '');   
            var left = arr[3].replace('px', '');  
            var full = 0;
            
            if (arr_length <= 1) {
            	full = top;
            	right = top;
            	bottom = top;
            	left = top;            	
            	
            }
                    	
            self.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_full').val(full);
            self.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_top').val(top);
            self.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_right').val(right);        
            self.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_bottom').val(bottom);   
            self.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_left').val(left);  
            
                   	
            self.modal_border_width_opt.$el.on('change', '#js_id_sh_border_width_opt_input_full', function (e) {
                var full_value = $(e.currentTarget).val();
            	self._onChange_sh_border_width_opt_input_full(full_value);
            });
            
        	

        });
    
        
        
        
        
    	
    	
    },    
    
    
    
    
    /**
     * Onchange Full width property update left, right, top, bottom values.
     *
     * @private
     */
    _onChange_sh_border_width_opt_input_full: function (full_value) {
      
    	this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_top').val(full_value);
    	this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_right').val(full_value);
    	this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_bottom').val(full_value);
    	this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_left').val(full_value);
                
    },  
    
    
    
    
        
    /**
     * Updates the target element border width property.
     *
     * @private
     */
    _saveChanges_border_width_opt: function () {
        //this._clean();
            	
        var top = this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_top').val();
        var right = this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_right').val();        
        var bottom = this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_bottom').val();   
        var left = this.modal_border_width_opt.$('#js_id_sh_border_width_opt_input_left').val();   
         
        this.$target.css({
            'border-top-width':  (top ? top + 'px' : 'auto'),
            'border-right-width':  (right ? right + 'px' : 'auto'),
            'border-bottom-width':  (bottom ? bottom + 'px' : 'auto'),
            'border-left-width':  (left ? left + 'px' : 'auto'),            
        });        
                
    },    
    
    
    
    
    
    
    

    
    
    
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    _setActive: function () {
        this._super.apply(this, arguments);
        
        
        this.$el.find('[data-border_style]').removeClass('active')
            .filter('[data-border_style="' + (this.$target.css('border-style') || 'none') + '"]').addClass('active');
    
        this.$el.find('[data-border_width]').removeClass('active')
        .filter('[data-border_width="' + (this.$target.css('border-width') || '0px') + '"]').addClass('active');
        
        
    },

});


















return colorpicker;

});
