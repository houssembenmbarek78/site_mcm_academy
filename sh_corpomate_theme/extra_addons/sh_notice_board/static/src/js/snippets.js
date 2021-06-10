odoo.define('sh_notice_board.snippets', function (require) {
    "use strict";

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Animation = require('website.content.snippets.animation');
    var _t = core._t;

    Animation.registry.sh_nb_notice_board_horizontal_tmpl_1 = Animation.Class.extend({
        selector: '.sh_nb_notice_board_main_horizontal_marquee_cls_1',
        start: function () {
            //var defs = [this._super.apply(this, arguments)];
        	var self = this;
           
        	var section_classes = false;
        	var rows = 3;
        	if(this.$el.parents('section').attr('class')){
        		section_classes = this.$el.parents('section').attr('class');
        	}
  
        	if(section_classes){
        		var pos = section_classes.search("newscount_");
 
  			  	if (pos != -1){
  			  		var newscount_cls = section_classes.substring(pos,pos + 12);
  		        	var rows = newscount_cls.replace("newscount_", "");  			  		
  			  	} 		
        		
        	}

            //this.$el.find('a').parents('span').remove();
        	this.$el.find('span').remove();
        	
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })  
            .then(function (data) {
                _.each(data, function (news) {
                    self.$el.append(
                    		"<span>" + news.desc + "</span>"
                            
                        );
                });
            });
        },
    });
    
    //For horizontal snippets 2
    
    Animation.registry.sh_nb_notice_board_horizontal_tmpl_2 = Animation.Class.extend({
        selector: '.sh_nb_notice_board_main_horizontal_marquee_cls_2',
        start: function () {
            //var defs = [this._super.apply(this, arguments)];
        	var self = this;
           
        	var section_classes = false;
        	var rows = 3;
        	if(this.$el.parents('section').attr('class')){
        		section_classes = this.$el.parents('section').attr('class');
        	}
  
        	if(section_classes){
        		var pos = section_classes.search("newscount_");
 
  			  	if (pos != -1){
  			  		var newscount_cls = section_classes.substring(pos,pos + 12);
  		        	var rows = newscount_cls.replace("newscount_", "");  			  		
  			  	} 		
        		
        	}

            //this.$el.find('a').parents('span').remove();
        	this.$el.find('div').remove();
        	
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })  
            .then(function (data) {
                _.each(data, function (news) {
                    self.$el.append(
                            "<div class='sh_text'><span class='fa fa-caret-right' aria-hidden='true'> </span>"+ news.desc + "</div>"                            
                        );
                });
            });
        },
    });    
    
    
    //For horizontal snippets 3
    
    Animation.registry.sh_nb_notice_board_horizontal_tmpl_3 = Animation.Class.extend({
        selector: '.sh_nb_notice_board_main_horizontal_marquee_cls_3',
        start: function () {
            //var defs = [this._super.apply(this, arguments)];
        	var self = this;
           
        	var section_classes = false;
        	var rows = 3;
        	if(this.$el.parents('section').attr('class')){
        		section_classes = this.$el.parents('section').attr('class');
        	}
  
        	if(section_classes){
        		var pos = section_classes.search("newscount_");
 
  			  	if (pos != -1){
  			  		var newscount_cls = section_classes.substring(pos,pos + 12);
  		        	var rows = newscount_cls.replace("newscount_", "");  			  		
  			  	} 		
        		
        	}

            //this.$el.find('a').parents('span').remove();
        	this.$el.find('div').remove();
        	
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })  
            .then(function (data) {
                _.each(data, function (news) {
                    self.$el.append(
                            "<div class='sh_news_description'><span class='fa fa-caret-right'> </span>"+ news.desc + "</div>"                         
                        );
                });
            });
        },
    });       
    
    
    
    // ===========================================
    // for vertical snippets
    // ===========================================
    
    //For vertical snippet 1 
    Animation.registry.sh_nb_notice_board_vertical_tmpl_1 = Animation.Class.extend({
        selector: '.sh_nb_notice_board_main_vertical_marquee_cls_1',
        start: function () {
            //var defs = [this._super.apply(this, arguments)];
        	var self = this;
           
        	var section_classes = false;
        	var rows = 3;
        	if(this.$el.parents('section').attr('class')){
        		section_classes = this.$el.parents('section').attr('class');
        	}
  
        	if(section_classes){
        		var pos = section_classes.search("newscount_");
 
  			  	if (pos != -1){
  			  		var newscount_cls = section_classes.substring(pos,pos + 12);
  		        	var rows = newscount_cls.replace("newscount_", "");  			  		
  			  	} 		
        		
        	}

            //this.$el.find('a').parents('span').remove();
        	this.$el.find('div').remove();
        	
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })  
            .then(function (data) {
                _.each(data, function (news) {
                    self.$el.append(
                            "<div class='sh_news'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>"                    
                        );
                });
            });
        },
    });
    
    
    //For vertical snippet 2
    Animation.registry.sh_nb_notice_board_vertical_tmpl_2 = Animation.Class.extend({
        selector: '.sh_nb_notice_board_main_vertical_marquee_cls_2',
        start: function () {
            //var defs = [this._super.apply(this, arguments)];
        	var self = this;
           
        	var section_classes = false;
        	var rows = 3;
        	if(this.$el.parents('section').attr('class')){
        		section_classes = this.$el.parents('section').attr('class');
        	}
  
        	if(section_classes){
        		var pos = section_classes.search("newscount_");
 
  			  	if (pos != -1){
  			  		var newscount_cls = section_classes.substring(pos,pos + 12);
  		        	var rows = newscount_cls.replace("newscount_", "");  			  		
  			  	} 		
        		
        	}

            //this.$el.find('a').parents('span').remove();
        	this.$el.find('div').remove();
        	
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })  
            .then(function (data) {
                _.each(data, function (news) {
                    self.$el.append(
        		            "<div class='sh_news_box'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>"
                        );
                });
            });
        },
    });       
    
    
    //For vertical snippet 3
    Animation.registry.sh_nb_notice_board_vertical_tmpl_3 = Animation.Class.extend({
        selector: '.sh_nb_notice_board_main_vertical_marquee_cls_3',
        start: function () {
            //var defs = [this._super.apply(this, arguments)];
        	var self = this;
           
        	var section_classes = false;
        	var rows = 3;
        	if(this.$el.parents('section').attr('class')){
        		section_classes = this.$el.parents('section').attr('class');
        	}
  
        	if(section_classes){
        		var pos = section_classes.search("newscount_");
 
  			  	if (pos != -1){
  			  		var newscount_cls = section_classes.substring(pos,pos + 12);
  		        	var rows = newscount_cls.replace("newscount_", "");  			  		
  			  	} 		
        		
        	}

            //this.$el.find('a').parents('span').remove();
        	this.$el.find('div').remove();
        	
            ajax.jsonRpc('/get_latest_news', 'call', {
            	limit:  parseInt(rows),
                })  
            .then(function (data) {
                _.each(data, function (news) {
                    self.$el.append(
        		            "<div class='sh_news_box'><h4>" + news.name + "</h4><p>" + news.desc + "</p></div>"
                        );
                });
            });
        },
    });         
    

});
