			// pull all elments with paragraph tag "p"
			elements = document.getElementsByTagName('p');

			// for all those paragraph elements overwrite the color
			for(x = 0; x < elements.length; x++){
				elements[x].style.setProperty('color', 'red', 'important');
			}
