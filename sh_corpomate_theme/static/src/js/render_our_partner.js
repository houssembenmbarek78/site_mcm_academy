odoo.define('sh_ecommerce_snippet.our_partner', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var _t = core._t;


var qweb = core.qweb;


//A $( document ).ready() block.
$( document ).ready(function() {


		
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_9 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_9($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_9",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: false,
		   		        autoplayTimeout : 5000,
		   		        loop: true,
		   		        nav: true,
		   		        items : 4,        
		   		        navigation : true,
						rtl:is_rtl_enabled,
		   		        responsive:{
		   		            0:{
		   		                items:1,
		   		                nav:true
		   		            },
		   		            600:{
		   		                items:3,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:5,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_9");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_9( $( this ) );
		

	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_9 JS ends here
	 * **************************************
	 */		
	

	 
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_18 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_18($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_18",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: false,
		   		        autoplayTimeout : 5000,
		   		        loop: true,
		   		        nav: true,
		   		        items : 4,        
		   		        navigation : true,
						rtl:is_rtl_enabled,
		   		        responsive:{
		   		            0:{
		   		                items:1,
		   		                nav:true
		   		            },
		   		            600:{
		   		                items:3,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:5,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_18");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_18( $( this ) );
	
	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_18 JS ends here
	 * **************************************
	 */
	
	 
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_36 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_36($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_36",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: false,
		   		        autoplayTimeout : 5000,
		   		        loop: true,
		   		        nav: true,
		   		        items : 4,        
		   		        navigation : true,
						rtl:is_rtl_enabled,
		   		        responsive:{
		   		            0:{
		   		                items:1,
		   		                nav:true
		   		            },
		   		            600:{
		   		                items:3,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:4,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_36");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_36( $( this ) );
	
	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_36 JS ends here
	 * **************************************
	 */
	
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_42 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_42($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_42",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: false,
		   		        autoplayTimeout : 5000,
		   		        loop: true,
		   		        nav: true,
		   		        items : 4,        
		   		        navigation : true,
						rtl:is_rtl_enabled,
		   		        responsive:{
		   		            0:{
		   		                items:1,
		   		                nav:true
		   		            },
		   		            600:{
		   		                items:3,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:5,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_42");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_42( $( this ) );	
	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_42 JS ends here
	 * **************************************
	 */
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_169 PARTNER
	 * ####################################################################################################
	 */	
	

	//render function start here
	function sh_corpomate_theme_tmpl_169($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_169",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		 		items:5,
		   			    loop:true,
		   			    margin:10,
		   			    autoplay:true,	   
		   			    autoplaySpeed:1000,
						rtl:is_rtl_enabled,
		   			    responsive:{
		   			        0:{
		   			            items:1
		   			        },
		   			        600:{
		   			            items:3
		   			        },
		   			        1000:{
		   			            items:5
		   			        }
		   			    }		
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_169");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_169( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_169 PARTNER
	 * ####################################################################################################
	 */	
	
	
	
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_178 PARTNER
	 * ####################################################################################################
	 */	
	

	//render function start here
	function sh_corpomate_theme_tmpl_178($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_178",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		 		items:5,
		   			    loop:true,
		   			    margin:10,
		   			    autoplay:true,	   
		   			    autoplaySpeed:1000,
						rtl:is_rtl_enabled,
		   			    responsive:{
		   			        0:{
		   			            items:1
		   			        },
		   			        600:{
		   			            items:3
		   			        },
		   			        1000:{
		   			            items:5
		   			        }
		   			    }		
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_178");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_178( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_178 PARTNER
	 * ####################################################################################################
	 */		
	
	
	
	
	
	
	
	
	
	
	
	
	

	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_191 PARTNER
	 * ####################################################################################################
	 */	
	

	//render function start here
	function sh_corpomate_theme_tmpl_191($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_191",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		 		items:5,
		   			    loop:true,
		   			    margin:10,
		   			    autoplay:true,	   
		   			    autoplaySpeed:1000,
						rtl:is_rtl_enabled,
		   			    responsive:{
		   			        0:{
		   			            items:1
		   			        },
		   			        600:{
		   			            items:3
		   			        },
		   			        1000:{
		   			            items:5
		   			        }
		   			    }		
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_191");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_191( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_191 PARTNER
	 * ####################################################################################################
	 */		
		
	
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_264 PARTNER
	 * ####################################################################################################
	 */	
	

	//render function start here
	function sh_corpomate_theme_tmpl_264($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_our_partner', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_264",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({

	   		    		items:5,
	   		    	    loop:true,
	   		    	    margin:10,
	   		    	    autoplay:true,	   
	   		    	    autoplaySpeed:1000,
						rtl:is_rtl_enabled,
	   		    	    responsive:{
	   		    	        0:{
	   		    	            items:1
	   		    	        },
	   		    	        600:{
	   		    	            items:2
	   		    	        },
	   		    	        1000:{
	   		    	            items:5
	   		    	        }
	   		    	    }	
	   		    	
	   		    		
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_264");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
						
			sh_corpomate_theme_tmpl_264( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_264 PARTNER
	 * ####################################################################################################
	 */		
		
	
	
	
	
	
	
	
	
		
//document ready ends here.
		
});





});