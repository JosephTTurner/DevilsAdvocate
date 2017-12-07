import csv, sys, argparse

articleData = []
dictionary = {}
csv.field_size_limit(5000000)
with open('Real_News.csv' , encoding= 'ISO-8859-1') as csvfile:
    wordreader = csv.reader(csvfile, delimiter='\n', quotechar='|')
    entry = []
    for row in wordreader: #split the csv file into articles
        entry = row[0].split(',')
        articleData.append(entry)

for entry in articleData:
    articleData = entry[3].split() #split the articles into words
    for word in articleData:
        #normalize all of the words by removing all non-alphanumeric characters
        #and making all of the words lowercase
        word = word.lower()
        if (word not in stopwords.words('english')): #Don't include stopwords
            if word not in dictionary: #check to see if the word has been added to the dictionary
                dictionary[word] = 1
            else:
                dictionary[word] = dictionary[word] + 1

#Format the data into readable comments with headers
sort = sorted(dictionary.items(), key = lambda x:x[1], reverse = True)
print ('{:20}{:3}'.format('Word', 'Frequency'))
for (word, frequency) in sort:
    print('{:20}{:3}'.format(word, frequency))
