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
def collect_real_news():

	# wsj = newspaper.build('http://www.wsj.com', memoize_articles = False)
	# article = wsj.articles[1]
	# print(article.url)
	# article.download()
	# article.parse()
	# print(article.text)

	# return

	build_threads = []
	download_threads =[]
	parse_threads = []

	start_parsing = Semaphore()
	added_articles = Event()
	no_more_articles = Event()
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

	escape_chars = re.compile('/[\n\\\-\_\t\(\)\,]/')

	cachedStopWords = stopwords.words("english")

	# Load CSV
	with open("Good_Sources.csv", "r", encoding="utf-8") as csvfile:
		source_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')		
		for line in source_reader:
			known_sources.append(line[0])

	# WITH THE AMOUNT OF ARTICLES WE ARE PULLING WE COULD JUST 
	# FOCUS ON SOURCES TAGGED AS "FAKE"

	out = open("Real_Articles_Data_Clean_English_Test3.csv", "w+", encoding="ISO-8859-1", errors="surrogateescape")
	out.write("source,url,title,text,fake,bias,imposter,satire,unreliable,reliable,conspiracy,parody,rumor,junksci,clickbait,hate,political\n")


	def build_papers(start, end, sources, articles_to_parse):
		print('LAUNCHING: build thread')

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
				print('built ' + sources[i])

				if paper.size() > 50:

					while appended < 50:
						article = paper.articles[random.randrange(paper.size())]
						a = Article(article.url, language = 'en')

						if a is None:
							continue

						if [a, i] in articles_to_parse:
							continue

						else:
							with articles_lock:
								articles_to_parse.append([a, i])
								appended += 1

							if not added_articles.is_set():
								added_articles.set()
							start_parsing.release()

							
				else:

					for article in paper.articles:
						a = Article(article.url, language = 'en')

						if a is None:
							continue
						
						with articles_lock:
							articles_to_parse.append([a, i])
							appended += 1
							
						if not added_articles.is_set():
							added_articles.set()
						start_parsing.release()
						

				
				# for k in range(appended):
				# 	start_parsing.release()	

			
			print('ADDED: ' + str(appended) + ' articles from ' + sources[i])

			


	
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
		print('LAUNCHING: parse thread')
		while True:

			added_articles.wait()

			start_parsing.acquire()

			if no_more_articles.is_set():
				break

			article_entry = None

			with articles_lock:
				if len(articles_to_parse) > 0:
					article_entry = articles_to_parse.pop(0)
				else:
					no_more_articles.set()


			if article_entry is None:
				continue

			article = article_entry[0]

			source_index = article_entry[1]

			article.download()

			print('DOWNLOADED: ' + article.url)

			try:
				article.parse()
			except Exception as e:
				pass
			else:
				
				print('PARSED: ' + article.url)
				# parsed_uri = urllib.parse.urlparse(article.url)
				# domain = '{uri.netloc}'.format(uri=parsed_uri)

				row = known_sources[source_index]
				row += "," + article.url

				title = article.title
				title = " ".join([re.sub(r'\W+', " ", word) for word in title.split() if word not in cachedStopWords])

				text = article.text
				text = " ".join([re.sub(r'\W+', " ", word) for word in text.split() if word not in cachedStopWords])


				row += ","+title
				row += ","+text


			# if flagged_fake:
				# row += ',1'
			# else:
				row += ",0"
			# if flagged_bias:
			# 	row += ',1'
			# else:
				row += ",0"
			# if flagged_imposter:
			# 	row += ',1'
			# else:
				row += ",0"
			# if flagged_satire:
			# 	row += ',1'
			# else:
				row += ",0"
			# if flagged_unreliable:
			# 	row += ',1'
			# else:
				row += ",0"
			# if flagged_reliable:
				row += ",1"
			# else:
			# 	row += ",0"
			# if flagged_conspiracy:
			# 	row += ',1'
			# else:
				row += ",0"
			# if flagged_parody:
			# 	row += ',1'
			# else:
				row += ",0"
			# if flagged_rumor:
			# 	row += ',1'
			# else:
				row += ",0"
				row += ",0"
				row += ",0"
				row += ",0"
				row += ",0"

				row += "\n"

				with write_lock:
					try:
						out.write(row)
					except Exception as e:
						pass
					else:
						print('WROTE: ' + article.url)




	# known_sources = known_sources[100:125]
	# nthreads = int(len(known_sources)/4);
	nthreads = 4 # int(len(known_sources) / 4);

	print('launching ' + str(nthreads) + ' building threads...')

	for i in range(nthreads):
		start = i * int(len(known_sources) / nthreads)
		end = (i+1) * int(len(known_sources) / nthreads)
		t = Thread(target=build_papers, args=(start, end, known_sources, articles_to_parse))
		build_threads.append(t)
		t.start()

	for i in range(20):
		t = Thread(target=parse_articles, args=(articles_to_parse, source_data))
		parse_threads.append(t)
		t.start()

	print('building...')

	for i in range(nthreads):
		build_threads[i].join()
	
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

	for i in range(len(parse_threads)):
		parse_threads[i].join()

	print('done parsing')

	# print('parsed %d artciles from %d newspapers. %d articles were flagged as reliable', num_parsed, num_papers, num_reliable)

	### output to data file ###

	print('output data Real_Articles_Data_Clean_English_Test.csv...')

	out.close()
	

if __name__ == "__main__":
#     app.run()
	collect_real_news()


