/*
 *  jQuery FillBox v1.0.0
 *
 *  Copyright (c) 2014 Leandro Cunha aka. Frango
 *  http://www.owlgraphic.com/owlcarousel/
 *
 *  Licensed under MIT
 *
 */

(function ($, window, document) {
	$.fn.fillBox = function() {

		this.each(function(){
		    var el = $(this),
		    	src = el.attr('src'),
		    	parent = el.parent();

		    parent.css({
		    	'background-image'    : 'url(' + src + ')',
		    	'background-size'     : 'cover',
		    	'background-position' : 'center'
		    });

		    el.hide();
		});
	};
}(jQuery, window, document));
