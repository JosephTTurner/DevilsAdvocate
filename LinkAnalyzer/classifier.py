import nltk.corpus
import csv
featuresets = []


with open('./Fake_News.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        featuresets.append(row['text'])
with open('./Real_Articles_Data_Clean_English_Test4.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        featuresets.append(row['text'])
#articleData = ([(articleText, 'fake') for articleText in .words('Fake.txt')] + [(articleText, 'real') for articleText in articleText.words('real.txt')])
import random
random.shuffle(featuresets)

#featuresets = [(articleText, validity) for (n, validity) in articleData]
train_set, test_set = featuresets[4430:], featuresets[:4430]
print ('Made Data Sets')
classifier = nltk.NaiveBayesClassifier.train(train_set)
print('Made classifier')
classifier.classify(article_features('exampleArticle.txt'))

print(nltk.classify.accuracy(classifier, test_set))
