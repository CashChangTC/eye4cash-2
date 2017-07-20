# Project name: eye4cash
Object detect and classification US&amp;Taiwan Dollar

# DataSet and Code
1. Call the Microfost's Bing search api to download images and reviewed it by myself.
2. Images taken by myself.
3. Final Model save in "/raidHDD/experimentData/Dev/Knife/hackthon/model1"
4. DataSet save in "/raidHDD/experimentData/Dev/Knife/hackthon/upup7"
5. train script is "/raidHDD/experimentData/Dev/Knife/hackthon/KnifeHackthonCoin_train.py"

#Architecture
1. Client: WebUI (html, javascript, jQuery, PHP)
2. Server: Python Flask 0.12 Framework
3. Deep Learning: Google TensorFlow
 
# Test on Dev Envirment step
1. Check docker's name "TF_gpu1_knife" is start.
```shell
$ docker ps -a
```

2. Entry docker: 
```shell
$ docker exec -it TF_gpu1_knife bash
```

3. Launch service
```shell
$ cd /raidHDD/experimentData/Dev/Knife/hackthon/
$ python server.py
```
you will see message =>  * Running on http://0.0.0.0:9455/ (Press CTRL+C to quit)
please do not close terminal !

4. Use mobile's browser (or Chrome F12) to visit host: http://10.36.161.199/eye4cash/ and upload photo get the answer.


# Train Your Model Step
1. Entry docker

2. check training dataset is exists "/raidHDD/experimentData/Dev/Knife/hackthon/upup7"

3. launch train script
```shell
$ cd /raidHDD/experimentData/Dev/Knife/hackthon/
$ python KnifeHackthonCoin_train.py
```
you will see each loss and accuracy...

4.When step is equal 10000,It will save final model in "/raidHDD/experimentData/Dev/Knife/hackthon/modelX"

# Explanation of the approach
We only use 2 layer conv and 3 class dataset include of 1 cent: 1891 files, 10 cent: 1472 files, 25 cent: 1322 files.
Reshape to 208x208 size, training 10,000 step.
Although accuracy is 99% but is not really on the real case,I test 15 photos  accuracy is 80%....
I think it can add more dataset to increase real accuracy, prevent over fitting...
