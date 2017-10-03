document.addEventListener('DOMContentLoaded', function(){
	var changeButton = document.getElementById('changeText');
	changeButton.addEventListener('click', function(){
		chrome.tabs.getSelected(null, function(tab){
			doc = document;
			console.log("Found the Document");
			elements = doc.getElementsByTagName('p');
			for(x = 0; x < elements.length; x++){
				console.log(elements[x]);
			}
		})
	})
})
