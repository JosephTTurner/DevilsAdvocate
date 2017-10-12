from flask import Flask, request, url_for, redirect # Allow client - server interactions
from flask_cors import CORS, cross_origin # Addition flask functionality
from bs4 import BeautifulSoup # Make sense of / parse html files
import json # string based data structures
import urllib.request # open remote links
import urllib.error # catch possible errors when we open remote links
import re # handle / compile regular expressions

# Flask set up
app = Flask(__name__)
CORS(app, support_credentials=True)

# Define route to local host
@app.route("/get_sub_links", methods=['GET', 'POST'])
@cross_origin(support_credentials=True)
def get_sub_links():
	# 

	json_list_of_links = request.get_json()

	# json_list_of_links = json.load(request.data)

	print ("bluh some debug message")
	
	print(json_list_of_links)

	return_links = {}

	for link in json_list_of_links:
		print(link)	
		try:
			response = urllib.request.urlopen(link, timeout = 5)
		except urllib.error.HTTPError as err:
			# if err.code >= 400
			print(err.code)
		html = response.read()
		soup = BeautifulSoup(html)
		sub_links = []
		for sub_link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
			print("-----" + sub_link.get('href'))
			sub_links.append(sub_link.get('href'))
		return_links[link] = sub_links

	print(return_links)

	return json.dumps(return_links)

if __name__ == "__main__":
    app.run()
