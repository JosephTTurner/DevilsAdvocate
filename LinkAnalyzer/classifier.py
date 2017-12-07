import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
import csv
featuresets = []

#import the csv files from the datasets and mark them as true or false given the data.
#this will act as the trainset and test set
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
random.shuffle(featuresets) #mix the data

train_set, test_set = featuresets[1258252:], featuresets[:1258253] #The first half of the dataset will be used as the trainset and the other half will be used as the test set
print ('Made Data Sets')
classifier = SklearnClassifier(BernoulliNB()).train(train_set) #Create the classification using the train set
print('Made classifier')
testFile = {}

print(nltk.classify.accuracy(classifier, test_set)) #test the accuracy of the classifier on the test set
