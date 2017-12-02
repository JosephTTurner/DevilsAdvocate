# from flask import Flask, request, url_for, redirect # Allow client - server interactions
# from flask_cors import CORS, cross_origin # Cross Orgin Resource Sharing 
# # from bs4 import BeautifulSoup # Make sense of / parse html files
# import json # string based data structures
# import urllib.request # open remote links
# import urllib.error # catch possible errors when we open remote links
import re # handle / compile regular expressions
import csv # work with csv files
import urllib.parse
# from pprint import pprint
import newspaper
from threading import Thread
import sys
import random
from nltk.corpus import stopwords

# # Flask set up
# app = Flask(__name__)

# # Allow CORS requests 
# CORS(app, support_credentials=True)

# # Define route to local host
# @app.route("/analyze_news_source", methods=['POST'])
# @cross_origin(support_credentials=True)
def collect_fake_news():

	build_threads = []
	download_threads =[]
	parse_threads = []

	num_papers = 0
	num_articles = 0
	num_parsed = 0

	known_sources = []
	newspapers = []
	articles_to_download = []
	articles_to_parse = []
	source_data = []
	source_list = []

	fake = re.compile('.*[fF][aA][kK][eE].*')
	bias = re.compile('.*[bB][iI][aA][sS].*')
	imposter = re.compile('.*[iI][mM][pP][oO][sS][tT][eE][rR].*')
	satire = re.compile('.*[sS][aA][tT][iI][eE][rR].*')
	unreliable = re.compile('.*[uU][nN][rR][eE][lL][iI][aA][bB][lL][eE].*')
	reliable = re.compile('.*[rR][eE][lL][iI][aA][bB][lL][eE].*')
	conspiracy = re.compile('.*[cC][oO][nN][sS][pP][iI][rR][aA][cC][yY].*')
	rumor = re.compile('.*[rR][uU][mM][eE][rR].*')
	parody = re.compile('.*[pP][aA][rR][oO][dD][yY].*')

	escape_chars = re.compile('/[\n\\\-\_\t\(\)\,]/')

	cachedStopWords = stopwords.words("english")

	# Load CSV
	with open('BadSources.csv', 'r') as csvfile:
		source_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')		
		for line in source_reader:
			if line[0].split(",")[0] != "site_name":
				source_list.append(line[0].split(","))
				known_sources.append(line[0].split(",")[0])

	# WITH THE AMOUNT OF ARTICLES WE ARE PULLING WE COULD JUST 
	# FOCUS ON SOURCES TAGGED AS "FAKE"

	out = open("Articles_Data.csv", "w+")
	out.write("source,url,title,text,fake,bias,imposter,satire,unreliable,reliable,conspiracy,parody,rumor\n")


	def build_papers(start, end, sources, articles_to_parse):
		for i in range(start, end):
		# try:
			paper = newspaper.build('http://'+sources[i], 
				memoize_articles=False,
				http_success_only=False,
				fetch_images=False,
				request_timeout=7)
		# except Exception as e:
		# 	pass
		# else:
			if paper.size() > 0:
				j = 0
				if paper.size() > 10:
					while j < 10:
						article = paper.articles[random.randrange(paper.size() - 1)]
						if article in articles_to_parse:
							continue
						else:
							articles_to_parse.append([article, i])
							j += 1
				else:
					for article in paper.articles:
						articles_to_parse.append([article, i])			

			print('built ' + sources[i])


	
	# def download_articles(i, articles_to_download, articles_to_parse):
	# 	# print('attempting to build ' + sources[i])
	# 	article = articles_to_download[i]
	# 	# article_data = []
	# 	try:
	# 		article.download()
	# 	except Exception as e:	
	# 		print('failed to download article' + article.url)
	# 	else:				
	# 		articles_to_parse.append(article)

					


	def parse_articles(start, end, articles_to_parse, source_data):
		for i in range(start, end):
			article = articles_to_parse[i][0]
			source_index = articles_to_parse[i][1]

			article.download()

			print(article.url)

			try:
				article.parse()
			except Exception as e:
				pass
			else:
			
				# parsed_uri = urllib.parse.urlparse(article.url)
				# domain = '{uri.netloc}'.format(uri=parsed_uri)

				row = source_list[source_index][0]
				row += "," + article.url

				title = article.title

				title = title.replace(",", " ")
				title = title.replace(',', ' ')
				title = title.replace("\"", "\'")
				title = title.replace("\"", "\'")
				title = title.replace("\n", " ")
				title = ' '.join([word for word in title.split() if word not in cachedStopWords])


				text = article.text
				text = text.replace(",", " ")
				text = text.replace(',', ' ')
				text = text.replace("\"", "\'")
				text = text.replace("\n", " ")
				text = ' '.join([word for word in text.split() if word not in cachedStopWords])


				row += ",\""+title+"\""
				row += ",\""+text+"\""

				isfake = False
				flagged_fake = False
				flagged_imposter = False
				flagged_satire = False
				flagged_unreliable = False
				flagged_reliable = False
				flagged_conspiracy = False
				flagged_bias = False
				flagged_parody = False
				flagged_rumor = False

				for data in source_list[source_index]:

					if fake.match(data):
						flagged_fake = True
					elif imposter.match(data):
						flagged_imposter = True
					elif satire.match(data):
						flagged_satire = True
					elif unreliable.match(data):
						flagged_unreliable = True
					elif reliable.match(data):
						flagged_reliable = True
					if conspiracy.match(data):
						flagged_conspiracy = True
					elif bias.match(data):
						flagged_bias = True
					elif parody.match(data):
						flagged_parody = True
					elif rumor.match(data):
						flagged_rumor = True


				if flagged_fake:
					row += ',1'
				else:
					row += ',0'
				if flagged_bias:
					row += ',1'
				else:
					row += ',0'
				if flagged_imposter:
					row += ',1'
				else:
					row += ',0'
				if flagged_satire:
					row += ',1'
				else:
					row += ',0'
				if flagged_unreliable:
					row += ',1'
				else:
					row += ',0'
				if flagged_reliable:
					row += ',1'
				else:
					row += ',0'
				if flagged_conspiracy:
					row += ',1'
				else:
					row += ',0'
				if flagged_parody:
					row += ',1'
				else:
					row += ',0'
				if flagged_rumor:
					row += ',1'
				else:
					row += ',0'

				row += "\n"
				
				out.write(row)

				print('successfully downloaded and parsed ' + article.url)




	# known_sources = known_sources[100:200]
	# nthreads = int(len(known_sources)/4);
	nthreads = 20 # int(len(known_sources) / 4);

	print('launching ' + str(nthreads) + ' building threads...')

	for i in range(nthreads - 1):
		start = i * int(len(known_sources) / nthreads)
		end = (i+1) * int(len(known_sources) / nthreads) - 1

		t = Thread(target=build_papers, args=(start, end, known_sources, articles_to_parse))

		# t = Thread(target=build_papers, args=(i, known_sources, articles_to_parse))

		build_threads.append(t)
		t.start()

	print('building...')

	for i in range(nthreads - 1):
		build_threads[i].join()

	print('done done_building')
	
	# nthreads = int(len(articles_to_parse) / 4);

	print('launching ' + str(nthreads) + ' parsing threads...')

	for i in range(nthreads - 1):

		start = i * int(len(articles_to_parse) / nthreads)
		end = (i+1) * int(len(articles_to_parse) / nthreads) - 1

		t = Thread(target=parse_articles, args=(start, end, articles_to_parse, source_data))
		# t = Thread(target=parse_articles, args=(i, articles_to_parse, source_data))

		parse_threads.append(t)
		t.start()

	print('parsing...')

	for i in range(nthreads - 1):
		parse_threads[i].join()

	print('done parsing')

	### output to data file ###

	print('output data Articles_Data.csv...')

	out.close()
	

if __name__ == "__main__":
#     app.run()
	analyze_news_source()


