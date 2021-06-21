


// snippet 1

$(document).ready(function() {
	$("#sh_megamenubar").on("click", function(e) {
		e.stopPropagation();
	});
});

//snippet 1

$(document).ready(function() {
  
  $("#sh_megamenubar .sub-heading").on("click", function() {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar ul")
        .slideUp(200);
      $("#sh_megamenubar .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar .sub-heading").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar ul").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar ul")
        .slideDown(200);
    }
  });

});


// snippet 1





// snippet 2

$(document).ready(function() {
  $("#sh_megamenubar_2").on("click", function(e) {
    e.stopPropagation();
  });
});

//snippet 2

$(document).ready(function() {
  
  $("#sh_megamenubar_2 .sub-heading").on("click", function() {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar_2 .sh_acoordion_part")
        .slideUp(200);
      $("#sh_megamenubar_2 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar_2 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar_2 .sub-heading").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar_2 .sh_acoordion_part").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar_2 .sh_acoordion_part")
        .slideDown(200);
    }
  });

});


// snippet 2


// snippet 3
/*
$(document).ready(function() {
  $("#sh_megamenubar_3").on("click", function(e) {
    e.stopPropagation();
  });
});

*/
$(document).ready(function() {
  
  $("#sh_megamenubar_3 .sh_main > a").on("click", function(e) {
    
      e.preventDefault();
      //$(this).closest('ul.dropdown-menu').addClass("show");

	  if ($(this).hasClass("active")) {
	      $(this).removeClass("active");
	      $(this)
	        .siblings("#sh_megamenubar_3 .sh_content")
	        .slideUp(200);
	      $("#sh_megamenubar_3 .sh_content .o_default_snippet_text i")
	        .removeClass("fa-minus")
	        .addClass("fa-plus");
	    } else {
	      $("#sh_megamenubar_3 .sh_content .o_default_snippet_text i")
	        .removeClass("fa-minus")
	        .addClass("fa-plus");
	      $(this)
	        .find("i")
	        .removeClass("fa-plus")
	        .addClass("fa-minus");
	      $("#sh_megamenubar_3 .sh_main > a").removeClass("active");
	      $(this).addClass("active");
	      $("#sh_megamenubar_3 .sh_content").slideUp(200);
	      $(this)
	        .siblings("#sh_megamenubar_3 .sh_content")
	        .slideDown(200);
	    }
      
      e.stopPropagation();
      
      /*
	  if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar_3 .sh_content")
        .slideUp(200);
      $("#sh_megamenubar_3 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar_3 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar_3 .sh_main > a").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar_3 .sh_content").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar_3 .sh_content")
        .slideDown(200);
    }
	 */ 
	  
  });

});



// snippet 3






// snippet 4

$(document).ready(function() {
  $("#sh_megamenubar_4").on("click", function(e) {
    e.stopPropagation();
  });
});

//snippet 4

$(document).ready(function() {
  
  $("#sh_megamenubar_4 .sub-heading").on("click", function() {
    

      
	  if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar_4 .sh_acoordion_part")
        .slideUp(200);
      $("#sh_megamenubar_4 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar_4 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar_4 .sub-heading").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar_4 .sh_acoordion_part").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar_4 .sh_acoordion_part")
        .slideDown(200);
    }
  });

});


// snippet 4



// snippet 5

$(document).ready(function() {
  $("#sh_megamenubar_5").on("click", function(e) {
    e.stopPropagation();
  });
});



$(document).ready(function() {
  
  $("#sh_megamenubar_5 > .container > ul > li > a").on("click", function() {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar_5 .row")
        .slideUp(200);
      $("#sh_megamenubar_5 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar_5 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar_5 > .container > ul > li > a").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar_5 .row").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar_5 .row")
        .slideDown(200);
    }
  });

});
// snippet 5





// snippet 6

$(document).ready(function() {
  $("#sh_megamenubar_6").on("click", function(e) {
    e.stopPropagation();
  });
});


$(document).ready(function() {
	
  $("#sh_megamenubar_6 .sh_content .o_default_snippet_text").on("click", function() {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar_6 .sh_content ul")
        .slideUp(200);
      $("#sh_megamenubar_6 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar_6 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar_6 .sh_content .o_default_snippet_text a").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar_6 .sh_content ul").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar_6 .sh_content ul")
        .slideDown(200);
    }
  });

});


// snippet 6


















/* snippet 7 */
$(document).ready(function() {
  $("#sh_megamenubar_7").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 7 */

/* snippet 8 */
$(document).ready(function() {
  $("#sh_megamenubar_8").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 8 */


/* snippet 9 */
$(document).ready(function() {
  $("#sh_megamenubar_9").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 9 */

/* snippet 10 */
$(document).ready(function() {
  $("#sh_megamenubar_10").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 10 */

/* snippet 11 */
$(document).ready(function() {
  $("#sh_megamenubar_11").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 11 */

/* snippet 12 */
$(document).ready(function() {
  $("#sh_megamenubar_12").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 12 */

/* snippet 13 */
$(document).ready(function() {
  $("#sh_megamenubar_13").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 13 */

/* snippet 14 */
$(document).ready(function() {
  $("#sh_megamenubar_14").on("click", function(e) {
    e.stopPropagation();
  });
});
/* snippet 14 */

/* snippet 15 */
$(document).ready(function() {
  $("#sh_megamenubar_15").on("click", function(e) {
    e.stopPropagation();
  });
});

$(document).ready(function() {
  
  $("#sh_megamenubar_15 .sh_content h4").on("click", function() {
    if ($(this).hasClass("active")) {
      $(this).removeClass("active");
      $(this)
        .siblings("#sh_megamenubar_15 ul")
        .slideUp(200);
      $("#sh_megamenubar_15 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
    } else {
      $("#sh_megamenubar_15 .sh_content .o_default_snippet_text i")
        .removeClass("fa-minus")
        .addClass("fa-plus");
      $(this)
        .find("i")
        .removeClass("fa-plus")
        .addClass("fa-minus");
      $("#sh_megamenubar_15 .sh_content h4").removeClass("active");
      $(this).addClass("active");
      $("#sh_megamenubar_15 ul").slideUp(200);
      $(this)
        .siblings("#sh_megamenubar_15 ul")
        .slideDown(200);
    }
  });

});
/* snippet 15 */