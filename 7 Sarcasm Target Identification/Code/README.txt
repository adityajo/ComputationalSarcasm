Python script name			Description

baseline.py			implement the baseline decided for the dataset - all words except stop word and sentiment bearing words of the text

classification_acc.py		used to produce the results for statistical extractor, and can also be used for sequence labeling results, for a particular run/fold
				(out of the 4 folds used) and for a particular feature set (out of the 17 combinations used for ablation - explained in results->
				README2) for all 3 metrics.

convert_for_svm_labels.py	modifies the training and test files produced for sequence labeling to the format required for SVM classification (changing labels
				2 -> 1 and 1 -> -1; removing the qid field used for sequence labeling files). data prepared for svm perf tool.	

dep_parse.py			to test the stanford dependency parser - not used directly anywhere

final_results.py		to produce final results for a particular feature combination (1-17) for statistical or sequence labeling approach by taking average
				of the results for the 4 folds (this script is present in each run folder (for a specific fold 1-4) for each approach for each dataset)

generate.py			generates the training files (17) and corresponding test files (17), with flags in the code to set the feature combination and the
				particular fold. format suitable for SVM HMM tool. used for sequence labeling, for statistical, 
				convert_for_svm_labels runs 2 small changes in the format.

generate_sents.py		generates 2 files - one containing the test sentences(text) and the other containing corresponding actual targets of that text(test)
				(for a particular fold at a time)

integ_34.py			used to produce the results for hybrid approach (or as well as and), for a particular run/fold
				(out of the 4 folds used) and for a particular feature set (out of the 17 combinations used for ablation - explained in results->
				README2) for all 3 metrics. The section checking for outside case also records the performance for outside cases separately (this 
				'outside' cases performance is not stored, the counts are printed, and the further calculation done manually)

NE_extractor.py			takes in text, returns a list of named entities in the text. used for rule 2 of rule based exatractor.

outside_stats.py		to produce the counts for cases where the target is outside the text


produce_actual_targs.py		this produces and stores a list of actual targets - used for generating word clouds (and nothing else)

produce_classi_results.py	to generate the results of statistical extractor (import and use classification_acc.py) and hybrid (import and use integ_34.py)
				for all feature combinations (17), across all folds (4) [basically a nested loop]

rule_based_app.py		produces the list of candidate target for rule based extractor (one for each metric) (one for majority approach as well, cut out in
				final draft of paper)

rule_based_app_evaluation	produces results for rule based extractor (prints and does not save in file)

rule_weighting.py		for a specific metric (out of 3), and according to that metric, produces the results for a specific rule at a time (will give 3 lists
				of potential targets according to the 3 different metrics for each dataset)

rules_implement.py		takes a text, and produces 9 lists of candidate targets, one for each rule

stats.py			produces the stats for the dataset (like average length of text, vocabulary size, etc.) mentioned in final report in dataset section


Text File

Run_SVM.txt			contains the command line intructions for implementing SVM perf tool and SVM HMM tool for training classifier and producing predictions		

NOTE:
in almost all of the above scripts, careful modification of file and folder names needs to be done for switching between the two datasets (tweets and snippets)




	