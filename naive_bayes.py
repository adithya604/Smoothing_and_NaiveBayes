from plotly import __version__
from plotly.offline import  plot
from plotly.graph_objs import Figure, Layout, Data, Scatter, Bar
from math import log
from n_grams import *
from collections import defaultdict
import os, sys

if len(sys.argv) != 2:
	print "Usage: python naive_bayes.py <folder_of_corpus>"
	exit(0)

dirr = sys.argv[1]

oFolder = 'naive_bayes/'
if not os.path.exists(oFolder):
	os.makedirs(oFolder)

if dirr[len(dirr)-1] != '/':
	dirr += '/'

files = sorted(os.listdir(dirr))
print files

def naiveBayes_Estimate(sentence, uprobs, cprobs):
	probs = []
	sprob = 0
	for file in uprobs:
		p = 1.0
		for word in sentence:
			p = p * uprobs[file][word]
		sprob += p
		probs += [(file, p * cprobs[file])]
	return probs, sprob


def probSentences(sentence, uprobs):
	resultProbs = []
	for file in uprobs:
		p = 1.0
		for word in sentence:
			p = p * uprobs[file][word]
		resultProbs.append((file, p))
	return resultProbs

def unigramProbs(corpus):
	probs = {}
	for file in corpus:
		N = sum(corpus[file].values())
		V = len(corpus[file])

		probs[file] = {}
		for word in corpus[file]:
			probs[file][word] = (corpus[file][word]+1)/float(N+V)

	return probs

def classProbabilities(corpus):
	probs = {}
	for file, corp in corpus.items():
		probs[file] = sum([len(x) for x in corp])
	val = sum(list(probs.values()))

	new_probs = {}
	for k, v in probs.items():
		new_probs[k] = v/float(val)
	return new_probs



corpora = {}

for f in files:
	corpora[f] = getTokenCounts(dirr+f, 'unigram')

words = []

for file in corpora:
	for word in corpora[file]:
		words.append(word)

words = set(words)

for word in words:
	for file in corpora:
		if word not in corpora[file]:
			corpora[file][word] = 0

## Plotting unigram counts
all_values = [(word, [corpora[file][word] for file in corpora]) for word in words]
sorted_all_values = sorted(all_values, reverse=True, key = lambda x: sum(x[1]))

get_v_for_auth = lambda x : list(zip(*list(zip(*sorted_all_values))[1]))[files.index(x)]

plots = []
for file in corpora:
	plots.append( Bar({"x" : list(zip(*sorted_all_values))[0], "y": get_v_for_auth(file)}, name=file) )

plot(plots, filename=oFolder+"naive_bayes_all_three")


## Getting and plotting unigram probabilities
uprobs = unigramProbs(corpora)

uni_prob_table = [(word, [uprobs[file][word] for file in uprobs]) for word in words]
sorted_uni_prob_table = sorted(uni_prob_table, reverse=True, key = lambda x: sum(x[1]))

get_v_for_auth = lambda x : list(zip(*list(zip(*sorted_uni_prob_table))[1]))[files.index(x)]

plots = []
for file in corpora:
	plots.append( Bar({"x" : list(zip(*sorted_uni_prob_table))[0], "y": get_v_for_auth(file)}, name=file) )

plot(plots, filename=oFolder+"naive_bayes_prob_all_three")


cprobs = classProbabilities(corpora)
print cprobs
sorted_cprobs = sorted(cprobs.items(), key = lambda x : x[1], reverse = True)

print list(zip(*sorted_cprobs))[1]

plot( [ Bar({"x" : list(zip(*sorted_cprobs))[0], "y": list(zip(*sorted_cprobs))[1]}) ], filename=oFolder+"NV_class_prob" )


sentence = 'the following are the movies'.split(' ')
sprobs = probSentences(sentence, uprobs)
plot([ Scatter({"x" : list(zip(*sprobs))[0], "y": list(zip(*sprobs))[1]}) ], filename=oFolder+'sprobs')

plot([ Bar({"x" : sentence, "y": [uprobs[file][w] for w in sentence]}, name=file) for author in corpora ], filename =oFolder+'uprobs')

nbprobs, sprob = naiveBayes_Estimate(sentence, uprobs, cprobs)

# print nbprobs
# print sprobs

p1 = Bar({"x" : list(zip(*sprobs))[0], "y": list(zip(*sprobs))[1]}, name='sprobs')
p2 = Bar({"x" : list(zip(*nbprobs))[0], "y": [i for i in list(zip(*nbprobs))[1]]}, name='nbprobs')

plot([p1, p2], filename=oFolder+"s_nb_probs")