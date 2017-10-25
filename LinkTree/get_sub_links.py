from flask import Flask, request, url_for, redirect # Allow client - server interactions
from flask_cors import CORS, cross_origin # Cross Orgin Resource Sharing 
from bs4 import BeautifulSoup # Make sense of / parse html files
import json # string based data structures
import urllib.request # open remote links
import urllib.error # catch possible errors when we open remote links
import re # handle / compile regular expressions
import csv # work with csv files
import urllib.parse


# Flask set up
app = Flask(__name__)

# Allow CORS requests 
CORS(app, support_credentials=True)

# Define route to local host
@app.route("/get_sub_links", methods=['POST'])
@cross_origin(support_credentials=True)
def get_sub_links():


	json_list_of_links = request.get_json()

	# json_list_of_links = json.load(request.data)
	
	# debugging purposes
	print(json_list_of_links)

	with open('OpenSources.csv', 'r') as csvfile:
		source_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		source_list = list(source_reader)

	print (source_list[1][0].split(","))

	# initialize JSON data
	return_links = {}

	for link in json_list_of_links:
		print(link)	
		parsed_uri = urllib.parse.urlparse(link)
		domain = '{uri.netloc}'.format(uri=parsed_uri)
		print(domain)
		print(link)	
		domain_info = []
		for badSource in source_list:
			bSourceInfo = badSource[0].split(",")
			re.compile(".*"+bSourceInfo[0])
			if domain == bSourceInfo[0]:
				domain_info = bSourceInfo
				break
		return_links[link] = domain_info


	# for link in json_list_of_links:
	# 	print(link)	
	# 	try:
	# 		response = urllib.request.urlopen(link, timeout = 5)
	# 	except urllib.error.HTTPError as err:
	# 		# if err.code >= 400
	# 		print(err.code)
	# 	html = response.read()
	# 	soup = BeautifulSoup(html)
	# 	sub_links = []
	# 	current_link = soup.findAll('a', attrs={'href': re.compile("^http://")})
	# 	for child_link in current_link:
	# 		print("-----" + child_link.get('href'))
	# 		sub_links.append(child_link.get('href'))
	# 	return_links[link] = sub_links

	# print(return_links)

	# start by setting the links on current page as keys
	# with appropriate bias, fake, conspiracy, etc. tags
	# as values. 
	#
	# pass thos values back to js to enable the hover-text 
	# to display those tags 


	return json.dumps(return_links)

if __name__ == "__main__":
    app.run()
