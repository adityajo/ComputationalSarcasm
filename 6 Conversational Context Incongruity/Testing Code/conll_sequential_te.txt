#unigrams+whosaidtowhom+actions+speaker+sentiment + PREV SENTIMENT 9March 2016
#!/usr/bin/python

import sys

import re


f = open('/data/aa1/PhD_Sem8/AAAI17Demo/sentiwordlist','r')
sentiment_dict = {}

for line in f:
	words = line.split(' ')
	sentiment_dict[words[0]] = words[1]





qid = 0
dict = {}
word_count = {}
rev_dict = {}
index = 1

def getActions(input):
	output = ''
	words = input.split(' ')
	action = False
	for word in words:
		if '(' in word:
			action = True
		
		if action:
			output += 'k'+word+' '
		else:
			output += word+' '

		if ')' in word:
			action = False
	return output.strip()

f_vocab = open(sys.argv[2],'r')		
for line in f_vocab:
	word1 = line.split('\t')[0]
	word2 = line.split('\t')[1]
	dict[word1] = int(word2)
	index = int(word2)

pos_index = index
neg_index = index+1
prev_pos_index = index+2
prev_neg_index = index+3

prev_speaker = '$'
prev_pos_score = 0
prev_neg_score = 0

prev_speaker = '$'
f = open(sys.argv[1],'r')
f_o2 = open('/data/aa1/PhD_Sem8/AAAI17Demo/output_seq.o','w')

prev_pos_score = 0
prev_neg_score = 0
for line in f:
	s_line = ''
	contents = line.split('\t')
	if "Scene" in line:
		qid +=1
		prev_pos_score = 0
		prev_neg_score = 0
	pos_score = 0
	neg_score = 0
	
	if len(contents) ==1:
		#print(contents)
		word_ids = [1]
		dialogue = contents[0].lower()
		dialogue = dialogue + ' '+ getActions(dialogue).lower()
		if len(dialogue) == 0:
			continue
		words = re.findall(r"[\w']+|[.,!?;]",dialogue)
		
		first_word = words[0]
		speaker = first_word+'ss'
		words.append(speaker)
		
		whosaidtowhom = prev_speaker+first_word+'ss'
		words.append(whosaidtowhom)

		prev_speaker = first_word

		for word in words:
			if word in dict:
				if word.lower() in sentiment_dict:
					sentiment = sentiment_dict[word.lower()]
					
					if int(sentiment) == 1:
						#print(word+' found as positive')
						pos_score += 1
					else:
						#print(word+' found as negative')
						neg_score += 1
				index = dict[word]
				word_ids.append(index)
		
		label = '1'
		

		word_ids = list(set(word_ids))
		word_ids.sort()
		s_line = label+' ' + 'qid:'+str(qid)+' '
		#print(word_ids)
		for id in word_ids:
			s_line += str(id)+':1 '
		s_line += str(pos_index)+':'+str(pos_score)+' '+str(neg_index)+':'+str(neg_score)+' '
		s_line += str(prev_pos_index)+':'+str(prev_pos_score)+' '+str(prev_neg_index)+':'+str(prev_neg_score)+' '
		s_line += '# '+line
		s_line = s_line.strip()
		f_o2.write(s_line+'<br/>\n')
	prev_pos_score = pos_score
	prev_neg_score = neg_score
