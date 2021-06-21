// start of coming soon js 1
$( document ).ready(function() {

function makeTimer() {
			
	
			
			var launch_date = $("#sh_website_coming_soon_section_1 .sh_website_coming_soon_hidden_date_1").text();
							
			launch_date = String(launch_date);
			launch_date = launch_date.trim();		
//			launch_date = launch_date.slice(0, 10);		

						
			var endTime = new Date(launch_date);		
			endTime = (Date.parse(endTime) / 1000);
		
			var now = new Date();
			now = (Date.parse(now) / 1000);

			var timeLeft = endTime - now;
	
			var days = Math.floor(timeLeft / 86400); 
			var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
			var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
			var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
			days = Math.abs(days);

						
			if (hours < "10") { hours = "0" + hours; }
			if (minutes < "10") { minutes = "0" + minutes; }
			if (seconds < "10") { seconds = "0" + seconds; }

			
			
			$("#sh_website_coming_soon_section_1 .days").html(
				    '<div class="number">' + days  +  '</div><div class="label">Days</div>'					
					);				
			$("#sh_website_coming_soon_section_1 .hours").html(
				    '<div class="number">' + hours  +  '</div><div class="label">Hours</div>'					
					);	
			$("#sh_website_coming_soon_section_1 .minutes").html(
				    '<div class="number">' + minutes  +  '</div><div class="label">Minutes</div>'					
					);				
			$("#sh_website_coming_soon_section_1 .seconds").html(
				    '<div class="number">' + seconds  +  '</div><div class="label">Seconds</div>'					
					);		
	         }

	setInterval(function() { 
		makeTimer();
	}, 1000);
	
});	

// end of coming soon js 1


// start of coming soon js 2
$( document ).ready(function() {
	function makeTimer2() {

				var launch_date = $("#sh_website_coming_soon_section_2 .sh_website_coming_soon_hidden_date_2").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();					
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				

				
				$("#sh_website_coming_soon_section_2 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_2 .sh_hour").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_2 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_2 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer2();
		}, 1000);

});			
// end of coming soon js 2

	
// start of coming soon js 3
$( document ).ready(function() {
		function makeTimer3() {
			
			var launch_date = $("#sh_website_coming_soon_section_3 .sh_website_coming_soon_hidden_date_3").text();
			launch_date = String(launch_date);
			launch_date = launch_date.trim();					
			
			var endTime = new Date(launch_date);			
			endTime = (Date.parse(endTime) / 1000);

			var now = new Date();
			now = (Date.parse(now) / 1000);

			var timeLeft = endTime - now;

			var days = Math.floor(timeLeft / 86400); 
			var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
			var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
			var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
			days = Math.abs(days);
			
			if (seconds < "10") { seconds = "0" + seconds; }

		
			$("#sh_website_coming_soon_section_3 .sh_time").html(seconds);	
	         }

	setInterval(function() { 
		makeTimer3();
	}, 1000);	
	
});		
// end of coming soon js 3	
	
	
$( document ).ready(function() {	
// start of coming soon js 4
	function makeTimer4() {
				
				var launch_date = $("#sh_website_coming_soon_section_4 .sh_website_coming_soon_hidden_date_4").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();		
				
				var endTime = new Date(launch_date);			
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_4 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_4 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_4 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_4 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer4();
		}, 1000);
		
});			

// end of coming soon js 4


// start of coming soon js 5
$( document ).ready(function() {		
		function makeTimer5() {
					
					var launch_date = $("#sh_website_coming_soon_section_5 .sh_website_coming_soon_hidden_date_5").text();
					launch_date = String(launch_date);
					launch_date = launch_date.trim();							
					
					var endTime = new Date(launch_date);			
					endTime = (Date.parse(endTime) / 1000);

					var now = new Date();
					now = (Date.parse(now) / 1000);

					var timeLeft = endTime - now;

					var days = Math.floor(timeLeft / 86400); 
					var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
					var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
					var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
					days = Math.abs(days);
					
					if (hours < "10") { hours = "0" + hours; }
					if (minutes < "10") { minutes = "0" + minutes; }
					if (seconds < "10") { seconds = "0" + seconds; }

					
					
					$("#sh_website_coming_soon_section_5 .sh_days").html(
						    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
							);				
					$("#sh_website_coming_soon_section_5 .sh_hours").html(
						    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
							);	
					$("#sh_website_coming_soon_section_5 .sh_minutes").html(
						    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
							);				
					$("#sh_website_coming_soon_section_5 .sh_seconds").html(
						    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
							);		
			         }

			setInterval(function() { 
				makeTimer5();
			}, 1000);
});				

	// end of coming soon js 5






        // start of coming soon js 6
$( document ).ready(function() {	        
			function makeTimer6() {
						
						var launch_date = $("#sh_website_coming_soon_section_6 .sh_website_coming_soon_hidden_date_6").text();
						launch_date = String(launch_date);
						launch_date = launch_date.trim();								
						
						var endTime = new Date(launch_date);			
						endTime = (Date.parse(endTime) / 1000);

						var now = new Date();
						now = (Date.parse(now) / 1000);

						var timeLeft = endTime - now;

						var days = Math.floor(timeLeft / 86400); 
						var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
						var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
						var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
						days = Math.abs(days);
						
						if (hours < "10") { hours = "0" + hours; }
						if (minutes < "10") { minutes = "0" + minutes; }
						if (seconds < "10") { seconds = "0" + seconds; }

						
						
						$("#sh_website_coming_soon_section_6 .sh_days").html(
							    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
								);				
						$("#sh_website_coming_soon_section_6 .sh_hours").html(
							    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
								);	
						$("#sh_website_coming_soon_section_6 .sh_minutes").html(
							    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
								);				
						$("#sh_website_coming_soon_section_6 .sh_seconds").html(
							    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
								);		
				         }

				setInterval(function() { 
					makeTimer6();
				}, 1000);
				
});					

		  // end of coming soon js 6

				// start of coming soon js 7
$( document ).ready(function() {	        
			function makeTimer7() {
						
						var launch_date = $("#sh_website_coming_soon_section_7 .sh_website_coming_soon_hidden_date_7").text();
						launch_date = String(launch_date);
						launch_date = launch_date.trim();								
						
						var endTime = new Date(launch_date);			
						endTime = (Date.parse(endTime) / 1000);

						var now = new Date();
						now = (Date.parse(now) / 1000);

						var timeLeft = endTime - now;

						var days = Math.floor(timeLeft / 86400); 
						var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
						var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
						var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
						days = Math.abs(days);
						
						if (hours < "10") { hours = "0" + hours; }
						if (minutes < "10") { minutes = "0" + minutes; }
						if (seconds < "10") { seconds = "0" + seconds; }

						
						
						$("#sh_website_coming_soon_section_7 .sh_days").html(
							    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
								);				
						$("#sh_website_coming_soon_section_7 .sh_hours").html(
							    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
								);	
						$("#sh_website_coming_soon_section_7 .sh_minutes").html(
							    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
								);				
						$("#sh_website_coming_soon_section_7 .sh_seconds").html(
							    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
								);		
				         }

				setInterval(function() { 
					makeTimer7();
				}, 1000);
				
});					

		  // end of coming soon js 7


					
					


// start of coming soon js 8
$( document ).ready(function() {	        
			function makeTimer8() {
						
						var launch_date = $("#sh_website_coming_soon_section_8 .sh_website_coming_soon_hidden_date_8").text();
						launch_date = String(launch_date);
						launch_date = launch_date.trim();							
						
						var endTime = new Date(launch_date);			
						endTime = (Date.parse(endTime) / 1000);

						var now = new Date();
						now = (Date.parse(now) / 1000);

						var timeLeft = endTime - now;

						var days = Math.floor(timeLeft / 86400); 
						var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
						var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
						var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
						days = Math.abs(days);
						
						if (hours < "10") { hours = "0" + hours; }
						if (minutes < "10") { minutes = "0" + minutes; }
						if (seconds < "10") { seconds = "0" + seconds; }

						
						
						$("#sh_website_coming_soon_section_8 .sh_days").html(
	                  			'<div class="sh_number">' + days + '</div><div class="sh_label"></div>'							    				
								);				
						$("#sh_website_coming_soon_section_8 .sh_hours").html(
							    '<div class="sh_number">' + hours  +  '</div><div class="sh_label"></div>'					
								);	
						$("#sh_website_coming_soon_section_8 .sh_minutes").html(
							    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label"></div>'					
								);				
						$("#sh_website_coming_soon_section_8 .sh_seconds").html(
							    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label"></div>'					
								);		
				         }

				setInterval(function() { 
					makeTimer8();
				}, 1000);
				
});					

		  // end of coming soon js 8





 


// start of coming soon js 9
$( document ).ready(function() {	        
			function makeTimer9() {
						
						var launch_date = $("#sh_website_coming_soon_section_9 .sh_website_coming_soon_hidden_date_9").text();
						launch_date = String(launch_date);
						launch_date = launch_date.trim();							
						
						var endTime = new Date(launch_date);			
						endTime = (Date.parse(endTime) / 1000);

						var now = new Date();
						now = (Date.parse(now) / 1000);

						var timeLeft = endTime - now;

						var days = Math.floor(timeLeft / 86400); 
						var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
						var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
						var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
						days = Math.abs(days);
						
						if (hours < "10") { hours = "0" + hours; }
						if (minutes < "10") { minutes = "0" + minutes; }
						if (seconds < "10") { seconds = "0" + seconds; }

						
						
						$("#sh_website_coming_soon_section_9 .sh_days").html(
							    '<div class="sh_number">' + days  +  '</div><div class="sh_label">days</div>'					
								);				
						$("#sh_website_coming_soon_section_9 .sh_hours").html(
							    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">hours</div>'					
								);	
						$("#sh_website_coming_soon_section_9 .sh_minutes").html(
							    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">minutes</div>'					
								);				
						$("#sh_website_coming_soon_section_9 .sh_seconds").html(
							    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">seconds</div>'					
								);		
				         }

				setInterval(function() { 
					makeTimer9();
				}, 1000);
				
});					

		  // end of coming soon js 9


	
	// start of coming soon js 10
$( document ).ready(function() {	 
	function makeTimer10() {
				
				var launch_date = $("#sh_website_coming_soon_section_10 .sh_website_coming_soon_hidden_date_10").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();					
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_10 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_10 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_10 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_10 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer10();
		}, 1000);
});	
	// end of coming soon js 10	
	
	
		// start of coming soon js 12
$( document ).ready(function() {	
	function makeTimer12() {
				
				var launch_date = $("#sh_website_coming_soon_section_12 .sh_website_coming_soon_hidden_date_12").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();					
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_12 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_12 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_12 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_12 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer12();
		}, 1000);
});	
	// end of coming soon js 12
	
	
	
	
	
	// start of coming soon js 13
$( document ).ready(function() {	
	function makeTimer13() {
				
				var launch_date = $("#sh_website_coming_soon_section_13 .sh_website_coming_soon_hidden_date_13").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_13 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_13 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_13 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_13 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer13();
		}, 1000);
});	
	// end of coming soon js 13
	
	
	
	
	// start of coming soon js 14
$( document ).ready(function() {	
	function makeTimer14() {
				
				var launch_date = $("#sh_website_coming_soon_section_14 .sh_website_coming_soon_hidden_date_14").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_14 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_14 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_14 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_14 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer14();
		}, 1000);
});	
	// end of coming soon js 14
	
	
	
	
		// start of coming soon js 15
$( document ).ready(function() {	
	function makeTimer15() {
				
				var launch_date = $("#sh_website_coming_soon_section_15 .sh_website_coming_soon_hidden_date_15").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_15 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days/</div>'					
						);				
				$("#sh_website_coming_soon_section_15 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours/</div>'					
						);	
				$("#sh_website_coming_soon_section_15 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes/</div>'					
						);				
				$("#sh_website_coming_soon_section_15 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer15();
		}, 1000);
});	
	// end of coming soon js 15
	
	
	
	
	
			// start of coming soon js 16
$( document ).ready(function() {	
	function makeTimer16() {
				
				var launch_date = $("#sh_website_coming_soon_section_16 .sh_website_coming_soon_hidden_date_16").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_16 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_16 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_16 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_16 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer16();
		}, 1000);
});	
	// end of coming soon js 16
	
	
	
	
	
// start of coming soon js 17
$( document ).ready(function() {	
	function makeTimer17() {
				
				var launch_date = $("#sh_website_coming_soon_section_17 .sh_website_coming_soon_hidden_date_17").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_17 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_17 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_17 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_17 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer17();
		}, 1000);
});	
	// end of coming soon js 17
	
	
	
	// start of coming soon js 18
$( document ).ready(function() {	
	function makeTimer18() {
				
				var launch_date = $("#sh_website_coming_soon_section_18 .sh_website_coming_soon_hidden_date_18").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_18 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_18 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_18 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_18 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer18();
		}, 1000);
});	
	// end of coming soon js 18
	
	
	
	
	// start of coming soon js 19
$( document ).ready(function() {	
	function makeTimer19() {
				
				var launch_date = $("#sh_website_coming_soon_section_19 .sh_website_coming_soon_hidden_date_19").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();	
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }

				
				
				$("#sh_website_coming_soon_section_19 .days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">Days</div>'					
						);				
				$("#sh_website_coming_soon_section_19 .hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">Hours</div>'					
						);	
				$("#sh_website_coming_soon_section_19 .minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">Minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_19 .seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">Seconds</div>'					
						);		
		         }

		setInterval(function() { 
			makeTimer19();
		}, 1000);
});	
	// end of coming soon js 19
	
	
	
	
	

	// start of coming soon js 20
$( document ).ready(function() {	
	function makeTimer20() {
				
				var launch_date = $("#sh_website_coming_soon_section_20 .sh_website_coming_soon_hidden_date_20").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();					
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }


				
				$("#sh_website_coming_soon_section_20 .days").html(
					    '<span class="sh_number">' + days  +  '</span><span class="sh_label">days</span>'					
						);				
				$("#sh_website_coming_soon_section_20 .hours").html(
					    '<span class="sh_number">' + hours  +  '</span><span class="sh_label">H</span>'					
						);	
				$("#sh_website_coming_soon_section_20 .minutes").html(
					    '<span class="sh_number">' + minutes  +  '</span><span class="sh_label">M</span>'					
						);				
				$("#sh_website_coming_soon_section_20 .seconds").html(
					    '<span class="sh_number">' + seconds  +  '</span><span class="sh_label">S</span>'					
						);	
		         }

		setInterval(function() { 
			makeTimer20();
		}, 1000);
});	
	// end of coming soon js 20
	
	
	
	
	// start of coming soon js 28
$( document ).ready(function() {	
	function makeTimer28() {
				
				var launch_date = $("#sh_website_coming_soon_section_28 .sh_website_coming_soon_hidden_date_28").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();					
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }


				
				$("#sh_website_coming_soon_section_28 .days").html(
					    '<span class="sh_number">' + days  +  '</span><span class="sh_label">days</span>'					
						);				
				$("#sh_website_coming_soon_section_28 .hours").html(
					    '<span class="sh_number">' + hours  +  '</span><span class="sh_label">hours</span>'					
						);	
				$("#sh_website_coming_soon_section_28 .minutes").html(
					    '<span class="sh_number">' + minutes  +  '</span><span class="sh_label">minutes</span>'					
						);				
				$("#sh_website_coming_soon_section_28 .seconds").html(
					    '<span class="sh_number">' + seconds  +  '</span><span class="sh_label">seconds</span>'					
						);	
		         }

		setInterval(function() { 
			makeTimer28();
		}, 1000);
});	
	// end of coming soon js 28
	
	
	
	// start of coming soon js 29
$( document ).ready(function() {	
	function makeTimer29() {
				
				var launch_date = $("#sh_website_coming_soon_section_29 .sh_website_coming_soon_hidden_date_29").text();
				launch_date = String(launch_date);
				launch_date = launch_date.trim();					
				
				var endTime = new Date(launch_date);		
				endTime = (Date.parse(endTime) / 1000);

				var now = new Date();
				now = (Date.parse(now) / 1000);

				var timeLeft = endTime - now;

				var days = Math.floor(timeLeft / 86400); 
				var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
				var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
				var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
				days = Math.abs(days);
				
				if (hours < "10") { hours = "0" + hours; }
				if (minutes < "10") { minutes = "0" + minutes; }
				if (seconds < "10") { seconds = "0" + seconds; }


				
				$("#sh_website_coming_soon_section_29 .sh_days").html(
					    '<div class="sh_number">' + days  +  '</div><div class="sh_label">days</div>'					
						);				
				$("#sh_website_coming_soon_section_29 .sh_hours").html(
					    '<div class="sh_number">' + hours  +  '</div><div class="sh_label">hours</div>'					
						);	
				$("#sh_website_coming_soon_section_29 .sh_minutes").html(
					    '<div class="sh_number">' + minutes  +  '</div><div class="sh_label">minutes</div>'					
						);				
				$("#sh_website_coming_soon_section_29 .sh_seconds").html(
					    '<div class="sh_number">' + seconds  +  '</div><div class="sh_label">seconds</div>'					
						);	
		         }

		setInterval(function() { 
			makeTimer29();
		}, 1000);
});	
	// end of coming soon js 29









