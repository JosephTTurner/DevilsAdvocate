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
from newspaper import Article
import threading
from threading import Thread
from threading import Semaphore
from threading import Event
from threading import RLock
import sys
import random
from nltk.corpus import stopwords
import queue

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

	start_parsing = Semaphore()
	build_threads_done = Event()
	articles_lock = RLock()
	write_lock = RLock()

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
	junksci = re.compile('.*[jJ][uU][nN][kK][sS][cC][iI].*')
	clickbait = re.compile('.*[cC][lL][iI][cC][kK][bB][aA][iI][tT].*')
	hate = re.compile('.*[hH][aA][tT][eE].*')
	political = re.compile('.*[pP][oO][lL][iI][tT][iI][cC][aA][lL].*')

	escape_chars = re.compile('/[\n\\\-\_\t\(\)\,]/')

	cachedStopWords = stopwords.words("english")

	# Load CSV
	with open('BadSources_Clean.csv', 'r', encoding="ISO-8859-1") as csvfile:
		source_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')		
		for line in source_reader:
			if line[0].split(",")[0] != "site_name":
				source_list.append(line[0].split(","))
				known_sources.append(line[0].split(",")[0])

	# WITH THE AMOUNT OF ARTICLES WE ARE PULLING WE COULD JUST 
	# FOCUS ON SOURCES TAGGED AS "FAKE"

	out = open("Articles_Data_Clean_English_Full.csv", "w+", encoding="ISO-8859-1")
	out.write("source,url,title,text,fake,bias,imposter,satire,unreliable,reliable,conspiracy,parody,rumor,junksci,clickbait,hate,political\n")


	def build_papers(start, end, sources, articles_to_parse):
		print('launching build thread')

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
			appended = 0
			if paper.size() > 0:
				# num_papers += 1

				if paper.size() > 10:

					while appended < 10:
						article = paper.articles[random.randrange(paper.size() - 1)]
						a = Article(article.url, language = 'en')

						if a is None:
							continue

						if [a, i] in articles_to_parse:
							continue

						else:
							with articles_lock:
								articles_to_parse.append([a, i])
							appended += 1
				else:

					for article in paper.articles:
						a = Article(article.url, language = 'en')

						if a is None:
							continue
						
						with articles_lock:
							articles_to_parse.append([a, i])
						appended += 1

				for k in range(appended):
					start_parsing.release()	

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

					


	def parse_articles(articles_to_parse, source_data):
		print('launching parse thread')
		while True:

			start_parsing.acquire()

			if build_threads_done.is_set():
				break

			with articles_lock:
				article_entry = articles_to_parse.pop(0)

			if article_entry is None:
				continue

			article = article_entry[0]

			source_index = article_entry[1]

			article.download()

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
				title = title.replace("\n", " ")
				title = " ".join([re.sub(r'\W+', '', word) for word in title.split() if word not in cachedStopWords])
				


				text = article.text
				text = text.replace(",", " ")
				text = text.replace(',', ' ')
				text = text.replace("\"", "\'")
				text = text.replace("\n", " ")
				text = " ".join([re.sub(r'\W+', '', word) for word in text.split() if word not in cachedStopWords])


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
				flagged_junksci = False
				flagged_clickbait = False
				flagged_hate = False
				flagged_political = False

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
					elif junksci.match(data):
						flagged_junksci = True
					elif clickbait.match(data):
						flagged_clickbait = True
					elif hate.match(data):
						flagged_hate = True
					elif political.match(data):
						flagged_political = True


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
				if flagged_junksci:
					row += ',1'
				else:
					row += ',0'
				if flagged_clickbait:
					row += ',1'
				else:
					row += ',0'
				if flagged_hate:
					row += ',1'
				else:
					row += ',0'
				if flagged_political:
					row += ',1'
				else:
					row += ',0'

				row += "\n"

				with write_lock:
					out.write(row)

				print('successfully downloaded and parsed ' + article.url)




	# known_sources = known_sources[100:125]
	# nthreads = int(len(known_sources)/4);
	nthreads = 20 # int(len(known_sources) / 4);

	print('launching ' + str(nthreads) + ' building threads...')

	for i in range(nthreads):
		start = i * int(len(known_sources) / nthreads)
		end = (i+1) * int(len(known_sources) / nthreads)
		t = Thread(target=build_papers, args=(start, end, known_sources, articles_to_parse))
		build_threads.append(t)
		t.start()

		t = Thread(target=parse_articles, args=(articles_to_parse, source_data))
		parse_threads.append(t)
		t.start()

	print('building...')

	for i in range(nthreads):
		build_threads[i].join()
	
	build_threads_done.set()
	
	# nthreads = int(len(articles_to_parse) / 4);

	# print('launching ' + str(nthreads) + ' parsing threads...')

	# for i in range(nthreads - 1):

	# 	start = i * int(len(articles_to_parse) / nthreads)
	# 	end = (i+1) * int(len(articles_to_parse) / nthreads) - 1

	# 	t = Thread(target=parse_articles, args=(start, end, articles_to_parse, source_data))
	# 	# t = Thread(target=parse_articles, args=(i, articles_to_parse, source_data))

	# 	parse_threads.append(t)
	# 	t.start()

	# print('parsing...')

	for i in range(nthreads):
		start_parsing.release()

	for i in range(nthreads):
		parse_threads[i].join()

	print('done parsing')

	# print('parsed %d artciles from %d newspapers. %d articles were flagged as reliable', num_parsed, num_papers, num_reliable)

	### output to data file ###

	print('output data Articles_Data_Clean_English_Full.csv...')

	out.close()
	

if __name__ == "__main__":
#     app.run()
	collect_fake_news()


