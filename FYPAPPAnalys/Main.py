from imports import *
from random import seed
from random import randint

#Through Voting top max (top 5 LF, top 5 HF)
#larahost = "http://localhost:8000"


def updateTableDevice(device, detected_devices):
	table_name = 'devices'
	table_name_2 = 'devices_history'
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="alihassaan",
	  database="fypapp"
	)
	mycursor = mydb.cursor()
	query = " UPDATE "+table_name+" SET latest_change = %s WHERE name = %s "
	#increment old number
	data = (1, device)
	mycursor.execute(query, data)
	mydb.commit()
	#2nd query here
	timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
	data = (device, 1, str(detected_devices), timestamp, timestamp)
	query = "Insert into "+table_name_2+"(name, status, detected_devices, created_at, updated_at) values (%s, %s, %s, %s, %s)"
	mycursor.execute(query, data)
	mydb.commit()
	mycursor.close()
	mydb.close()

def classifyFinal(train, xhftrain, xlftrain ,clfhf, clflf, devicename, xhftest, xlftest, ytest, ytrain, label):
	#Get ID of Device
	idOfDevice = label[devicename]
	#Extract a test example of that id
	lfTestItem = None
	hfTestItem = None
	index = 0
	# seed random number generator
	seed(1)
	# generate some integers
	value = randint(0, 10)
	count = 0
	for i in range(0,len(ytest)):
		if ytest[i] == idOfDevice:
			lfTestItem = xlftest[i]
			hfTestItem = xhftest[i]
			index = i
			count += 1
			if count == value:
				break;

	detected_devices = []
	nsamples, nxhf, nyhf = xhftrain.shape
	distancesHf, indicesHf = clfhf.kneighbors(xhftest[i].reshape((1,nxhf*nyhf)), n_neighbors=1)
	#LF Top 5 Indices
	nsamples, nxlf, nylf = xlftrain.shape
	distancesHf, indicesLf = clflf.kneighbors(xlftest[i].reshape((1,nxlf*nylf)), n_neighbors=1)
	print([int(train[x][-1]) for x in indicesLf[0]])
	print([int(train[x][-1]) for x in indicesHf[0]])
	resultLf = [int(train[x][-1]) for x in indicesLf[0]]
	resultHf = [int(train[x][-1]) for x in indicesHf[0]]
	if (resultLf[0] == resultHf[0]):
		detected_devices = [label.inverse[resultHf[0]]]
		updateTableDevice(label.inverse[resultHf[0]], detected_devices)
	else:
		distancesHf, indicesHf = clfhf.kneighbors(xhftest[i].reshape((1,nxhf*nyhf)), n_neighbors=8)
		hfFinalIndices = [int(train[x][-1]) for x in indicesHf[0]]
		#LF Top 5 Indices
		distancesHf, indicesLf = clflf.kneighbors(xlftest[i].reshape((1,nxlf*nylf)), n_neighbors=7)
		lfFinalIndices = [int(train[x][-1]) for x in indicesLf[0]]
		finalIndices = hfFinalIndices + lfFinalIndices
		counter = dict(Counter(finalIndices))
		print(counter)

		maxIndice = max(counter.items(), key=operator.itemgetter(1))[0]
		counterSorted = sorted(counter.items(), key=lambda x: x[1], reverse=True)
	
	
		for item in counterSorted[0:3]:
			detected_devices.append(label.inverse[item[0]])
	#if counter[maxIndice] >= 8:
	#	detected_devices = label.inverse[maxIndice]
	#print("The Classified Device is: ", label.inverse[maxIndice])
		updateTableDevice(label.inverse[maxIndice], detected_devices)
	#Add the new example in clfhf, clflf
	#xhftrain, xlftrain ,clfhf, clflf, xhftest, xlftest, ytest, ytrain = getArrayTrainTest(xhftrain, xlftrain ,clfhf, clflf, xhftest, xlftest, ytest, ytrain, index)
	print("The Classified Device is/are: ", detected_devices)
	return str(detected_devices)
	

def readLabels(main_dir):
	label = {}
	for i in range(len(os.listdir(main_dir))):
	    if (os.listdir(main_dir)[i].split('.')[0] not in ['mains', 'subpanel', 'outdoor', 'electric', 'electronics']):
	        label[os.listdir(main_dir)[i].split('.')[0]] = int(i);
	label = bidict(label)
	return label


def getArray():
	array = []
	for file in os.listdir(main_dir):
		if (file.split('.')[0] not in ['mains', 'subpanel', 'outdoor', 'electric', 'electronics']):
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
def getnewArray(array):
	newarray = np.zeros((len(array)-1, len(array[0])))
	for x in range(len(array)-1):
	    #print(x)
	    for y in range(len(array[0])):
	        try:
	        	newarray[x][y] = float(array[x][y])
	        except IndexError as E:
	        	print(x,y)
	return newarray

#-----

#-----

#print(label)
#print(label.inverse)
def getArrayTrainTest(xhftrain, xlftrain ,clfhf, clflf, xhftest, xlftest, ytest, ytrain, index):
	print(xlftrain.shape)
	xhftrain = np.append(xhftrain,xhftest[index])
	print(xlftrain.shape)
	xlftrain = np.append(xlftrain,xlftest[index])
	#xhftest = np.delete(xhftrain,index)
	#xlftest = np.delete(xlftest,index)
	#ytrain = np.append(ytrain,ytest[index])
	ytest = np.delete(ytest,index)
	nsamples, nx, ny = xlftrain.shape
	xtrain_new = xlftrain.reshape((nsamples,nx*ny))
	clflf = KNeighborsClassifier(n_neighbors=1, p=1)
	clflf.fit(xtrain_new, ytrain.ravel())
	nsamples, nx, ny = xlftrain.shape
	xtrain_new = xlftrain.reshape((nsamples,nx*ny))
	clfhf = KNeighborsClassifier(n_neighbors=1, p=1)
	clfhf.fit(xtrain_new, ytrain.ravel())
	return xhftrain, xlftrain ,clfhf, clflf, xhftest, xlftest, ytest, ytrain


def splitTrainTest(newarray):
	newarray = np.array(newarray)
	newarray = newarray.reshape(len(newarray), len(newarray[0]),1)
	print(newarray.shape)
	noTrain=int(0.85*len(newarray));
	train,test,__ = np.vsplit(newarray[np.random.permutation(newarray.shape[0])],(noTrain,len(newarray)))
	print(len(train))
	upto=len(newarray[0])-1 #550 + 275 + 250 = 825
	xtrain,ytrain = train[:,0:upto,:],train[:,upto,:]
	xhftrain = xtrain[:,0:550,:]
	xlftrain = xtrain[:,550:800,:]
	xtest,ytest = test[:,0:upto,:],test[:,upto,:]
	xhftest = xtest[:,0:550,:]
	xlftest = xtest[:,550:800,:]
	#print(ytrain)
	#print(ytest)
	return train,test, xtrain, ytrain, xhftrain, xhftest, xlftrain, xlftest, ytrain, ytest

#-----
#-----

def highFreqTrain():
	#HF using top n_neighbors to see if the ground label is in n_neighbors or not.
	nsamples, nx, ny = xhftrain.shape
	xtrain_new = xhftrain.reshape((nsamples,nx*ny))
	clfhf = KNeighborsClassifier(n_neighbors=1, p=1)
	clfhf.fit(xtrain_new, ytrain.ravel())
	#print(ytrain.ravel())
	results = []
	for i in range(0,len(xhftest)):
	    distances, indices = clfhf.kneighbors(xhftest[i].reshape((1,nx*ny)), n_neighbors=1)
	    #for x in indices[0]:
	    #print(ytest[i], [int(train[x][-1]) for x in indices[0]])
	    if (ytest[i] in [int(train[x][-1]) for x in indices[0]]):
	        results.append(1)
	    else:
	    	pass
	        #print("original: ", label.inverse[int(ytest[i])], "predicted:", label.inverse[int(clf.predict(xhftest[i].reshape((1,nx*ny))))])
	#print(train[4168][-1]#print(ytest[0])
	#print(indices)
	#print("Results for All Categories, power:"+str(1)+" neighbors: "+str(1))
	print("HF Stats:")
	print(sum(results))
	print(len(ytest))
	print(sum(results)/len(ytest))
	return clfhf
#-------
#-----

def highFreqTrainCounter():
	#HF using top n_neighbors to see if the ground label is in n_neighbors or not.
	nsamples, nx, ny = xhftrain.shape
	xtrain_new = xhftrain.reshape((nsamples,nx*ny))
	clfhf = KNeighborsClassifier(n_neighbors=1, p=1)
	clfhf.fit(xtrain_new, ytrain.ravel())
	#print(ytrain.ravel())
	results = []
	for i in range(0,len(xhftest)):
		distances, indicesHf = clfhf.kneighbors(xhftest[i].reshape((1,nx*ny)), n_neighbors=8)
		hfFinalIndices = [int(train[x][-1]) for x in indicesHf[0]]
		#for x in indices[0]:
		#print(ytest[i], [int(train[x][-1]) for x in indices[0]])
		counter = dict(Counter(hfFinalIndices))
		#print(counter)
		maxIndice = max(counter.items(), key=operator.itemgetter(1))[0]
		if (maxIndice == ytest[i]):
			results.append(1)
##	    if (ytest[i] in [int(train[x][-1]) for x in indices[0]]):
##	        results.append(1)
##	    else:
##	    	pass
	        #print("original: ", label.inverse[int(ytest[i])], "predicted:", label.inverse[int(clf.predict(xhftest[i].reshape((1,nx*ny))))])
	#print(train[4168][-1]#print(ytest[0])
	#print(indices)
	#print("Results for All Categories, power:"+str(1)+" neighbors: "+str(1))
	print("HF Stats:")
	print(sum(results))
	print(len(ytest))
	print(sum(results)/len(ytest))
	return clfhf
#-------
def lowFreqTrainCounter():
	#HF using top n_neighbors to see if the ground label is in n_neighbors or not.
	nsamples, nx, ny = xlftrain.shape
	xtrain_new = xlftrain.reshape((nsamples,nx*ny))
	clfhf = KNeighborsClassifier(n_neighbors=1, p=1)
	clfhf.fit(xtrain_new, ytrain.ravel())
	#print(ytrain.ravel())
	results = []
	for i in range(0,len(xhftest)):
		distances, indicesLf = clfhf.kneighbors(xlftest[i].reshape((1,nx*ny)), n_neighbors=7)
		lfFinalIndices = [int(train[x][-1]) for x in indicesLf[0]]
		#for x in indices[0]:
		#print(ytest[i], [int(train[x][-1]) for x in indices[0]])
		counter = dict(Counter(lfFinalIndices))
		#print(counter)
		maxIndice = max(counter.items(), key=operator.itemgetter(1))[0]
		if (maxIndice == ytest[i]):
			results.append(1)
##	    if (ytest[i] in [int(train[x][-1]) for x in indices[0]]):
##	        results.append(1)
##	    else:
##	    	pass
	        #print("original: ", label.inverse[int(ytest[i])], "predicted:", label.inverse[int(clf.predict(xhftest[i].reshape((1,nx*ny))))])
	#print(train[4168][-1]#print(ytest[0])
	#print(indices)
	#print("Results for All Categories, power:"+str(1)+" neighbors: "+str(1))
	print("LF Counter Stats:")
	print(sum(results))
	print(len(ytest))
	print(sum(results)/len(ytest))
	return clfhf
#-------

#Separate Out the HF and LF Data and use both to classify, see the results;

def lowFreqTrain():
	#LF using top n_neighbors to see if the ground label is in n_neighbors or not.
	nsamples, nx, ny = xlftrain.shape
	xtrain_new = xlftrain.reshape((nsamples,nx*ny))
	clflf = KNeighborsClassifier(n_neighbors=1, p=1)
	clflf.fit(xtrain_new, ytrain.ravel())
	#print(ytrain.ravel())
	results = []
	for i in range(0,len(xlftest)):
	    distances, indices = clflf.kneighbors(xlftest[i].reshape((1,nx*ny)), n_neighbors=1)
	    #for x in indices[0]:
	    #print(ytest[i], [int(train[x][-1]) for x in indices[0]])
	    if (ytest[i] in [int(train[x][-1]) for x in indices[0]]):
	        results.append(1)
	    else:
	    	pass
	        #print("original: ", label.inverse[int(ytest[i])], "predicted:", label.inverse[int(clflf.predict(xlftest[i].reshape((1,nx*ny))))])
	#print(train[4168][-1]#print(ytest[0])
	#print(indices)
	#print("Results for All Categories, power:"+str(1)+" neighbors: "+str(1))
	print("LF Stats:")
	print(sum(results))
	print(len(ytest))
	print(sum(results)/len(ytest))
	return clflf
#-------------
def classifyFinalAccuracy(train ,clfhf, clflf, xhftest, xlftest, ytest, label):
	results = []
	for i in range(0,len(ytest)):
		lfTestItem = xlftest[i]
		hfTestItem = xhftest[i]

		nsamples, nxhf, nyhf = xhftrain.shape
		distancesHf, indicesHf = clfhf.kneighbors(hfTestItem.reshape((1,nxhf*nyhf)), n_neighbors=5)
		hfFinalIndices = [int(train[x][-1]) for x in indicesHf[0]]
		#LF Top 5 Indices
		nsamples, nxlf, nylf = xlftrain.shape
		distancesLf, indicesLf = clflf.kneighbors(lfTestItem.reshape((1,nxlf*nylf)), n_neighbors=5)
		lfFinalIndices = [int(train[x][-1]) for x in indicesLf[0]]
		finalIndices = hfFinalIndices + lfFinalIndices
		counter = dict(Counter(finalIndices))
		#print(counter)
		maxIndice = max(counter.items(), key=operator.itemgetter(1))[0]
		
		if (maxIndice == ytest[i]):
			results.append(1)
	print("Counter Stats: ")
	print(sum(results))
	print(len(ytest))
	print("Final Accuracy Counting: ", sum(results)/len(ytest))    

	
#------------

def addLabelstoDatabase(label):
	table_name = 'devices'
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="alihassaan",
	  database="fypapp"
	)

	mycursor = mydb.cursor()

	sql = "Insert into "+table_name+"(id, name, status, latest_change) values (%s, %s, %s, %s)"
	for key,value in label.items():
		val = (str(value), key, '0', '0')
		mycursor.execute(sql, val)
	mydb.commit()
	mycursor.close()
	mydb.close()
	print(mycursor.rowcount, "record inserted.")

main_dir = 'high_freq_difference_data'
label = readLabels(main_dir)
labelCount = readLabels(main_dir)

def classifyFinalAccuracyTopk(train ,clfhf, clflf, xhftest, xlftest, ytest, label, k):
	results = []
	for i in range(0,len(ytest)):
		lfTestItem = xlftest[i]
		hfTestItem = xhftest[i]

		nsamples, nxhf, nyhf = xhftrain.shape
		distancesHf, indicesHf = clfhf.kneighbors(hfTestItem.reshape((1,nxhf*nyhf)), n_neighbors=5)
		hfFinalIndices = [int(train[x][-1]) for x in indicesHf[0]]
		#LF Top 5 Indices
		nsamples, nxlf, nylf = xlftrain.shape
		distancesLf, indicesLf = clflf.kneighbors(lfTestItem.reshape((1,nxlf*nylf)), n_neighbors=5)
		lfFinalIndices = [int(train[x][-1]) for x in indicesLf[0]]
		finalIndices = hfFinalIndices + lfFinalIndices
		counter = dict(Counter(finalIndices))
		counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
		#print(counter)
		#print(counter)
		#maxIndice = max(counter.items(), key=operator.itemgetter(1))[0]
		count = 0
		for item in counter:
			if count < k:
				if item[0] == ytest[i]:
					results.append(1)
				count += 1
		#if (maxIndice == ytest[i]):
		#	results.append(1)
	print("Counter Stats: ")
	print(sum(results))
	print(len(ytest))
	print("Final Accuracy Counting: ", sum(results)/len(ytest))    

addLabelstoDatabase(label)
print(label)
array1 = getArray()
newarray = getnewArray(array1)
train, test, xtrain, ytrain, xhftrain, xhftest, xlftrain, xlftest, ytrain, ytest = splitTrainTest(newarray)
hfClassifer = highFreqTrain()
lfClassifier = lowFreqTrain()
#highFreqTrainCounter() #reduces Accuracy 88
#lowFreqTrainCounter() #reduces accuracy 80
print("With Top in N freq")
classifyFinalAccuracy(train,hfClassifer, lfClassifier, xhftest, xlftest, ytest, label)
print("With Top 2 in N freq")
classifyFinalAccuracyTopk(train,hfClassifer, lfClassifier, xhftest, xlftest, ytest, label,2)
print("With Top 3 in N freq")
classifyFinalAccuracyTopk(train,hfClassifer, lfClassifier, xhftest, xlftest, ytest, label,3)
print("With Top 4 in N freq")
classifyFinalAccuracyTopk(train,hfClassifer, lfClassifier, xhftest, xlftest, ytest, label,4)
print("With Top 5 in N freq")
classifyFinalAccuracyTopk(train,hfClassifer, lfClassifier, xhftest, xlftest, ytest, label,5)
#for key,value in label.items():
#	print(key,classifyFinal(train ,hfClassifer, lfClassifier, key, xhftest, xlftest, ytest, label))