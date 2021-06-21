odoo.define('sh_pwa_frontend.pwa', function(require) 
{
	var ajax = require('web.ajax');
	$( document ).ready(function(require) {
   		if ('serviceWorker' in navigator) {
			
			navigator.serviceWorker.register("/sw.js").then(function(){
				   });
		}
	});

});