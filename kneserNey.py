from plotly import __version__
from plotly.offline import  plot
from plotly.graph_objs import Figure, Layout, Data, Scatter, Bar
from math import log
from n_grams import *
from laplace import *
from writtenBellBackOff import *
from collections import defaultdict

## File Names
oFolder = 'kneserNey/'
extension = '.txt'
file1 = 'anime'
file2 = 'movies'
file3 = 'news'
import os, sys
import shutil

unigram_dict = {}
bigram_dict = {}
trigram_dict = {}

if not os.path.exists(oFolder):
	os.makedirs(oFolder)

DELTA = 0.005
count_bigram_first = defaultdict(int)
count_bigram_second = defaultdict(int)
type_bigram_first = defaultdict(int)
type_bigram_second = defaultdict(int)
count_trigram_first = defaultdict(int)
count_trigram_second = defaultdict(int)
type_trigram_first = defaultdict(int)
type_trigram_second = defaultdict(int)


if len(sys.argv) != 3:
	print "Usage : python kneserNey.py <gram_type> <fileName>"
	exit(0)

gram_type = sys.argv[1]
fileName = sys.argv[2]


unigram_dict = getTokenCounts(fileName, 'unigram')
bigram_dict = getTokenCounts(fileName, gram_type)
trigram_dict = getTokenCounts(fileName, gram_type)


def kneserNey_BigramWord(ngram_word, smoothed_dict):

	global count_bigram_first, count_bigram_second, type_bigram_first, type_bigram_second

	global gram_type, unigram_dict, bigram_dict, trigram_dict

	if gram_type == 'bigram':
	
		w1, w2 = ngram_word.split()
		try:
			if smoothed_dict == None:
				prob = max(bigram_dict[ngram_word]-DELTA, 0)/float(unigram_dict[w1])
			else:
				prob = max(smoothed_dict[ngram_word]-DELTA, 0)/float(unigram_dict[w1])
		except: ## if ngram_word is not in keys of bigram_dict
			prob = 0

		prob += (DELTA/float(unigram_dict[w1])) * type_bigram_first[w1] * type_bigram_second[w2]

		return prob*unigram_dict[w1]
	
	elif gram_type == 'trigram':

		w1, w2, w3 = word.strip().split()
		w1 = w1 + " " + w2
		w2 = w3
		try:
			if smoothed_dict == None:
				prob = max(trigram_dict[ngram_word]-DELTA, 0)/float(bigram_dict[w1])
			else:
				prob = max(smoothed_dict[ngram_word]-DELTA, 0)/float(bigram_dict[w1])
		except: ## if ngram_word is not in keys of trigram_dict
			prob = 0
		print w1, w2, bigram_dict[w1] #type_trigram_first[w1]
		prob += (DELTA/float(bigram_dict[w1])) * type_trigram_first[w1] * type_trigram_second[w2]

		return prob*bigram_dict[w1] # new_count = prob * prev_count


def kneserNey(smoothed_dict):

	dict1 ={}
	if gram_type == 'bigram':
		for word in bigram_dict:
			dict1[word] = kneserNey_BigramWord(word, smoothed_dict)
	if gram_type == 'trigram':
		for word in trigram_dict:
			dict1[word] = kneserNey_BigramWord(word, smoothed_dict)

	return dict1

folder , fname = fileName.split('/')

if gram_type == 'bigram':

	for word in bigram_dict:
		w1, w2 = word.strip().split()
		count_bigram_first[w1] += bigram_dict[word]
		count_bigram_second[w2] += bigram_dict[word]
		type_bigram_first[w1] += 1
		type_bigram_second[w2] += 1
		
	kn_bigram_dict = sortTokenCounts( kneserNey(None))

	smoothedFreq_200 = sortTokenCounts( kneserNey( laplaceSmoothing(bigram_dict, 200)))
	smoothedFreq_2000 = sortTokenCounts( kneserNey( laplaceSmoothing(bigram_dict, 2000)))
	WB_discounted = sortTokenCounts( kneserNey( wittenBell_Bigrams(bigram_dict)))

	p1 = Bar(x = list(zip(*kn_bigram_dict))[0], y= list(zip(*kn_bigram_dict))[1], name="KN Only")
	p2 = Bar(x = list(zip(*smoothedFreq_200))[0], y= list(zip(*smoothedFreq_200))[1], name="KN + Laplace200")
	p3 = Bar(x = list(zip(*smoothedFreq_2000))[0], y= list(zip(*smoothedFreq_2000))[1], name="KN + Laplace2000")
	p4 = Bar(x = list(zip(*WB_discounted))[0], y= list(zip(*WB_discounted))[1], name="KN + Witten Bell")

	plot([p1, p2, p3, p4], filename= oFolder + "kn_" + gram_type +"_" + fname)

	laplace = sortTokenCounts(laplaceSmoothing(bigram_dict, 200))
	witten = sortTokenCounts(wittenBell_Bigrams(bigram_dict))

	p5 = Bar(x = list(zip(*laplace))[0], y= list(zip(*laplace))[1], name="Laplace - V")
	p6 = Bar(x = list(zip(*witten))[0], y= list(zip(*witten))[1], name="Witten-Bell")

	plot([p1, p5, p6], filename= oFolder + "kn_" + gram_type +"_comparision_" + fname)

elif gram_type == 'trigram':
	

	for word in trigram_dict:
		w1, w2, w3 = word.strip().split()
		w1 = w1 + " " + w2
		w2 = w3
		count_trigram_first[w1] += trigram_dict[word]
		count_trigram_second[w2] += trigram_dict[word]
		type_trigram_first[w1] += 1
		type_trigram_second[w2] += 1

	#print trigram_dict
	kn_trigram_dict = sortTokenCounts( kneserNey(None))
	#print kn_trigram_dict
	smoothedFreq_200 = sortTokenCounts( kneserNey( laplaceSmoothing(trigram_dict, 200)))
	smoothedFreq_2000 = sortTokenCounts( kneserNey( laplaceSmoothing(trigram_dict, 2000)))
	WB_discounted = sortTokenCounts( kneserNey( wittenBell_Bigrams(trigram_dict)))

	p1 = Bar(x = list(zip(*kn_trigram_dict))[0], y= list(zip(*kn_trigram_dict))[1], name="KN Only")
	p2 = Bar(x = list(zip(*smoothedFreq_200))[0], y= list(zip(*smoothedFreq_200))[1], name="KN + Laplace200")
	p3 = Bar(x = list(zip(*smoothedFreq_2000))[0], y= list(zip(*smoothedFreq_2000))[1], name="KN + Laplace2000")
	p4 = Bar(x = list(zip(*WB_discounted))[0], y= list(zip(*WB_discounted))[1], name="KN + Witten Bell")
	
	plot([p1, p2, p3, p4], filename= oFolder + "kn_" + gram_type+ "_" + fname)



'''
def getFollowerCount(w1, bigram_dict):
	cnt = 0
	for word in bigram_dict:
		first, _ = word.split()
		if first == w1:
			cnt += 1
	return cnt

def continuationProb(w2, bigram_dict):
	denom = len(bigram_dict)
	cnt = 0
	for word in bigram_dict:
		_, second = word.split()
		if second == w2:
			cnt += 1
	return cnt/float(denom) '''