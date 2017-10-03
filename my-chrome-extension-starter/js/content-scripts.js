;(function($) {

	'use strict';

	// Include HTML
	var container = document.querySelector('body');

	$.get(chrome.extension.getURL('./content.html'), function(data) {
		$($.parseHTML(data)).appendTo(container);
	});

})(jQuery);