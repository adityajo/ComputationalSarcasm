Details of the Files 


calculate_F_TL_NG.py - calculates taking input from result_NewPhrases_28June.txt and gives output to result and stat file depending on the code inside.
Please change the values in lines 69 and 90 for AND , OR , and Relaxed AND.

Also change all files paths in the code.

result_NewPhrases_28June.txt - Number of flips using Word-Emotion lexicon for flips

------------------------------------------------------------------------------------

Integrator (OR AND Relaxed-AND)

WORKING-
Takes results of the two predictors. Compares the output according to the ‘<x’ or ’<=x’ condition depending on ‘x’ and prints the output in result and stat files. The Paths for each of the files used must be changed for the computer in use.

Running steps-
	1) Set the paths to the ones needed(_SAIF will you word-emotion lexicon).
	2) Change the values in line 68 and 89 for OR, AND , Relaxed-AND configuration.
	3) Run the calculate_F_TL_NG.py.
	