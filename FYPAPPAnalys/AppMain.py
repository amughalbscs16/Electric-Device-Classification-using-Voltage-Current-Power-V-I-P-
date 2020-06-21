from Main import *

from flask import Flask, request
from flask_cors import CORS

#DEBUG=os.environ["DEBUG_LINKEDIN_ENDPOINT"]=="True"
app = Flask(__name__)
CORS(app)
@app.route("/classifyDevice/<string:deviceName>/", methods=["GET"])
def websiteMain(deviceName):
	print(deviceName,classifyFinal(train,xhftrain, xlftrain  ,hfClassifer, lfClassifier, deviceName, xhftest, xlftest, ytest, ytrain, label))
	return classifyFinal(train,xhftrain, xlftrain  ,hfClassifer, lfClassifier, deviceName, xhftest, xlftest, ytest, ytrain, label)

@app.route("/userSelection/<string:deviceName>/", methods=["GET"])
def userSelection(deviceName):
	print("User Selected, Added to the Trained List",deviceName)
	return deviceName+" added to Training "

app.run(host="localhost")

