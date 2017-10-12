from flask import Flask, request, url_for, redirect
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import json
import urllib.request 
import urllib.error
import re

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/hello", methods=['GET', 'POST'])
@cross_origin(support_credentials=True)
def hello():

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
