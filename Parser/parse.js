

;(function($) {

	// 'use strict';

	// // Include HTML
	// var container = document.querySelector('body');

	// $.get(chrome.extension.getURL('./content.html'), function(data) {
	// 	$($.parseHTML(data)).appendTo(container);
	// });

	//  var el = document.createElement( 'html' );
	//  el.innerHTML = "<html><head><title>titleTest</title></head><body><a href='test0'>test01</a><a href='test1'>test02</a><a href='test2'>test03</a></body></html>";

	// console.log(document.getElementsByTagName( 'href' )); 

	// // need to load initial html file
	// // the line below is just a concept
	// document = getHTMLFromURL('http://people.cs.vt.edu/tmitra/cs4984/spotlight/');

	// create a list of the href blocks in a document
	var arr = [], l = document.links;
	for(var i=0; i < l.length; i++) {
  		arr.push(l[i].href);
	}	
	
	// output the list of hrefs to the log
	for(var i = 0; i < arr.length; i++){
		console.log(arr[i]); 	
	}

	// JSON list?


	// var links = { arr[1], arr[2], arr[3] };

	var arrJSON = JSON.stringify(arr);


	// Talk to server

	$.ajax({
		type : "POST",
		url : "http://localhost:5000/hello",
		data : arrJSON,
		contentType : 'application/json;charset=UTF-8',
		crossDomain: true,
		success : function(result){
			console.log(result);
		}
	});

	
})(jQuery);