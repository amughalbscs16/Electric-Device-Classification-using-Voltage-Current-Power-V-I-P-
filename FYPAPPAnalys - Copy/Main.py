from imports import *

#Through Voting top max (top 5 LF, top 5 HF)
#larahost = "http://localhost:8000"


def updateTableDevice(device):
	table_name = 'devices'
	table_name_2 = 'devices_history'
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="",
	  database="fypapp"
	)
	mycursor = mydb.cursor()
	query = " UPDATE "+table_name+" SET latest_change = %s WHERE name = %s "
	data = (True, device)
	mycursor.execute(query, data)
	mydb.commit()
	#2nd query here
	timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
	data = (device, 1, timestamp, timestamp)
	query = "Insert into "+table_name_2+"(name, status, created_at, updated_at) values (%s, %s, %s, %s)"
	mycursor.execute(query, data)
	mydb.commit()
	mycursor.close()
	mydb.close()

def classifyFinal(train ,clfhf, clflf, devicename, xhftest, xlftest, ytest, label):
	#Get ID of Device
	idOfDevice = label[devicename]
	#Extract a test example of that id
	lfTestItem = None
	hfTestItem = None
	for i in range(0,len(ytest)):
		if ytest[i] == idOfDevice:
			lfTestItem = xlftest[i]
			hfTestItem = xhftest[i]
			break;

	#Now Classify
	nsamples, nxhf, nyhf = xhftrain.shape
	distancesHf, indicesHf = clfhf.kneighbors(xhftest[i].reshape((1,nxhf*nyhf)), n_neighbors=8)
	hfFinalIndices = [int(train[x][-1]) for x in indicesHf[0]]
	#LF Top 5 Indices
	nsamples, nxlf, nylf = xlftrain.shape
	distancesHf, indicesLf = clflf.kneighbors(xlftest[i].reshape((1,nxlf*nylf)), n_neighbors=7)
	lfFinalIndices = [int(train[x][-1]) for x in indicesLf[0]]
	finalIndices = hfFinalIndices + lfFinalIndices
	counter = dict(Counter(finalIndices))
	print(counter)
	maxIndice = max(counter.items(), key=operator.itemgetter(1))[0]    
	print("The Classified Device is: ", label.inverse[maxIndice])
	updateTableDevice(label.inverse[maxIndice])
	return label.inverse[maxIndice]
	

def readLabels(main_dir):
	label = {}
	for i in range(len(os.listdir(main_dir))):
	    if (os.listdir(main_dir)[i].split('.')[0] not in ['mains', 'subpanel', 'outdoor', 'electric']):
	        label[os.listdir(main_dir)[i].split('.')[0]] = int(i);
	label = bidict(label)
	return label


def getArray():
	array = []
	for file in os.listdir(main_dir):
		if (file.split('.')[0] not in ['mains', 'subpanel', 'outdoor', 'electric']):
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
	  passwd="",
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

#addLabelstoDatabase(label)
print(label)
array1 = getArray()
newarray = getnewArray(array1)
train, test, xtrain, ytrain, xhftrain, xhftest, xlftrain, xlftest, ytrain, ytest = splitTrainTest(newarray)
hfClassifer = highFreqTrain()
lfClassifier = lowFreqTrain()
classifyFinalAccuracy(train ,hfClassifer, lfClassifier, xhftest, xlftest, ytest, label)
#for key,value in label.items():
#	print(key,classifyFinal(train ,hfClassifer, lfClassifier, key, xhftest, xlftest, ytest, label))