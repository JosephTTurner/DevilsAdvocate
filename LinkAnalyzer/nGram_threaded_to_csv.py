import csv, sys, argparse
from nltk.corpus import stopwords
from nltk import ngrams
import threading
from threading import Thread
from threading import Semaphore
from threading import Event
from threading import RLock
import re

NUM_THREADS = 20

N_GRAMS = 3

TYPES = ["Real", "Fake"]

TYPE = TYPES[0]

articleData = []
article_lock = RLock()
dictionary = {}
dictionary_lock = RLock()
get_grams_go = Semaphore()
write_go = Semaphore()
done_writing = Event()
done_getting = Event()
threads = []
cached_stopwords = stopwords.words('english')
single_letter = re.compile('[a-z]{1}')

total_word_count = 0
twc_lock = RLock()

csv.field_size_limit(5000000)
with open(TYPE+'_News.csv' , encoding= 'ISO-8859-1') as csvfile:
	wordreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	entry = []
	for row in wordreader:
		if len(row) > 0:
			entry = row[0].split(',')
			if (len(entry) == 17): # ignore broken entries
				articleData.append(entry)

articleData2 = articleData

phrase_matrix_csv = open(TYPE+'_News_Phrases'+str(N_GRAMS)+'_Grams.csv', "w+", encoding= 'ISO-8859-1')
phrase_matrix_csv.write('article,fake,')
phrase_matrix_abstract = []
phrase_columns = []
article_entries = []


#print(articleData[3])

def get_grams(articleData, dictionary, total_word_count, phrase_columns, phrase_matrix_abstract):
	while(True):

		get_grams_go.acquire()

		with article_lock:      
			if len(articleData) > 0:   
				entry = articleData.pop()
			else:
				done_getting.set()
			
			get_grams_go.release()

		if (done_getting.is_set()):
			break

		entry[3] = " ".join([re.sub(r'\W+', '', word) for word in entry[3].split() if word not in cached_stopwords])

		# print (text)

		text = entry[3]
		
		# print (text)
		text = text.split()
		
		word_count = len(text)

		phrases = ngrams(text, N_GRAMS)
		
		with dictionary_lock:
			current_size = len(phrase_columns)+2    

		row = [0]*(current_size)

		#add the title to the data for context
		row[0] = (entry[2])

		#is the entry real or fake news?
		row[1] = (TYPES.index(TYPE))

		for phrase in phrases:
			
			in_list = True #for the sake of leaving the while loop out of the lock

			with dictionary_lock:
				if phrase not in phrase_columns: 
					phrase_columns.append(phrase)
					phrase_matrix_csv.write(str(phrase)+",")

		print(1)

def write_csv(articleData2, phrase_matrix_csv):
	while(True):

		write_go.acquire()

		if done_writing.is_set():
			break

		with write_lock:      
			if len(articleData2) > 0:   
				entry = articleData2.pop()
			else:
				done_writing.set()
			
			write_go.release()

		if done_writing.is_set():
			break

		text = entry[3]

		phrase_matrix_csv.write(entry[2]) # article title
		phrase_matrix_csv.write(str(TYPSE.index(TYPE))) # real/fake

		for phrase in phrase_columns:
			if phrase in text:
				phrase_matrix_csv.write('1,')
			else:
				phrase_matrix_csv.write('0,')

		phrase_matrix_csv.write('\n')


# launch threads
for i in range(NUM_THREADS): 
	t = Thread(target=get_grams, args=(articleData, dictionary, total_word_count, phrase_columns, phrase_matrix_abstract))
	threads.append(t)
	t.start()

print("Building dicitonary...")

for i in range(NUM_THREADS):
	threads[i].join()

for i in range(NUM_THREADS):
	threads[i] = Thread(target=write_grams, args=(articleData2, phrase_matrix_csv))
	threads[i].start()

print("Building matrix csv..")

phrase_matrix_csv.write('\n')

# for entry in articleData2:
#     text = entry[3]
#     text = " ".join([re.sub(r'\W+', '', word) for word in text.split() if word not in cached_stopwords])

#     phrase_matrix_csv.write(entry[2])
#     phrase_matrix_csv.write(TYPSE.index(TYPE))

#     for phrase in phrase_columns:
#         if phrase in text:
#             phrase_matrix_csv.write('1,')
#         else
#             phrase_matrix_csv.write('0,')

#     phrase_matrix_csv.write('\n')

phrase_matrix_csv.close()

print("Writing "+str(TYPE)+str(N_GRAMS)+"_Grams dictionary to csv...")

align = '{!s:50}{:30}{:20}'
sys.stdout = open(str(TYPE)+str(N_GRAMS)+'_Grams.csv', 'w+')
sort = sorted(dictionary.items(), key = lambda x:x[1][0], reverse = True)
print('phrase,freq,f_over_art_wc')
for (phrase, frequency) in sort:
	if frequency[0] >= 5:
		words = " ".join([word for word in phrase])
		print(words+","+str(frequency[0])+","+str(frequency[1]))