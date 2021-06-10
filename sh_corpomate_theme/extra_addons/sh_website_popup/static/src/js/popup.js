
$(document).ready(function(){
	var sh_cookie_key = window.location.hostname + '_sh_swp_model_popup_cookie';
	if ($.cookie(sh_cookie_key) != 'swp_shown'){
		$("#sh_swp_model_popup").modal('show');
		$.cookie(sh_cookie_key, "swp_shown", { expires: 1, path: '/' });
	}
});

		