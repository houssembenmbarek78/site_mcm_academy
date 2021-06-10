odoo.define('sh_corpomate_theme.slider', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var _t = core._t;


var qweb = core.qweb;



//A $( document ).ready() block.
$( document ).ready(function() {
//document ready start here.


	

	
	
	
	
	/*
	 * ----------------------------------------------------------------------------------------------------------------------------------------------
	 * BLOG THINGS
	 * ----------------------------------------------------------------------------------------------------------------------------------------------
	 */	
		
		


	
	
	
		
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 1
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_202_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_202_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_202').replaceWith(values.data);
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_202");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_202_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_202').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_202 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_202_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_202 ' + tab_href_find ).replaceWith(values.data);
		   		        

		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 1
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		
			
		
		
		
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
	
		
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 2
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_203_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_203_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_203').replaceWith(values.data);
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_203");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_203_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_203').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_203 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_203_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_203 ' + tab_href_find ).replaceWith(values.data);
		   		        

		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 2
		 * **************************************
		 * ###################################################################################		
		 */
		
		
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 3
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_204_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_204_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_204').replaceWith(values.data);
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_204");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_204_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_204').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_204 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_204_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_204 ' + tab_href_find ).replaceWith(values.data);
		   		        

		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 3
		 * **************************************
		 * ###################################################################################		
		 */
		
		
				
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 4
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_205_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_205_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_205').replaceWith(values.data);
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_205");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_205_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_205').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_205 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_205_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_205 ' + tab_href_find ).replaceWith(values.data);
		   		        

		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 4
		 * **************************************
		 * ###################################################################################		
		 */
		
		
				
						
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 5
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_206_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_206_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_206').replaceWith(values.data);
		   		    	var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
	                        
	                        
			   		      });  	               
		               
			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_206");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_206_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_206').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_206 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_206_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_206 ' + tab_href_find ).replaceWith(values.data);
		   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
		   		    	
		   		    	
		   		    	
		   		    	
			   		      });  	               
		               
			   		   //refresh the own ends here	
		   		    	
		   		    	
		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 5
		 * **************************************
		 * ###################################################################################		
		 */
		
		
				
						
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 6 template 207
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_207_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_207_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_207').replaceWith(values.data);
		   		    	var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
	                        
	                        
			   		      });  	               
		               
			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_207");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_207_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_207').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_207 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_207_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_207 ' + tab_href_find ).replaceWith(values.data);
		   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
		   		    	
		   		    	
		   		    	
		   		    	
			   		      });  	               
		               
			   		   //refresh the own ends here	
		   		    	
		   		    	
		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 6 template 207
		 * **************************************
		 * ###################################################################################		
		 */
		
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 7 template 208
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_208_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_208_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_208').replaceWith(values.data);
		   		    	var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
							rtl:is_rtl_enabled,     
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:3
	                	        }
	                	    }	
	                        
	                        
			   		      });  	               
		               
			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_208");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_208_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_208').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_208 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_208_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_208 ' + tab_href_find ).replaceWith(values.data);
		   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:3
	                	        }
	                	    }	
		   		    	
		   		    	
		   		    	
		   		    	
			   		      });  	               
		               
			   		   //refresh the own ends here	
		   		    	
		   		    	
		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 7 template 208
		 * **************************************
		 * ###################################################################################		
		 */
		
		
					
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 8 template 209
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_209_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_209_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_209').replaceWith(values.data);
		   		    	var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
	                        
	                        
			   		      });  	               
		               
			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_209");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_209_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_209').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_209 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_209_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_209 ' + tab_href_find ).replaceWith(values.data);
		   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
		   		    	
		   		    	
		   		    	
		   		    	
			   		      });  	               
		               
			   		   //refresh the own ends here	
		   		    	
		   		    	
		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 8 template 209
		 * **************************************
		 * ###################################################################################		
		 */
		
		
					
		
		
		
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 9 template 210
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_210_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_210_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_210').replaceWith(values.data);
		   		    	var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
	                        
	                        
			   		      });  	               
		               
			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_210");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_210_layout( $( this )  );
			

		});
			
		}	
		
		
		
		//ON CLICK SLIDER TAB PANE.
		$('.js_cls_corpomate_blog_slider_section_210').on('click','.js_cls_corpomate_blog_slider_nav_tabs_ul_210 a',function (e) {
		    e.preventDefault();
		    

		    
	        var $tab = $(e.currentTarget);
	        var $el = $tab.closest('section')	    
		    
		    var tab_href = $(this).attr('href');
	     
		    var tab_href_find = $(this).attr('href');
		    var token = tab_href.replace("#nav_tab_", '');
		    
		    var tab_id = $(this).attr('data-tab_id');
		    
	    	
	    	var class_name = $el.attr('class');
	    	
		    
	    	if(class_name){
	    		
	    		//DO NOTHING FOR BLOG RIGHT NOW.
	    	}		    
		    
		    	    
		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_210_tab_pane_one', 'call', 
		       	 	{       
			    		'tab_id':	tab_id,	
			    		'token':	token,		    				    		
		    		
		   		    }).then(function (values) {

		   		    	
		   		    	$el.find('.js_cls_corpomate_blog_slider_tab_content_210 ' + tab_href_find ).replaceWith(values.data);
		   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
		   		    	//refresh the owl start here
		   		    	$el.find('.owl-carousel').owlCarousel({
	                        items:		values.items,
	                        autoplay:	values.autoplay,
	                        speed:		values.speed,
	                        loop:		values.loop,
	                        nav:		values.nav,                        
	                        rtl:is_rtl_enabled,      
	                	    responsive:{
	                	        0:{
	                	            items:1
	                	        },
	                	        600:{
	                	            items:1
	                	        },
	                	        1000:{
	                	            items:2
	                	        }
	                	    }	
		   		    	
		   		    	
		   		    	
		   		    	
			   		      });  	               
		               
			   		   //refresh the own ends here	
		   		    	
		   		    	
		            });  
			
			//then function ends here
		    

		});		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 9 template 210
		 * **************************************
		 * ###################################################################################		
		 */
		
		
					
		
		
		
			
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 10 template 263 theme 10
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_263_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_263_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_263').replaceWith(values.data);
		   		    	
		   		    	//refresh the owl start here

			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_263");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_263_layout( $( this )  );
			

		});
			
		}	
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 10 template 263 theme 10
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		
		
		
				
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 11 template 280 theme 11
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_280_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_280_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_280').replaceWith(values.data);
		   		    	
		   		    	//refresh the owl start here

			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_280");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_280_layout( $( this )  );
			

		});
			
		}	
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 11 template 280 theme 11
		 * **************************************
		 * ###################################################################################		
		 */
		
		
				
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 12 template 298 theme 12
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_298_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_298_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_298').replaceWith(values.data);
		   		    	
		   		    	//refresh the owl start here

			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_298");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_298_layout( $( this )  );
			

		});
			
		}	
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 12 template 298 theme 12
		 * **************************************
		 * ###################################################################################		
		 */
		
		
				
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 13 template 323 theme 13
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_323_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_323_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_323').replaceWith(values.data);
		   		    	
		   		    	//refresh the owl start here

			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_323");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_323_layout( $( this )  );
			

		});
			
		}	
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 13 template 323 theme 13
		 * **************************************
		 * ###################################################################################		
		 */
		
		
						
		
		
		
		
		
		
		
		
		
		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 14 template 348 theme 14
		 * **************************************
		 * ###################################################################################		
		 */
		
		
		
		
		// BLOG SLIDER LAYOUT render function start here
		function sh_corpomate_theme_tmpl_348_layout($el) {
			
			//get snippet options start here    	 	
	    	var class_name = $el.attr('class');
		    var slider_id = false;
		    	
	    	
	 	    		    	
		    	if(class_name){

		    		
		    		//for slider 
		    		var js_slider_id = class_name.match("sh_slider_(.*)_send");
		
		    		
		    		if(js_slider_id && js_slider_id.length == 2){
		    			slider_id = js_slider_id[1];
		    		} 	
		    		
		    			    		
		    	}		
			
			
			//get snippet option ends here		

		    //ajax call start here	
			ajax.jsonRpc('/sh_corpomate_theme/sh_tab_slider_snippet/sh_corpomate_theme_tmpl_348_tab_pane_layout', 'call', 
		       	 	{       
			    		'slider_id': 			slider_id,	    		
			    		
		   		    }).then(function (values) {

		   		    	$el.find('.js_cls_corpomate_blog_slider_main_div_348').replaceWith(values.data);
		   		    	
		   		    	//refresh the owl start here

			   		   //refresh the own ends here			   		    	
		   		    	
		   		        
		            });  
			
			//then function ends here
				
	        
	    }
		// blog LAYOUT render function ends here		
		
		
		
		var $snippet_sections = $(".js_cls_corpomate_blog_slider_section_348");
		
		if($snippet_sections && $snippet_sections.length){
			
			$snippet_sections.each(function( index ) {
				
				sh_corpomate_theme_tmpl_348_layout( $( this )  );
			

		});
			
		}	
		
		

		
		
		
		/* 
		 * ###################################################################################
		 * ***************************************
		 * blog 14 template 348 theme 14
		 * **************************************
		 * ###################################################################################		
		 */
		
		
						
			
				
		
		
		

	
	
		
//document ready ends here.
		
});





});