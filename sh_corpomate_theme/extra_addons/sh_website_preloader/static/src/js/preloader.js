$(document).ready(function () 
{ 
	  $('#preloader').css({'display':'block'});	  
	  $('body').css({'overflow':'auto'});
	  $('#preloader').delay(1500).fadeOut('slow');
	  $('body').delay(1500).css({'overflow':'auto'});
});
