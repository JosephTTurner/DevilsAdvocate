import csv, sys, argparse
from nltk.corpus import stopwords
from nltk import ngrams

articleData = []
dictionary = {}
csv.field_size_limit(5000000)
with open('Real_Articles_Data_Clean_English_Test4.csv' , encoding= 'ISO-8859-1') as csvfile:
    wordreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    entry = []
    for row in wordreader:
        entry = row[0].split(',')
        articleData.append(entry)

#print(articleData[3])

for entry in articleData:
    articleData = ngrams(entry[3].split(), 2)
    for word in articleData:
        #normalize all of the words by removing all non-alphanumeric characters
        #and making all of the words lowercase
        #word = re.sub(r'\W+', '', word)
        #word = word.lower()
        if (word not in stopwords.words('english')): #Don't include stopwords
            if word not in dictionary: #check to see if the word has been added to the dictionary
                dictionary[word] = 1
            else:
                dictionary[word] = dictionary[word] + 1

fun = open('testfile.txt', 'w')
sort = sorted(dictionary.items(), key = lambda x:x[1], reverse = True)
fun.write('{!s:20}{:3}\n'.format('Word', 'Frequency'))
for (word, frequency) in sort:
    fun.write('{!s:20}{:3}\n'.format(word, frequency))
fun.close()
