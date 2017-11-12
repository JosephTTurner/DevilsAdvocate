

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

	// convert to JSON array
	// readable data for python server
	var arrJSON = JSON.stringify(arr);

	/*
		Connect to a server that applies information to known
		sources that appear on the webpage.
	*/
	$.ajax({
		type : "POST",
		url : "http://localhost:5000/analyze_links",
		data : arrJSON,
		contentType : 'application/json;charset=UTF-8',
		crossDomain: true,
		success : function(result){ // success code: 200
			// result = link data
			console.log(result);
			result = $.parseJSON(result);
			showLinkInfoOnHover(result);
		}
	});	

	/*
	*	Break up the returned info into a readable substring.
	*
	*	@param result = link data
	*/
	function showLinkInfoOnHover(result){
		for(dataLink in result){
			// make a readable string from the sublinks in the data
			var hoverString = result[dataLink][0]+ "\n\n";
			for (var i = 1; i < result[dataLink].length; i++){
				for (var j = 0; j < result[dataLink][i].length; j++){
					hoverString += result[dataLink][i][j] + "\n";
				}
				hoverString += "\n";
			}
			// replace the title of the href with the info associated with the link
			$('a[href="'+dataLink+'"]').attr('title', hoverString);
			// info will now appear when you hover over a link.
		}
	}
	
})(jQuery);