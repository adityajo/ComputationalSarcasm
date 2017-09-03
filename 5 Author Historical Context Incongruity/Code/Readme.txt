Below is the list of “filename - details” - 


Java - Contains different java projects that give sentiment values for the input query. Further details are explained in the read me files in the folder

Python - Contains all the python codes that work together with the Java projects to detect sarcasm

Libraries - Contains all the libraries for twitter api and svm. There are docs for the explanation of how to use these libraries in their respective folders



###WORKING AND RUNNING THE CODE

Contrast-based Predictor 

WORKING-
We have the test tweets in the data folder. These tweets are input to the SentiPredict (Make sure to change the file paths in java code as instructed in its folder). Java program gives output to ‘ntweetsvalue’ and ‘ptweetsvalue’ in Codes/Python/flips/. These files are input to calculate.py which generates output in result and stats files.

Running steps-me
	1) Run the java project SnentiPredict.
	2) Run Codes/Python/flips/calculate.py
	

Historical tweet-based Predictor-

WORKING-
We have the test tweets with author in the data folder. These tweets are input to searc.py(Make sure to change the file paths in code as instructed in its folder). This program gives in output in Codes/Python/only_timeline/timelines. Run pos_tag.py to get the tweets that have the NNPs from test tweet and saves those tweets to Codes/Python/only_timeline/_only_NNP.These files are input to calculate.py which generates output in result and stats files.

Running steps-
	1) Run search.py.
	2) Run pos_tag.py to search tweets in timeline for NNPs
	3) Run the java project only timeline SentiPredict.
	4) Run Codes/Python/flips/calculate.py
	

