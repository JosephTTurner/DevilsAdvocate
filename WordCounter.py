import newspaper
import re
from nltk.corpus import stopwords
cnn_paper = newspaper.build('http://cnn.com', memoize_articles=False)
first_article = cnn_paper.articles[5]
first_article.download()
first_article.parse()
dictionary = {}
text = first_article.text.split() #split the text into words
for word in text:
    #normalize all of the words by removing all non-alphanumeric characters
    #and making all of the words lowercase
    word = re.sub(r'\W+', '', word)
    word = word.lower()
    if (word not in stopwords.words('english')): #Don't include stopwords
        if word not in dictionary: #check to see if the word has been added to the dictionary
            dictionary[word] = 1
        else:
            dictionary[word] = dictionary[word] + 1
sort = sorted(dictionary.items(), key = lambda x:x[1], reverse = True)
print ('{:20}{:3}'.format('Word', 'Frequency'))
for (word, frequency) in sort:
    print ('{:20}{:3}'.format(word, frequency))
