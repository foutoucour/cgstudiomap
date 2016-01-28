(function($){

	function loadSVG(svgId, svgFile) {
		Snap.load(svgFile, function (f) {	
			var svg = Snap(svgId);
			svg.append(f);
		});
	}
	
	$(".fill-box").fillBox();
	
	$(document).ready(function() {

		/* ---------------------------------------------- /*
		 * SVG // snapsvg loader
		/* ---------------------------------------------- */
		// Nav
        loadSVG("#arrow-down", "/shared_web_theme/static/src/svg/__arrow-down.svg");
        loadSVG("#logo-nav", "/shared_web_theme/static/src/svg/__logo-nav.svg");
        
        // Stats
        $(".stats div").each(function( index ) {
            loadSVG(this, "/shared_web_theme/static/src/svg/__stats-bg.svg");
         });


		/* ---------------------------------------------- /*
		 * Smooth scroll / Scroll To Top
		/* ---------------------------------------------- */

		$('a[href*=#]').bind("click", function(e){
           
			var anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $(anchor.attr('href')).offset().top
			}, 1000);
			e.preventDefault();
		});

		$(window).scroll(function() {
			if ($(this).scrollTop() > 100) {
				$('.scroll-up').fadeIn();
			} else {
				$('.scroll-up').fadeOut();
			}
		});

	});

})(jQuery);
