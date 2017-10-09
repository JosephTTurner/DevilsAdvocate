

;(function($) {

	'use strict';

	// Include HTML
	var container = document.querySelector('body');

	$.get(chrome.extension.getURL('./content.html'), function(data) {
		$($.parseHTML(data)).appendTo(container);
	});

	var el = document.createElement( 'html' );
	el.innerHTML = "<html><head><title>titleTest</title></head><body><a href='test0'>test01</a><a href='test1'>test02</a><a href='test2'>test03</a></body></html>";

	el.getElementsByTagName( 'a' ); 	
	

})(jQuery);