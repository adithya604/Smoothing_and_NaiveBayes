from n_grams import *
from zipfs_curve import *
import os, sys
import shutil

## File Names
oFolder = 'laplace/'


def laplaceSmoothing(countFreq, V):
	N = sum(countFreq.values())
	for key in countFreq:
		countFreq[key] = round(((countFreq[key]+1)/float(N+V))*N)
	return countFreq


def plot_Zipf_Laplace(n_grams, file_name):
	
	freqCounts_dict = getTokenCounts(file_name, n_grams)
	N = len(freqCounts_dict)

	folder, file_name = file_name.split('/')

	unsmoothed = sortTokenCounts(freqCounts_dict)
	smoothedFreq_200 = sortTokenCounts(laplaceSmoothing(freqCounts_dict, 200))
	smoothedFreq_2000 = sortTokenCounts(laplaceSmoothing(freqCounts_dict, 2000))
	smoothedFreq_N = sortTokenCounts(laplaceSmoothing(freqCounts_dict, N))
	smoothedFreq_10N = sortTokenCounts(laplaceSmoothing(freqCounts_dict, 10*N))

	p1 = Scatter(x = list(zip(*unsmoothed))[0], y= list(zip(*unsmoothed))[1], mode='lines', name="unsmoothed")
	p2 = Scatter(x = list(zip(*smoothedFreq_200))[0], y= list(zip(*smoothedFreq_200))[1], mode='lines', name="200")
	p3 = Scatter(x = list(zip(*smoothedFreq_2000))[0], y= list(zip(*smoothedFreq_2000))[1], mode='lines', name="2000")
	p4 = Scatter(x = list(zip(*smoothedFreq_N))[0], y= list(zip(*smoothedFreq_N))[1], mode='lines', name="Voc Size")
	p5 = Scatter(x = list(zip(*smoothedFreq_10N))[0], y= list(zip(*smoothedFreq_10N))[1], mode='lines', name="10*(Voc Size)")

	plot([p1,p2,p3,p4,p5], filename=oFolder +"_"+ n_grams +"_" + file_name)



if len(sys.argv) != 3:
	print "Usage : %s <type_of_gram> <file_name>" %argv[0]
	exit(1)

gram_type = sys.argv[1]
fileName = sys.argv[2]

if not os.path.exists(oFolder):
	os.makedirs(oFolder)

if not os.path.exists(fileName):
	print "'"+iFolder+file1+extension+"' file doesn't exist"
	exit(1)

plot_Zipf_Laplace(gram_type, fileName)