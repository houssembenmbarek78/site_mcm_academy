odoo.define('sh_ecommerce_snippet.Testimonial', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var _t = core._t;


var qweb = core.qweb;


//A $( document ).ready() block.
$( document ).ready(function() {


		
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_23 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_23($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_23",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: true,
		   		        autoplayTimeout : 5000,
		   		        loop: true,
		   		        nav: true,
		   		        items : 4,
		   		        margin: 10,
		   		        navigation : true,
						rtl:is_rtl_enabled,
		   		        responsive:{
		   		            0:{
		   		                items:1,
		   		                nav:true
		   		            },
		   		            600:{
		   		                items:1,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:2,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_23");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_23( $( this ) );
		

	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_23 JS ends here
	 * **************************************
	 */		
	

	        		
	
	
	
	
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_6 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_6($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_6",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: true,
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
		   		                items:1,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:1,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_6");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_6( $( this ) );
		

	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_6 JS ends here
	 * **************************************
	 */		
	
	 
	
	
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_16 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_16($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_16",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: true,
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
		   		                items:1,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:1,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_16");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_16( $( this ) );		

	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_16 JS ends here
	 * **************************************
	 */
	
	
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_32 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_32($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_32",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
		   		        autoplay: true,
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
		   		                items:1,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:2,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_32");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_32( $( this ) );	
	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_32 JS ends here
	 * **************************************
	 */
	
	
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_41 JS start here
	 * **************************************
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_41($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_41",
		    				    		
	    		
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
		   		                items:1,
		   		                nav:false
		   		            },
		   		            1000:{
		   		                items:2,
		   		                nav:true,                
		   		            }
		   		        }   
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_41");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_41( $( this ) );	
	});
		
	}
	
	/*
	 * ***************************************
	 * sh_corpomate_theme_tmpl_41 JS ends here
	 * **************************************
	 */
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_168 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_168($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_168",
		    				    		
	    		
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
		   			            items:1
		   			        },
		   			        1000:{
		   			            items:1
		   			        }
		   			    }	 
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_168");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_168( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_168 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_177 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_177($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_177",
		    				    		
	    		
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
		   			            items:2
		   			        }
		   			    }	 
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_177");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_177( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_tmpl_177 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_239 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_239($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_239",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
	   		    		
	   		    		items:3,
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
	   		    	            items:1
	   		    	        },
	   		    	        1000:{
	   		    	            items:1
	   		    	        }
	   		    	    }	
	   		    	
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_239");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_239( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_239 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_259 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_tmpl_259($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_259",
		    				    		
	    		
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
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_259");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_tmpl_259( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_259 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_281 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_281($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_281",
		    				    		
	    		
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
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_281");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_281( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_281 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	
			
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_297 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_297($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_297",
		    				    		
	    		
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
	   		    	            items:2
	   		    	        }
	   		    	    }	
	   		    	
	   		    	
	   		    	
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_297");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_297( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_297 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	
			
	
		
	
	
	
	
	
	
	
	
	
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_322 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_322($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_322",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
	   		    		
	   		 		items:1,
	   			    loop:true,
	   			    margin:10,
	   			    navs: false,
	   			    dots: false,
	   			    autoplay: true,	   
	   			    autoplaySpeed:2000,
					rtl:is_rtl_enabled,
	   			    responsive:{
	   			        0:{
	   			            items:1
	   			        },
	   			        600:{
	   			            items:1
	   			        },
	   			        1000:{
	   			            items:1
	   			        }
	   			    }	
	   		    	
	   		    	
	   		    	
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_322");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_322( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_322 TESTIMONIAL
	 * ####################################################################################################
	 */	
	
	


	 /* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_347 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_347($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_347",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
	   		    		
	   		 		items:1,
	   			    loop:true,
	   			    margin:10,
	   			    navs: false,
	   			    dots: false,
	   			    autoplay: true,	   
	   			    autoplaySpeed:2000,
					rtl:is_rtl_enabled,
	   			    responsive:{
	   			        0:{
	   			            items:1
	   			        },
	   			        600:{
	   			            items:1
	   			        },
	   			        1000:{
	   			            items:1
	   			        }
	   			    }	
	   		    	
	   		    	
	   		    	
		   		      });  	               
	               
		   		   //refresh the own ends here
	            });  
		
		//then function ends here
			
        
    }
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_347");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_347( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_347 TESTIMONIAL
	 * ####################################################################################################
	 */	



	 /* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_347 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_352($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_352",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
	   		    		
	   		 		items:1,
	   			    loop:true,
	   			    margin:10,
	   			    navs: false,
	   			    dots: false,
	   			    autoplay: true,	   
	   			    autoplaySpeed:2000,
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
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_352");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_352( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_347 TESTIMONIAL
	 * ####################################################################################################
	 */	
				
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_371 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_371($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_371",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        var is_rtl_enabled =  $('#wrapwrap').hasClass('o_rtl');
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
	   		    		
	   		 		items:1,
	   			    loop:true,
	   			    margin:10,
	   			    navs: true,
	   			    dots: false,
	   			    autoplay: true,	   
	   			    autoplaySpeed:2000,
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
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_371");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_371( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_371 TESTIMONIAL
	 * ####################################################################################################
	 */
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_394 TESTIMONIAL
	 * ####################################################################################################
	 */	

	//render function start here
	function sh_corpomate_theme_section_394($el) {
		//get snippet options start here    	

		
		//get snippet option ends here		

	    //ajax call start here	
		ajax.jsonRpc('/sh_corpomate_theme/render_testimonial', 'call', 
	       	 	{       

		    		'template_id': "sh_corpomate_theme.sh_corpomate_theme_item_394",
		    				    		
	    		
	   		    }).then(function (data) {
	   		    	$el.find('.owl-carousel').replaceWith(data);
	   		        
	   		    	//refresh the owl start here
	   		    	$el.find('.owl-carousel').owlCarousel({
	   		    		
	   		 		items:1,
	   			    loop:true,
	   			    margin:10,
	   			    navs: true,
	   			    dots: false,
	   			    autoplay: true,	   
	   			    autoplaySpeed:2000,
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
	//render function ends here
	
	var $snippet_sections = $(".js_cls_sh_corpomate_theme_section_394");
	if($snippet_sections && $snippet_sections.length){
		$snippet_sections.each(function( index ) {
			sh_corpomate_theme_section_394( $( this ) );	
	});
		
	}
	
	/* 
	 * ####################################################################################################
	 * sh_corpomate_theme_section_394 TESTIMONIAL
	 * ####################################################################################################
	 */
	
	
	
		
//document ready ends here.
		
});





});