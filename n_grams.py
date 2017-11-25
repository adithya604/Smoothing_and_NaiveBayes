## importing libraries
import re
import operator
from collections import Counter

## Tokenize and return unigrams
def tokenize_unigrams(data1):
	data1 = data1.lower()
	#data1 = re.sub('\( http[s]? : //(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])|( \? [a-zA-Z0-9]+ = [a-zA-Z0-9]+))+ \)', ' ', data1)
	#data1 = re.sub(' http[s]? : //(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])+|( \? ([a-zA-Z0-9]+) = ([a-zA-Z0-9]+)))+ ', '\1\3\4', data1)
	data1 = re.sub('http[s]? : //([a-zA-Z0-9\.]+)/(([a-zA-Z0-9\.]+))', '\1 \2', data1)
	data1 = re.sub('\[|\]|\(|\)|\*|\^|%|$|#|@|{|}|"|<|>|~|&gt|&amp', '', data1)
	#data1 = re.sub('\.|:|;|,|/|_|-|=|\?', ' ', data1)
	unigrams = re.findall('[a-zA-Z]+|[0-9]+|\.|:|;|,|&|!|\?|\'s',data1)
	#data1 = data1.strip().split()
	return unigrams

## Tokenize and return bigrams
def tokenize_bigrams(data):
	bigrams = []
	data = tokenize_unigrams(data)
	for ind, word in enumerate(data):
		if ind > 0:
			bigrams.append(data[ind-1] + " " + word)
	return bigrams

## Tokenize and return trigrams
def tokenize_trigrams(data):
	trigrams = []
	data = tokenize_unigrams(data)
	for ind, word in enumerate(data):
		if ind > 1:
			trigrams.append(data[ind-2] + " " + data[ind-1] + " " + word)
	return trigrams

## Get Sorted Tokens by frequency
def getTokenCounts(filename, ngram):
	with open(filename, 'r') as fptr:
		data = fptr.read()
		if ngram =="unigram":
			unigrams = tokenize_unigrams(data)
			unigram_counts = Counter(unigrams)
			return unigram_counts# sorted(unigram_counts.items(), key=operator.itemgetter(1), reverse=True)
		elif ngram == "bigram":
			bigrams = tokenize_bigrams(data)
			bigram_counts = Counter(bigrams)
			return bigram_counts #sorted(bigram_counts.items(), key=operator.itemgetter(1), reverse=True)
		elif ngram == "trigram":
			trigrams = tokenize_trigrams(data)
			trigram_counts = Counter(trigrams)
			return trigram_counts #sorted(trigram_counts.items(), key=operator.itemgetter(1), reverse=True)
        
def sortTokenCounts(countFreq):
	return sorted(countFreq.items(), key=operator.itemgetter(1), reverse=True)

#print tokenize_unigrams(open('corpora/anime.txt', 'r').read())