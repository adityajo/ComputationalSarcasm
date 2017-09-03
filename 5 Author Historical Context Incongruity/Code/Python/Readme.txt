###WORKING AND RUNNING THE CODE

Contrast-based Predictor  (Flips folder)

WORKING-
We have the test tweets in the data folder. These tweets are input to the SentiPredict (Make sure to change the file paths in java code as instructed in its folder). Java program gives output to ‘ntweetsvalue’ and ‘ptweetsvalue’ in Codes/Python/flips/. These files are input to calculate.py which generates output in result and stats files.

Running steps-
	1) Run the java project SnentiPredict.
	2) Run Codes/Python/flips/calculate.py
	
——————————————————————————————————————————————————————————————————————————————————————————
Historical tweet-based Predictor (only_timeline folder)

WORKING-
We have the test tweets with author in the data folder. These tweets are input to searc.py(Make sure to change the file paths in code as instructed in its folder). This program gives in output in Codes/Python/only_timeline/timelines. Run pos_tag.py to get the tweets that have the NNPs from test tweet and saves those tweets to Codes/Python/only_timeline/_only_NNP.These files are input to calculate.py which generates output in result and stats files.

Running steps-
	1) Run search.py to get the timeline of users into timelines folders.
	2) Run pos_tagger.py to search tweets in timeline for NNPs
	3) Run the java project only timeline SentiPredict.
	4) Run Codes/Python/flips/calculate.py

——————————————————————————————————————————————————————————————————————————————————————————

Integrator (OR AND Relaxed-AND)

WORKING-
Takes results of the two predictors. Compares the output according to the ‘<x’ or ’<=x’ condition depending on ‘x’ and prints the output in result and stat files. The Paths for each of the files used must be changed for the computer in use.

Running steps-
	1) Set the paths to the ones needed(_SAIF will you word-emotion lexicon).
	2) Change the values in line 68 and 89 for OR, AND , Relaxed-AND configuration.
	3) Run the calculate_F_TL_NG.py.
	

	