odoo.define('sh_website_quote.sh_contact_us', function(require) 
{
	
	var core = require('web.core');
	var session = require('web.session');
	var time = require('web.time');

	var QWeb = core.qweb;	
	var ajax = require('web.ajax');
 	
 	$(document).ready(function() 
	{		
 		/* 
 		$('#product_req_quote_modal').on('shown.bs.modal', function() 
		{	  
 			$('input[name="inputquantity"]').focus();
		});
		*/
 		
		$("#sh_wq_website_quote_form").submit(function(e) 
		{
			e.preventDefault();			
			
	    	
			var result =  ajax.jsonRpc('/sh_website_quote/contact_us', 'call', 
    	 	{        
    	           
    	           'contact_name' : $('input[name="contact_name"]').val(),
    	           'phone'        : $('input[name="phone"]').val(),
    	           'email_from'   : $('input[name="email_from"]').val(),
                   'partner_name' : $('input[name="partner_name"]').val(),  	           
    	           'name'         : $('input[name="name"]').val(),
    	           'description'  : $('textarea[name="description"]').val(),           
    	        	   
    	        	  
    	           
    	   	}).then(function (result)
    		{
    	      		if (result)
    				{    	       			
//    	       			$("#product_req_quote_modal .closemodel").click();
    	       			
    	      			
    	      			$("#sh_wq_website_quote_form").hide();
    	      			$("#sh_wq_website_quote_thankyou_msg").show();
    	      			$("#sh_wq_website_quote_thankyou_msg").html('<div class="alert alert-success"><strong>Your message has been sent successfully. We will get back to you shortly.</strong></div>');
    	       			
    				}
    	      		else
    				{
//    	       			$("#product_req_quote_modal .closemodel").click();
    	      			$("#sh_wq_website_quote_thankyou_msg").show();    	      			
    	      			$("#sh_wq_website_quote_thankyou_msg").html('<div class="alert alert-danger"><strong>Failure to request a quote.</strong></div>');    	      				
    				}   
			});		    
	    	return false;
		});		
	}); 	
    
});










