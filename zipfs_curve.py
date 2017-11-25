from plotly import __version__
from plotly.offline import  plot
from plotly.graph_objs import Figure, Layout, Data, Scatter
from math import log
from n_grams import *


## File Names
iFolder = 'corpora/'
file1 = 'anime'
file2 = 'movies'
file3 = 'news'
extension = '.txt'
oFolder = 'output/'

import os, sys
import shutil

if not os.path.exists(iFolder+file1+extension):
	print "'"+iFolder+file1+extension+"' file doesn't exist"
	exit(1)
if not os.path.exists(iFolder+file2+extension):
	print "'"+iFolder+file2+extension+"' file doesn't exist"
	exit(1)
if not os.path.exists(iFolder+file3+extension):
	print "'"+iFolder+file3+extension+"' file doesn't exist"
	exit(1)

if not os.path.exists(oFolder):
	os.makedirs(oFolder)

## Plots Zipf's Curve for sorted_word_frequencies
def plot_Zipf(sorted_word_freq, outFolder, n_gram, file_name):
	fileName = outFolder + "zipfs_" + n_gram + "_" + file_name + ".html"

	data = Data([ { "x" : list(zip(*sorted_word_freq)[0]), "y": list(zip(*sorted_word_freq)[1]) } ])
	layout = Layout(title = "zipf's curve for " + n_gram + " - " + file_name + ".txt", 
		xaxis = dict(title = n_gram), 
		yaxis = dict(title = 'frequency'))
	fig = Figure(data = data, 
		layout = layout)

	plot(fig, filename = fileName)

def plot_zipf_unsmoothed_all_ngrams():
	global iFolder, file1, file2, file3, extension, oFolder
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file1+extension, 'unigram')),  oFolder, "unigrams", file1)
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file2+extension, 'unigram')),  oFolder, "unigrams", file2)
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file3+extension, 'unigram')),  oFolder, "unigrams", file3)

	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file1+extension, 'bigram')),  oFolder, "bigrams", file1)
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file2+extension, 'bigram')),  oFolder, "bigrams", file2)
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file3+extension, 'bigram')),  oFolder, "bigrams", file3)

	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file1+extension, 'trigram')),  oFolder, "trigrams", file1)
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file2+extension, 'trigram')),  oFolder, "trigrams", file2)
	plot_Zipf( sortTokenCounts(getTokenCounts(iFolder+file3+extension, 'trigram')),  oFolder, "trigrams", file3)

def plot_log_log(sorted_word_freq, outFolder, n_gram, file_name):
	fileName = outFolder + "log_log_" + n_gram + "_" + file_name + ".html"

	ranks = [i+1 for i in range(len(sorted_word_freq))]
	log_freq = [log(x, 10) for x in list(zip(*sorted_word_freq)[1]) ]

	data = Data([ { "x" : ranks, "y": log_freq } ])
	layout = Layout(title = "log-log curve for " + n_gram + " - " + file_name + ".txt", 
		xaxis = dict(title = n_gram), 
		yaxis = dict(title = 'frequency'))
	fig = Figure(data = data, 
		layout = layout)

	plot(fig, filename = fileName)

def plot_all_log_log():
	global iFolder, file1, file2, file3, extension, oFolder

	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file1+extension, 'unigram')),  oFolder, "unigrams", file1 )
	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file2+extension, 'unigram')),  oFolder, "unigrams", file2 )
	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file3+extension, 'unigram')),  oFolder, "unigrams", file3 )

	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file1+extension, 'bigram')),  oFolder, "bigrams", file1 )
	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file2+extension, 'bigram')),  oFolder, "bigrams", file2 )
	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file3+extension, 'bigram')),  oFolder, "bigrams", file3 )

	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file1+extension, 'trigram')),  oFolder, "trigrams", file1 )
	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file2+extension, 'trigram')),  oFolder, "trigrams", file2 )
	plot_log_log( sortTokenCounts(getTokenCounts(iFolder+file3+extension, 'trigram')),  oFolder, "trigrams", file3 )


#plot_zipf_unsmoothed_all_ngrams()
#plot_all_log_log()