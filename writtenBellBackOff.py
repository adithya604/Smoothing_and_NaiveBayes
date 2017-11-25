from plotly import __version__
from plotly.offline import  plot
from plotly.graph_objs import Figure, Layout, Data, Scatter, Bar
from math import log
from n_grams import *
from collections import defaultdict

## File Names
oFolder = 'wittenbell/'
extension = '.txt'
file1 = 'anime'
file2 = 'movies'
file3 = 'news'
import os, sys
import shutil


gram_type = sys.argv[1]
i_file_Name = sys.argv[2]

if not os.path.exists(i_file_Name):
	print "'"+i_file_Name+"' file doesn't exist"
	exit(1)

if not os.path.exists(oFolder):
	os.makedirs(oFolder)

def wittenBell_Unigrams(unigrams_dict):
	T = len(unigrams_dict.keys())
	N = sum(unigrams_dict.values())
	Z = N-T
	for word in unigrams_dict:
		count = unigrams_dict[word]
		new_prob = unigrams_dict[word]/float(N+T)
		unigrams_dict[word] = int(round(new_prob*N,0))
	count_unknown = (T*N)/float(Z*(N+T))
	#unigrams_dict['unknownwords'] = count_unknown
	return unigrams_dict

def wittenBell_Bigrams(bigrams_dict):
	count_dict = defaultdict(int)
	types_dict = defaultdict(int)

	for key in bigrams_dict:
		first = key.strip().split()[0]
		count_dict[first] += bigrams_dict[key]
		types_dict[first] += 1

	N = sum(bigrams_dict.values())
	for key in bigrams_dict:
		first = key.strip().split()[0]
		bigrams_dict[key] = round((bigrams_dict[key]/float(count_dict[first] + types_dict[first]))*count_dict[first], 0)
	return bigrams_dict

def wittenBell_Trigrams(bigrams_dict):
	count_dict = defaultdict(int)
	types_dict = defaultdict(int)

	for key in bigrams_dict:
		first = key.strip().split()  ## length of 3
		first = first[0]+ " " + first[1]  # we need only first two words for conditional prob
		count_dict[first] += bigrams_dict[key]
		types_dict[first] += 1

	for key in bigrams_dict:
		first = key.strip().split()
		first = first[0]+ " " + first[1]
		bigrams_dict[key] = round((bigrams_dict[key]/float(count_dict[first] + types_dict[first]))*count_dict[first], 0)
	return bigrams_dict

def wittenBell(fileName, gram_type):

	tokens_dict = getTokenCounts(fileName, gram_type)
	file = fileName.split('/')
	fileName = file[1]
	undiscounted = sortTokenCounts(tokens_dict)
	if gram_type == 'unigram':
		WB_discounted = sortTokenCounts(wittenBell_Unigrams(tokens_dict))
	if gram_type == 'bigram':
		WB_discounted = sortTokenCounts(wittenBell_Bigrams(tokens_dict))
	if gram_type == 'trigram':
		WB_discounted = sortTokenCounts(wittenBell_Trigrams(tokens_dict))
	
	p1 = Bar(x = list(zip(*undiscounted))[0], y= list(zip(*undiscounted))[1],  name="undiscounted")
	p2 = Bar(x = list(zip(*WB_discounted))[0], y= list(zip(*WB_discounted))[1],name="WB_discounted")

	plot([p1,p2], filename= oFolder + "wittenBell_" + gram_type +"_" + fileName)



print i_file_Name, gram_type

wittenBell(i_file_Name, gram_type)
