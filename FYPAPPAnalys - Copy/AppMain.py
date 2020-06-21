from Main import *

from flask import Flask, request
from flask_cors import CORS

#DEBUG=os.environ["DEBUG_LINKEDIN_ENDPOINT"]=="True"
app = Flask(__name__)
CORS(app)
@app.route("/classifyDevice/<string:deviceName>/", methods=["GET"])
def websiteMain(deviceName):
	print(deviceName,classifyFinal(train ,hfClassifer, lfClassifier, deviceName, xhftest, xlftest, ytest, label))
	return classifyFinal(train ,hfClassifer, lfClassifier, deviceName, xhftest, xlftest, ytest, label)



app.run(host="localhost")

