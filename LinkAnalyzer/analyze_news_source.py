from flask import Flask, request, url_for, redirect # Allow client - server interactions
from flask_cors import CORS, cross_origin # Cross Orgin Resource Sharing 
from bs4 import BeautifulSoup # Make sense of / parse html files
import json # string based data structures
import urllib.request # open remote links
import urllib.error # catch possible errors when we open remote links
import re # handle / compile regular expressions
import csv # work with csv files
import urllib.parse
from pprint import pprint
import newspaper


# # Flask set up
# app = Flask(__name__)

# # Allow CORS requests 
# CORS(app, support_credentials=True)

# # Define route to local host
# @app.route("/analyze_news_source", methods=['POST'])
# @cross_origin(support_credentials=True)
def analyze_news_source():

	print("hello")

	sources = []

	# Load CSV
	with open('BadSources.csv', 'r') as csvfile:
		source_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
		source_list = []
		for line in source_reader:
			source_list.append(line)
			sources.append(line[0].split(",")[0])

	newspaper.build('http://'+sources[0])

	newspapers = []
	
	for i in range(0,20):
		newspaper.build('http://'+sources[i])

if __name__ == "__main__":
#     app.run()
	analyze_news_source()
