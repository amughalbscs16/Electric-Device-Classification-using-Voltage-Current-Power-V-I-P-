import tensorflow as tf
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from bidict import bidict
from sklearn.neighbors import RadiusNeighborsClassifier
import time

main_dir = 'high_freq_difference_data'
label = readLabels()
array = getArray()
newarray = getnewArray()
train, test, xtrain, ytrain, xhftrain, xhftest, xlftrain, xlftest, ytrain, ytest = splitTrainTest(newarray)
highFreqTrain()
time.sleep(30)
lowFreqTrain()

def readLabels():
	label = {}
	for i in range(len(os.listdir(main_dir))):
	    if (os.listdir(main_dir)[i].split('.')[0] not in ['mains']):
	        label[os.listdir(main_dir)[i].split('.')[0]] = int(i);
	label = bidict(label)
	return label



print(label)
def getArray():
	array = []
	for file in os.listdir(main_dir):
		if (file.split('.')[0] not in ['mains']):
			fname = '{}/{}'.format(main_dir,file)
			openfile = open(fname, 'r')
			lines = openfile.readlines()
			#print(len(lines))
			#print(lines)
			#print(lines[-1])
			print(file)
			#print(lines[0])
			lines_new = []
			for i in range(0,len(lines)):
			    lines_new.append([])
			    for k in lines[i].split(','):
			        try:
			            lines_new[i].append(float(k))
			        except ValueError:
			            lines_new[i].append(0)
			            lines_new[i].append(0)

			lines = lines_new

			for i in range(0,len(lines)):
			    lines[i] = lines[i][0:800]#:800] #LF Data
			    lines[i].append(label[file.split('.')[0]]) #Label Append

			array = array + lines
			#print(len(lines))
			openfile.close()
	return array
#-----

#-----
def getnewArray():
	newarray = np.zeros((len(array)-1, len(array[0])))
	for x in range(len(array)-1):
	    print(x)
	    for y in range(len(array[0])):
	        if (y%100 == 0):
	            print(y) 
	        newarray[x][y] = float(array[x][y])
	return newarray

#-----

#-----

#print(label)
#print(label.inverse)

def splitTrainTest(newarray):
	newarray = np.array(newarray)
	newarray = newarray.reshape(len(newarray), len(newarray[0]),1)
	print(newarray.shape)
	noTrain=int(0.8*len(newarray));
	train,test,__ = np.vsplit(newarray[np.random.permutation(newarray.shape[0])],(noTrain,len(newarray)))
	print(len(train))
	upto=len(newarray[0])-1 #550 + 275 + 250 = 825
	xtrain,ytrain = train[:,0:upto,:],train[:,upto,:]
	xhftrain = xtrain[:,0:550,:]
	xlftrain = xtrain[:,550:800,:]
	xtest,ytest = test[:,0:upto,:],test[:,upto,:]
	xhftest = xtest[:,0:550,:]
	xlftest = xtest[:,550:800,:]
	print(ytrain)
	print(ytest)
	return train,test, xtrain, ytrain, xhftrain, xhftest, xlftrain, xlftest, ytrain, ytest

#-----
train, test, xtrain, ytrain, xhftrain, xhftest, xlftrain, xlftest, ytrain, ytest = splitTrainTest(newarray)
#-----

def highFreqTrain():
	#HF using top n_neighbors to see if the ground label is in n_neighbors or not.
	nsamples, nx, ny = xhftrain.shape
	xtrain_new = xhftrain.reshape((nsamples,nx*ny))
	clf = KNeighborsClassifier(n_neighbors=1, p=1)
	clf.fit(xtrain_new, ytrain.ravel())
	print(ytrain.ravel())
	results = []
	for i in range(0,len(xhftest)):
	    distances, indices = clf.kneighbors(xhftest[i].reshape((1,nx*ny)), n_neighbors=1)
	    #for x in indices[0]:
	    #print(ytest[i], [int(train[x][-1]) for x in indices[0]])
	    if (ytest[i] in [int(train[x][-1]) for x in indices[0]]):
	        results.append(1)
	    else:
	        print("original: ", label.inverse[int(ytest[i])], "predicted:", label.inverse[int(clf.predict(xhftest[i].reshape((1,nx*ny))))])
	#print(train[4168][-1]#print(ytest[0])
	#print(indices)
	print("Results for All Categories, power:"+str(1)+" neighbors: "+str(1))
	print(sum(results))
	print(len(ytest))
	print(sum(results)/len(ytest))
#-------

#-------

#Separate Out the HF and LF Data and use both to classify, see the results;

def lowFreqTrain():
	#LF using top n_neighbors to see if the ground label is in n_neighbors or not.
	nsamples, nx, ny = xlftrain.shape
	xtrain_new = xlftrain.reshape((nsamples,nx*ny))
	clflf = KNeighborsClassifier(n_neighbors=1, p=1)
	clflf.fit(xtrain_new, ytrain.ravel())
	print(ytrain.ravel())
	results = []
	for i in range(0,len(xlftest)):
	    distances, indices = clflf.kneighbors(xlftest[i].reshape((1,nx*ny)), n_neighbors=1)
	    #for x in indices[0]:
	    #print(ytest[i], [int(train[x][-1]) for x in indices[0]])
	    if (ytest[i] in [int(train[x][-1]) for x in indices[0]]):
	        results.append(1)
	    else:
	        print("original: ", label.inverse[int(ytest[i])], "predicted:", label.inverse[int(clflf.predict(xlftest[i].reshape((1,nx*ny))))])
	#print(train[4168][-1]#print(ytest[0])
	#print(indices)
	print("Results for All Categories, power:"+str(1)+" neighbors: "+str(1))
	print(sum(results))
	print(len(ytest))
	print(sum(results)/len(ytest))
#-------------

#------------