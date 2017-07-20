import requests
import json,shutil,random,time
import threading

def writeFile(imgUrl,filename):
    imgresponse = requests.get(imgUrl, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(imgresponse.raw, out_file)

def getPhoto(keyword,fileTag):
    baseurl="https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={0}"
    bing_url = baseurl.format(keyword)
    apikey="13ddd18a68da4fa3a7fe6802f4aa73b9"
    headers = {'Accept': 'application/json',"Content-Type":"multipart/form-data","Ocp-Apim-Subscription-Key":apikey}
    response = requests.get(bing_url, headers=headers)
    json_data = json.loads(response.text)
    if len(json_data["value"]) > 0:
        try:
            #seed = random.randint(0, len(json_data["value"])) -1
            idx = 0
            while True:
                imgUrl = json_data["value"][idx]["contentUrl"]
                #imgresponse = requests.get(imgUrl, stream=True)
                filename = "G:\\hackthon\\dataset\\{0}_{1}_{2}.{3}".format(fileTag,time.time(),idx,json_data["value"][idx]["encodingFormat"])
                thName = "{0}_{1}".format(fileTag,time.time())
                TH = threading.Thread(target=writeFile, name=thName,
                                      args=(imgUrl, filename,))
                TH.start()

                #with open(filename, 'wb') as out_file:
                #    shutil.copyfileobj(imgresponse.raw, out_file)
                idx+=1
                if idx >= len(json_data["value"]):
                    break

        except Exception as ex:
            print(ex)
            None
    else:
        return None

getPhoto("NTD 1","1c")
