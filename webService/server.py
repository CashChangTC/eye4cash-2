from flask import Flask, request
import json,prod_test,base64,time
app = Flask(__name__)

#Global variable
logFolderName = "Log"
jsonHeader = "application/json"

@app.route("/")
def hello():
    return "eye4Cash Service"

@app.route('/v1/singlePhotoPrediction', methods=['POST'])
def singlePhotoPrediction():
    #try:
    requestObject = request.get_json()
        #try:
    photoString = requestObject["photoURL"].split(",")
    saveFilePath = "/raidHDD/experimentData/Dev/Knife/hackthon/test/{}.jpg".format(time.time())
    imgdata = base64.b64decode(photoString[1])
    with open(saveFilePath, 'wb') as f:
        f.write(imgdata)
    classPred = prod_test.evaluate_one_image(saveFilePath)
    response = app.response_class(
        response=json.dumps({"result": True, "class": classPred}),
        status=200,
        mimetype=jsonHeader
    )
    return response
if __name__ == "__main__":

    #execute http service at port 9455
    app.run(host='0.0.0.0', port=9455)