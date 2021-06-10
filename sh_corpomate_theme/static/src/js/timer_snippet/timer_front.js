odoo.define('sh_corpomate_theme.timer_front', function (require) {
'use strict';

var ajax = require('web.ajax');
var core = require('web.core');
var _t = core._t;
var qweb = core.qweb;



//A $( document ).ready() block.
$( document ).ready(function() {

//DOCUMENT READY START HERE
    
    

	
	/*
	 * ###############################################
	 * TIMER sh_timer_snippet_tmpl_173
	 * ###############################################
	 */
	function sh_timer_snippet_tmpl_173($el) {
	
    	//self.$target.attr("data-date_start", date_start);
    	//self.$target.attr("data-date_end",date_end );
    	var date_start = $el.attr("data-date_start");
    	var date_end = $el.attr("data-date_end");
    	

    	//IF HAS START DATE AND END DATE.
    	if(date_start && date_end){

			// Get today's date and time
			var now = new Date().getTime();
			  
			var var_date_start = new Date(date_start); //dd-mm-YYYY
			var var_date_end = new Date(date_end); //dd-mm-YYYY
			var today = new Date();

			var_date_start.setHours(0,0,0,0);
			var_date_end.setHours(0,0,0,0);			
			today.setHours(0,0,0,0);
					
			
			if(var_date_start <= today && var_date_end >= today ) {
				//SHOW COUNTER AND LOOP INTERVAL
				
				// Update the count down every 1 second
				var EcomateTimerInterval = setInterval(function() {

				  // Get today's date and time
				  var now = new Date().getTime();

				  // Find the distance between now and the count down date
				  var distance = var_date_end.getTime() - now;

				  // Time calculations for days, hours, minutes and seconds
				  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
				  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
				  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
				  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
				  
				  	//IF VALUE IS ONE DIGIT THEN CONVER IT TO 2 DIGIT ADD ZERO BEFORE.
					if ((days+'').length == 1) {
						days = "0" + days;
					}
					if ((hours+'').length == 1) {
						hours = "0" + hours;
					}					
					if ((minutes+'').length == 1) {
						minutes = "0" + minutes;
					} 	
				    if ((seconds+'').length == 1) {
						seconds = "0" + seconds;
					}					
				    
				    days = days + '<br/><span>Days</span>';
				    hours = hours + '<br/><span>Hours</span>';
				    minutes = minutes + '<br/><span>Minutes</span>';
				    seconds = seconds + '<br/><span>Seconds</span>';
				    
				    //ASSIGN VALUE TO SNIPPET ELEMENT.
				    $el.find(".sh_corpomate_timer_day_counter").html(days);
				    $el.find(".sh_corpomate_timer_hour_counter").html(hours);				    
				    $el.find(".sh_corpomate_timer_minute_counter").html(minutes);
				    $el.find(".sh_corpomate_timer_second_counter").html(seconds);				    

				    // If the count down is finished, 

				    if (distance < 0) {
				        clearInterval(EcomateTimerInterval);
					    // HIDE COUNTER
				        $el.find(".sh_corpomate_counter_timer_main_div").hide();

				    }
					  
				  
				}, 1000);				
				
				
				
				
			}else{
				//HIDE COUNTER
		        $el.find(".sh_corpomate_counter_timer_main_div").hide();
			}		
			
			
    	}else{
    		//HIDE COUNTER
	        $el.find(".sh_corpomate_counter_timer_main_div").hide();
    	}
    	
    	
		
    }
	// RENDER FUNCTION ENDS HERE
	
    
    //IF TARGETED TIMER SNIPPET EXIST IN PAGE.
	var $snippet_timer = $(".js_cls_sh_corpomate_section_173");
	if($snippet_timer && $snippet_timer.length){
		$snippet_timer.each(function( index ) {
			sh_timer_snippet_tmpl_173( $( this ) );
		

	});
		
	}	
	
	/*
	 * ###############################################
	 * TIMER sh_timer_snippet_tmpl_173
	 * ###############################################
	 */
	
	
		
	
	
	
	
	
    
// DOCUMENT READY ENDS HERE
});



});