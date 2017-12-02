import csv, sys, argparse
from nltk.corpus import stopwords
from nltk import ngrams
import threading
from threading import Thread
from threading import Semaphore
from threading import Event
from threading import RLock

NUM_THREADS = 20

N_GRAMS = 4

articleData = []
article_lock = RLock()
dictionary = {}
dictionary_lock = RLock()
get_grams_go = Semaphore()
done_getting = Event()
threads = []

csv.field_size_limit(5000000)
with open('Fake_News.csv' , encoding= 'ISO-8859-1') as csvfile:
    wordreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    entry = []
    for row in wordreader:
        if len(row) > 0:
            entry = row[0].split(',')
            if (len(entry) == 17): # ignore broken entries
                articleData.append(entry)

#print(articleData[3])

def get_grams(articleData, dictionary):
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

        text = ngrams(entry[3].split(), N_GRAMS)
        for phrase in text:
            #normalize all of the words by removing all non-alphanumeric characters
            #and making all of the words lowercase
            #word = re.sub(r'\W+', '', word)
            #word = word.lower()
            # if (word not in stopwords.words('english')): #Don't include stopwords
            with dictionary_lock:
                if phrase not in dictionary: #check to see if the word has been added to the dictionary
                    dictionary[phrase] = 1
                else:
                    dictionary[phrase] = dictionary[phrase] + 1

# launch threads
for i in range(NUM_THREADS):
    t = Thread(target=get_grams, args=(articleData, dictionary))
    threads.append(t)
    t.start()

for i in range(NUM_THREADS):
    threads[i].join()
    # threads[i] = Thread(target=write_grams, args=(articleData, dictionary))
    # threads[i].start()

fun = open('fake_4_grams.txt', 'w')
sort = sorted(dictionary.items(), key = lambda x:x[1], reverse = True)
fun.write('{!s:20}{:3}\n'.format('Word', 'Frequency'))
for (word, frequency) in sort:
    fun.write('{!s:20}{:3}\n'.format(word, frequency))
fun.close()
