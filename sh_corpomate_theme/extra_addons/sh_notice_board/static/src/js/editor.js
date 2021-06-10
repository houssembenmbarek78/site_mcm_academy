odoo.define('sh_notice_board.editor', function (require) {
'use strict';


require('web.dom_ready');
var ajax = require('web.ajax');
var core = require('web.core');
var options = require('web_editor.snippets.options');
var Animation = require('website.content.snippets.animation');
var weContext = require('web_editor.context');
var _t = core._t;


options.registry.sh_nb_notice_board_horizontal_sec_editor_js_1 = options.Class.extend({
	
//for add marque direction classes.	
direction: function (previewMode, value, $li) {
    if (value && value.length) {
        this.$target.removeClass('newsdir_left newsdir_right').addClass(value);
    	var marquee = this.$target.find('div').children('marquee');
    	if(marquee){
    		
    		if (value === 'newsdir_left'){
        		marquee.attr("direction", "left");        			
    		}
    		if (value === 'newsdir_right'){
        		marquee.attr("direction", "right");        			
    		}        		
    		
    	}
    } else {
        this.$target.removeClass('newsdir_left newsdir_right');
    }
},    	
	

//for number of news (rows) display in marquee
selectClass: function (previewMode, value, $li) {
    this._super.apply(this, arguments);

    if(value && value.length){
    	var val_2 = value;
    	var rows = val_2.replace("newscount_", "");
    	var marquee = this.$target.find('div').children('marquee');
        
    	if(marquee){
        	var old_dir = marquee.attr('direction');
            var new_marquee = $('<marquee  class="sh_nb_notice_board_main_horizontal_marquee_cls_1" direction = "left" onmouseover="this.stop();" onmouseout="this.start();"></marquee>');    
            new_marquee.attr('direction', old_dir);
            
            
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })
            .then(function (data) {
                _.each(data, function (news) {
                	new_marquee.append(
                    		"<span>" + news.desc + "</span>"
                        );
                });
            });                
            marquee.replaceWith(new_marquee);     
        	
        }

    }
    
},    

});







//for horizontal snippet 2
options.registry.sh_nb_notice_board_horizontal_sec_editor_js_2 = options.Class.extend({
	
	//for add marque direction classes.	
	direction: function (previewMode, value, $li) {
	    if (value && value.length) {
	        this.$target.removeClass('newsdir_left newsdir_right').addClass(value);
	    	var marquee = this.$target.find('div').children('marquee');
	    	if(marquee){
	    		
	    		if (value === 'newsdir_left'){
	        		marquee.attr("direction", "left");        			
	    		}
	    		if (value === 'newsdir_right'){
	        		marquee.attr("direction", "right");        			
	    		}        		
	    		
	    	}
	    } else {
	        this.$target.removeClass('newsdir_left newsdir_right');
	    }
	},    	
		

	//for number of news (rows) display in marquee
	selectClass: function (previewMode, value, $li) {
	    this._super.apply(this, arguments);

	    if(value && value.length){
	    	var val_2 = value;
	    	var rows = val_2.replace("newscount_", "");
	    	var marquee = this.$target.find('div').children('marquee');
	        
	    	if(marquee){
	        	var old_dir = marquee.attr('direction');
	            var new_marquee = $('<marquee class="sh_nb_notice_board_main_horizontal_marquee_cls_2" direction="left" onmouseover="this.stop();" onmouseout="this.start();"></marquee>');    
	            new_marquee.attr('direction', old_dir);
	            
	            
	            ajax.jsonRpc('/get_latest_news', 'call', {
	            	limit:  parseInt(rows),
	                })
	            .then(function (data) {
	                _.each(data, function (news) {
	                	new_marquee.append(
	                            "<div class='sh_text'><span class='fa fa-caret-right' aria-hidden='true'> </span>"+ news.desc + "</div>"
	                    	);
	                });
	            });                
	            marquee.replaceWith(new_marquee);     
	        	
	        }

	    }
	    
	},    

	});





//for horizontal snippet 3
options.registry.sh_nb_notice_board_horizontal_sec_editor_js_3 = options.Class.extend({
	
	//for add marque direction classes.	
	direction: function (previewMode, value, $li) {
	    if (value && value.length) {
	        this.$target.removeClass('newsdir_left newsdir_right').addClass(value);
	    	var marquee = this.$target.find('div').children('marquee');
	    	if(marquee){
	    		
	    		if (value === 'newsdir_left'){
	        		marquee.attr("direction", "left");        			
	    		}
	    		if (value === 'newsdir_right'){
	        		marquee.attr("direction", "right");        			
	    		}        		
	    		
	    	}
	    } else {
	        this.$target.removeClass('newsdir_left newsdir_right');
	    }
	},    	
		

	//for number of news (rows) display in marquee
	selectClass: function (previewMode, value, $li) {
	    this._super.apply(this, arguments);

	    if(value && value.length){
	    	var val_2 = value;
	    	var rows = val_2.replace("newscount_", "");
	    	var marquee = this.$target.find('div').children('marquee');
	        
	    	if(marquee){
	        	var old_dir = marquee.attr('direction');
	            var new_marquee = $('<marquee class="sh_nb_notice_board_main_horizontal_marquee_cls_3" direction="left" onmouseover="this.stop();" onmouseout="this.start();"></marquee>');    
	            new_marquee.attr('direction', old_dir);
	            
	            
	            ajax.jsonRpc('/get_latest_news', 'call', {
	            	limit:  parseInt(rows),
	                })
	            .then(function (data) {
	                _.each(data, function (news) {
	                	new_marquee.append(
	                            "<div class='sh_news_description'><span class='fa fa-caret-right'> </span>"+ news.desc + "</div>"
	                    	);
	                });
	            });                
	            marquee.replaceWith(new_marquee);     
	        	
	        }

	    }
	    
	},    

	});


//===========================================
// for vertical snipppet
//===========================================

//for vertical snippet 1
options.registry.sh_nb_notice_board_vertical_sec_editor_js_1 = options.Class.extend({
	
	//for add marque direction classes.	
	direction: function (previewMode, value, $li) {
	    if (value && value.length) {
	        this.$target.removeClass('newsdir_left newsdir_right').addClass(value);
	    	var marquee = this.$target.find('div').children('marquee');
	    	if(marquee){
	    		
	    		if (value === 'newsdir_left'){
	        		marquee.attr("direction", "left");        			
	    		}
	    		if (value === 'newsdir_right'){
	        		marquee.attr("direction", "right");        			
	    		}        		
	    		
	    	}
	    } else {
	        this.$target.removeClass('newsdir_left newsdir_right');
	    }
	},    	
		

	//for number of news (rows) display in marquee
	selectClass: function (previewMode, value, $li) {
	    this._super.apply(this, arguments);

	    if(value && value.length){
	    	var val_2 = value;
	    	var rows = val_2.replace("newscount_", "");
	    	var marquee = this.$target.find('div').children('marquee');
	        
	    	if(marquee){
	        	var old_dir = marquee.attr('direction');
	            var new_marquee = $('<marquee class="sh_nb_notice_board_main_vertical_marquee_cls_1 sh_vertical_marquee col-lg-12" direction="left" onmouseover="this.stop();" onmouseout="this.start();"></marquee>');    
	            new_marquee.attr('direction', old_dir);
	            
	            
	            ajax.jsonRpc('/get_latest_news', 'call', {
	            	limit:  parseInt(rows),
	                })
	            .then(function (data) {
	                _.each(data, function (news) {
	                	new_marquee.append(
	                            "<div class='sh_news'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>"
	                    	);
	                });
	            });                
	            marquee.replaceWith(new_marquee);     
	        	
	        }

	    }
	    
	},    

	});


//for vertical snippet 2
options.registry.sh_nb_notice_board_vertical_sec_editor_js_2 = options.Class.extend({
	
	//for add marque direction classes.	
	direction: function (previewMode, value, $li) {
	    if (value && value.length) {
	        this.$target.removeClass('newsdir_left newsdir_right').addClass(value);
	    	var marquee = this.$target.find('div').children('marquee');
	    	if(marquee){
	    		
	    		if (value === 'newsdir_left'){
	        		marquee.attr("direction", "left");        			
	    		}
	    		if (value === 'newsdir_right'){
	        		marquee.attr("direction", "right");        			
	    		}        		
	    		
	    	}
	    } else {
	        this.$target.removeClass('newsdir_left newsdir_right');
	    }
	},    	
		

	//for number of news (rows) display in marquee
	selectClass: function (previewMode, value, $li) {
	    this._super.apply(this, arguments);

	    if(value && value.length){
	    	var val_2 = value;
	    	var rows = val_2.replace("newscount_", "");
	    	var marquee = this.$target.find('div').children('marquee');
	        
	    	if(marquee){
	        	var old_dir = marquee.attr('direction');
	            var new_marquee = $('<marquee class="sh_nb_notice_board_main_vertical_marquee_cls_2 sh_vertical_marquee col-lg-12" direction="left" onmouseover="this.stop();" onmouseout="this.start();"></marquee>');    
	            new_marquee.attr('direction', old_dir);
	            
	            
	            ajax.jsonRpc('/get_latest_news', 'call', {
	            	limit:  parseInt(rows),
	                })
	            .then(function (data) {
	                _.each(data, function (news) {
	                	new_marquee.append(
	        		            "<div class='sh_news_box'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>"
	                    	);
	                });
	            });                
	            marquee.replaceWith(new_marquee);     
	        	
	        }

	    }
	    
	},    

	});



//for vertical snippet 3
options.registry.sh_nb_notice_board_vertical_sec_editor_js_3 = options.Class.extend({
	
	//for add marque direction classes.	
	direction: function (previewMode, value, $li) {
	    if (value && value.length) {
	        this.$target.removeClass('newsdir_left newsdir_right').addClass(value);
	    	var marquee = this.$target.find('div').children('marquee');
	    	if(marquee){
	    		
	    		if (value === 'newsdir_left'){
	        		marquee.attr("direction", "left");        			
	    		}
	    		if (value === 'newsdir_right'){
	        		marquee.attr("direction", "right");        			
	    		}        		
	    		
	    	}
	    } else {
	        this.$target.removeClass('newsdir_left newsdir_right');
	    }
	},    	
		

	//for number of news (rows) display in marquee
	selectClass: function (previewMode, value, $li) {
	    this._super.apply(this, arguments);

	    if(value && value.length){
	    	var val_2 = value;
	    	var rows = val_2.replace("newscount_", "");
	    	var marquee = this.$target.find('div').children('marquee');
	        
	    	if(marquee){
	        	var old_dir = marquee.attr('direction');
	            var new_marquee = $('<marquee class="sh_nb_notice_board_main_vertical_marquee_cls_3 col-lg-12" direction="left" onmouseover="this.stop();" onmouseout="this.start();"></marquee>');    
	            new_marquee.attr('direction', old_dir);
	            
	            
	            ajax.jsonRpc('/get_latest_news', 'call', {
	            	limit:  parseInt(rows),
	                })
	            .then(function (data) {
	                _.each(data, function (news) {
	                	new_marquee.append(
	        		            "<div class='sh_news_box'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>"
	                    	);
	                });
	            });                
	            marquee.replaceWith(new_marquee);     
	        	
	        }

	    }
	    
	},    

	});



});


