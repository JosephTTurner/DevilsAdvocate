

;(function($) {

	// create a list of the href blocks in a document
	var arr = [], l = document.links;
	for(var i=0; i < l.length; i++) {
  		arr.push(l[i].href);
	}	
	
	// output the list of hrefs to the log
	for(var i = 0; i < arr.length; i++){
		console.log(arr[i]); 	
	}

	var arrJSON = JSON.stringify(arr);

	// Talk to server

	$.ajax({
		type : "POST",
		url : "http://localhost:5000/hello",
		data : arrJSON,
		contentType : 'application/json;charset=UTF-8',
		crossDomain: true,
		success : function(result){ 
			result = $.parseJSON(result);
			for(dataLink in result){

					var hoverString = "";
					for (var i = 0; i < result[dataLink].length; i++){
						hoverString += result[dataLink][i] + "\n";
					}

					$('a[href="'+dataLink+'"]').attr('title', hoverString);
					console.log("I did a thing.");
					console.log(dataLink);	
					console.log(result[dataLink]);
			}
		}
	});	
	
})(jQuery);