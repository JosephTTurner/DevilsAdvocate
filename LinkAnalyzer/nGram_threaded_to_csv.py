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

TYPES = ["Fake", "Real"]

TYPE = TYPES[0]

articleData = []
article_lock = RLock()
dictionary = {}
dictionary_lock = RLock()
get_grams_go = Semaphore()
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

phrase_matrix_csv = open(TYPE+'_News_Phrases.csv', "w+", encoding= 'ISO-8859-1')


#print(articleData[3])

def get_grams(articleData, dictionary, total_word_count):
    while(True):

        get_grams_go.acquire()

        with article_lock:      
            if len(articleData) > 0:   
                entry = articleData.pop()
            else:
                done_getting.set()
            
            get_grams_go.release()

        if (done_getting.is_set()):
            break;

        text = entry[3]

        # print (text)

        text = " ".join([re.sub(r'\W+', '', word) for word in text.split() if word not in cached_stopwords])
        
        # print (text)
        text = text.split()
        
        word_count = len(text)

        phrases = ngrams(text, N_GRAMS)

        for phrase in phrases:
            #normalize all of the words by removing all non-alphanumeric characters
            #and making all of the words lowercase
            #word = re.sub(r'\W+', '', word)
            #word = word.lower()
            # if (word not in stopwords.words('english')): #Don't include stopwords
            with dictionary_lock:
                if phrase not in dictionary: #check to see if the word has been added to the dictionary
                    dictionary[phrase] = [1, 1/word_count]
                else:
                    dictionary[phrase] = [dictionary[phrase][0] + 1, dictionary[phrase][1] + 1/word_count] 

# launch threads
for i in range(NUM_THREADS): 
    t = Thread(target=get_grams, args=(articleData, dictionary, total_word_count))
    threads.append(t)
    t.start()

for i in range(NUM_THREADS):
    threads[i].join()
    # threads[i] = Thread(target=write_grams, args=(articleData, dictionary))
    # threads[i].start()

align = '{!s:50}{:30}{:20}'
sys.stdout = open(TYPE+str(N_GRAMS)+'_Grams.csv', 'w+')
sort = sorted(dictionary.items(), key = lambda x:x[1][0], reverse = True)
print('phrase,freq,f_over_art_wc')
for (phrase, frequency) in sort:
    if frequency[0] >= 5:
        words = " ".join([word for word in phrase])
        print(words+","+str(frequency[0])+","+str(frequency[1]))