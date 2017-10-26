

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
		Connect to a server that pulls the html from the links 
		and parses out the sublinks
	*/

	$.ajax({
		type : "POST",
		url : "http://localhost:5000/get_sub_links",
		data : arrJSON,
		contentType : 'application/json;charset=UTF-8',
		crossDomain: true,
		success : function(result){ // success code: 200
			// result = link data
			console.log(result);
			result = $.parseJSON(result);
			showSubLinksOnHover(result);
		}
	});	

	/*
		Break up the sublinks into a readable string 
		that comes up when you hover over a link

		result = link data
	*/
	function showSubLinksOnHover(result){
		for(dataLink in result){

			// make a readable string from the sublinks in the data
			var hoverString = "";
			for (var i = 0; i < result[dataLink].length; i++){
				hoverString += result[dataLink][i] + "\n";
			}

			// replace the title of the href with the original link
			// with the readable list of sublinks
			$('a[href="'+dataLink+'"]').attr('title', hoverString);
			// sublinks will now appear when you hover over a link.
		}
	}
	
})(jQuery);