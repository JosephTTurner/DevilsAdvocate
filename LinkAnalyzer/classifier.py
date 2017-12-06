
import nltk.corpus
from nltk.tokenize import word_tokenize
import csv
featuresets = []


with open('./Fake_News.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		articleWords = nltk.word_tokenize(row['text'])
		for word in articleWords:
			addSet = [{'word': word}, 'False']
			featuresets.append(addSet)
with open('./Real_News.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		articleWords = nltk.word_tokenize(row['text'])
		for word in articleWords:
			addSet = [{'word': word}, 'True']
			featuresets.append(addSet)
import random
random.shuffle(featuresets)
print (len(featuresets))
train_set, test_set = featuresets[1258252:], featuresets[:1258253]
print ('Made Data Sets')
classifier = nltk.NaiveBayesClassifier.train(train_set)
print('Made classifier')
testFile = {}
# with open('exampleArticle.txt') as file:
# 	for line in file:
# 		articleWords = nltk.word_tokenize(line)
# 		for word in articleWords:
# 			addSet = [{'word': word}, 'False']
# 			testFile.update(addSet)

# classifier.classify(testFile)

print(nltk.classify.accuracy(classifier, test_set))