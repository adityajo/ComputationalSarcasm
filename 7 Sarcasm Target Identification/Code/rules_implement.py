import NE_extractor as named_entity
import nltk
import sentiment_mod as s
from textblob import TextBlob
from nltk.parse.stanford import StanfordDependencyParser
dep_parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

p=open('positive_sent_words.txt','r')		#positive sentiment words lexicon
n=open('negative_sent_words.txt','r')		#negatve sentiment words lexicon
p=list(p)
n=list(n)
p=[x[:-1] for x in p]
n=[q[:-1] for q in n]

#produce pos tags of sentence for use in various rule implementations
def tag(sent):
    words=nltk.word_tokenize(sent)
    tagged=nltk.pos_tag(words)
    return tagged

#implement the nine rule in nine separate functions (R1-R9)

# pronoun and pronoun based adjectives
def R1(sent):
    t=tag(sent)
    w=nltk.word_tokenize(sent)
    l=[]
    just_tags=[]
    for i in range(len(t)):
        just_tags.append(t[i][1])
		#get all words which are pronouns
        if t[i][1]=='PRP':
            l.append(t[i][0])
            if 'WRB' in just_tags or 'WP' in just_tags or 'WDT' in just_tags:
                l.append(t[i][0])
            if '.' in just_tags and '?' in w[i:]:
                l.append(t[i][0])
			# below adds the pronoun again to list if it is being praised
            if i+1 < len(t):
                if t[i+1][1]=='JJ' and TextBlob(t[i][0]+' '+t[i+1][0]).sentiment.polarity>=0:
                    l.append(t[i][0])
            if i+2 < len(t):
                if t[i+2][1]=='JJ' and TextBlob(t[i][0]+' '+t[i+1][0]+' '+t[i+2][0]).sentiment.polarity>=0:
                    l.append(t[i][0])
            if i+3 < len(t):
                if t[i+3][1]=='JJ' and TextBlob(t[i][0]+' '+t[i+1][0]+' '+t[i+2][0]+' '+t[i+3][0]).sentiment.polarity>=0:
                    l.append(t[i][0])
            if i+4 < len(t):
                if t[i+4][1]=='JJ' and TextBlob(t[i][0]+' '+t[i+1][0]+' '+t[i+2][0]+' '+t[i+3][0]+' '+t[i+4][0]).sentiment.polarity>=0:
                    l.append(t[i][0])

            if i>0:
                if TextBlob(t[i-1][0]+' '+t[i][0]).sentiment.polarity>0:
                    l.append(t[i][0])
            if i>1:
                if TextBlob(t[i-2][0]+' '+t[i-1][0]+' '+t[i][0]).sentiment.polarity>0:
                    l.append(t[i][0])
					
		#possesive pronouns along with their object
        if t[i][1]=='PRP$':
            if i+1==len(t):
                l.append(t[i][0])
            if i+1 < len(t):
                if t[i+1][1]=='NN' or t[i+1][1]=='NNP' or t[i+1][1]=='NNS' or t[i+1][1]=='NNPS':
                    l.append(t[i][0])
                    l.append(t[i+1][0])
                    l.append(t[i][0]+' '+t[i+1][0])
            if i+2 < len(t):
                if t[i+2][1]=='NN' or t[i+2][1]=='NNP' or t[i+2][1]=='NNS' or t[i+2][1]=='NNPS':
                    l.append(t[i][0])
                    l.append(t[i+2][0])
                    l.append(t[i][0]+' '+t[i+1][0]+' '+t[i+2][0])
            if i+3 < len(t):
                if t[i+3][1]=='NN' or t[i+3][1]=='NNP' or t[i+3][1]=='NNS' or t[i+3][1]=='NNPS':
                    l.append(t[i][0])
                    l.append(t[i+3][0])
                    l.append(t[i][0]+' '+t[i+1][0]+' '+t[i+2][0]+' '+t[i+3][0])

            if i>0:
                if TextBlob(t[i-1][0]+' '+t[i][0]).sentiment.polarity>0:
                    l.append(t[i][0])
            if i>1:
                if TextBlob(t[i-2][0]+' '+t[i-1][0]+' '+t[i][0]).sentiment.polarity>0:
                    l.append(t[i][0])




    return l

#named entities
def R2(sent):
    l=named_entity.ne(sent)
    l=list(set(l))
    if 'Wow' in l:
        l.remove('Wow')
    if 'wow' in l:
        l.remove('wow')
    return l

#object of sentiment verbs
def R3(sent):
    l=[]
    t=tag(sent)
    w=nltk.word_tokenize(sent)
    jt=[x[1] for x in t]
    for i in range(len(t)-1):
        if t[i][1]=='VB' or t[i][1]=='VBD' or t[i][1]=='VBG' or t[i][1]=='VBZ' or t[i][1]=='VBN' or t[i][1]=='VBP':
            #print(0)
            if t[i][0] in p:
                #print(1)
                if ',' in jt[i+1:] and (jt[i+1:].index(',')+i+1)!=i+1:
                    k=jt[i+1:].index(',')+i+1
                    o=' '.join(w[i+1:k])
                    l.append(o)
                elif ':' in jt[i+1:] and (jt[i+1:].index(':')+i+1)!=i+1:
                    k=jt[i+1:].index(':')+i+1
                    o=' '.join(w[i+1:k])
                    l.append(o)
                elif '.' in jt[i+1:] and (jt[i+1:].index('.')+i+1)!=i+1:
                    #print(2)
                    k=jt[i+1:].index('.')+i+1
                    #print(k)
                    #print(w[(i+1):k])
                    o=' '.join(w[i+1:k])
                    #print(o)
                    l.append(o)

                try:
                    x=jt[i+1:].index('NN')+i+1
                    o=' '.join(w[i+1:x+1])
                    l.append(o)
                    l.append(w[x])
                except:
                    try:
                        x=jt[i+1:].index('NNS')+i+1
                        o=' '.join(w[i+1:x+1])
                        l.append(o)
                        l.append(w[x])
                    except:
                        try:
                            x=jt[i+1:].index('NNP')+i+1
                            o=' '.join(w[i+1:x+1])
                            l.append(o)
                            l.append(w[x])
                        except:
                            try:
                                x=jt[i+1:].index('NNPS')+i+1
                                o=' '.join(w[i+1:x+1])
                                l.append(o)
                                l.append(w[x])
                            except:
                                pass
            if t[i][0] in n:
                if TextBlob(' '.join(w[i+1:])).sentiment.polarity >=0:
                    l.append('OUTSIDE/LISTENER')
    return l

#gerunds and infinitives
def R5(sent):
    l=[]
    flag=0
    t=tag(sent)
    w=nltk.word_tokenize(sent)
    jt=[x[1] for x in t]
    fct=[y[0] for y in jt]
    for i in range(len(jt)-1):
        if jt[i]=='VBG' and jt[i+1]!='TO' and w[i+1]!='as':
            for k in range(i+1,len(jt)):
                if (fct[k]=='V' and jt[k]!='VBN') or fct[k]=='W' or jt[k]==',' or jt[k]=='.' or jt[k]==':' or jt[k]=='CC':
                    l.append(' '.join(w[i:k]))
                    flag=1
                    break
            if(flag==0):
                l.append(' '.join(w[i:]))
    flag=0
    for e in range(len(t)-1):
        if jt[e]=='TO' and fct[e+1]=='V':
            if e<len(t)-2:
                for k in range(e+2,len(t)):
                    if (fct[k]=='V' and jt[k]!='VBN') or fct[k]=='W' or jt[k]==',' or jt[k]=='.' or jt[k]==':' or jt[k]=='CC':
                        l.append(' '.join(w[e:k]))
                        flag=1
                        break
                if(flag==0):
                    l.append(' '.join(w[e:]))
            else:
                l.append(w[e]+' '+w[e+1])
            if e>0:
                if w[e-1]=='not' or w[e-1]=='Not':
                    s=w[e-1]+' '+l[-1]
                    l[-1]=s



    return l

#nouns subject to positive adjective
def R6(sent):
    l=[]
    nn=[]
    t=tag(sent)

    w=nltk.word_tokenize(sent)
    for q in range(len(t)):
        if t[q][1]=='NN' or t[q][1]=='NNS' or t[q][1]=='NNP' or t[q][1]=='NNPS':
            nn.append(q)

    if len(nn)==1:
        l.append(w[nn[0]])
        return l
    if len(nn)>1:
        for x in nn:
            if x>1:
                if TextBlob(' '.join(w[x-2:x])).sentiment.polarity > 0:
                    l.append(w[x])
                elif w[x-1] in p:
                    l.append(w[x])
            elif x==1:
                if w[0] in p:
                    l.append(w[x])
    return l

#subject of interrogative sentence	
def R7(sent):
    l=[]
    t=tag(sent)
    w=nltk.word_tokenize(sent)
    jt=[x[1] for x in t]

    for i in range(len(jt)):
        if jt[i]=='WDT' or jt[i]=='WP'or jt[i]=='WRB' or w[i]=='Could' or w[i]=='Would':
            if i+1<len(jt):
                try:
                    x=jt[i+1:].index('NN')+i+1
                    l.append(w[x])
                    l.extend(R1(' '.join(w[i+1:])))
                except:
                    try:
                        x=jt[i+1:].index('NNS')+i+1
                        l.append(w[x])
                        l.extend(R1(' '.join(w[i+1:])))
                    except:
                        if i>1:
                            l.extend(R6(' '.join(w[:(i-1)])))
                if 'this' in w[i+1:]:
                    l.append('this')
                if 'that' in w[i+1:]:
                    l.append('that')
    return l


#demonstrative adjective + following noun
def R9(sent):
    l=[]
    t=tag(sent)
    jt=[x[1] for x in t]
    w=nltk.word_tokenize(sent)
    for i in range(len(w)):
        if w[i]=='this' or w[i]=='that' or w[i]=='these' or w[i]=='those' or w[i]=='This' or w[i]=='That' or w[i]=='These' or w[i]=='Those':
            if i==len(w)-1:
                l.append(w[i])
            else:
                try:
                    x=jt[i+1:].index('NN')+i+1
                    if x==i+1:
                        l.append(w[i]+' '+w[x])
                        l.append(w[x])
                    elif x==i+2:
                        if jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS':
                            l.append(w[i]+' '+w[i+1]+' '+w[i+2])
                            l.append(w[i+2])
                    elif x==i+3:
                        if (jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS') and (jt[i+2]=='JJ' or jt[i+2]=='JJR' or jt[i+2]=='JJS' or jt[i+2]=='RB' or jt[i+2]=='RBR' or jt[i+2]=='RBS'):
                            l.append(w[i]+' '+w[i+1]+' '+w[i+2]+' '+w[i+3])
                            l.append(w[i+3])
                except:
                    try:
                        x=jt[i+1:].index('NNP')+i+1
                        if x==i+1:
                            l.append(w[i]+' '+w[x])
                            l.append(w[x])
                        elif x==i+2:
                            if jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS':
                                l.append(w[i]+' '+w[i+1]+' '+w[i+2])
                                l.append(w[i+2])
                        elif x==i+3:
                            if (jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS') and (jt[i+2]=='JJ' or jt[i+2]=='JJR' or jt[i+2]=='JJS' or jt[i+2]=='RB' or jt[i+2]=='RBR' or jt[i+2]=='RBS'):
                                l.append(w[i]+' '+w[i+1]+' '+w[i+2]+' '+w[i+3])
                                l.append(w[i+3])
                    except:
                        try:
                            x=jt[i+1:].index('NNS')+i+1
                            if x==i+1:
                                l.append(w[i]+' '+w[x])
                                l.append(w[x])
                            elif x==i+2:
                                if jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS':
                                    l.append(w[i]+' '+w[i+1]+' '+w[i+2])
                                    l.append(w[i+2])
                            elif x==i+3:
                                if (jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS') and (jt[i+2]=='JJ' or jt[i+2]=='JJR' or jt[i+2]=='JJS' or jt[i+2]=='RB' or jt[i+2]=='RBR' or jt[i+2]=='RBS'):
                                    l.append(w[i]+' '+w[i+1]+' '+w[i+2]+' '+w[i+3])
                                    l.append(w[i+3])
                        except:
                            try:
                                x=jt[i+1:].index('NNPS')+i+1
                                if x==i+1:
                                    l.append(w[i]+' '+w[x])
                                    l.append(w[x])
                                elif x==i+2:
                                    if jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS':
                                        l.append(w[i]+' '+w[i+1]+' '+w[i+2])
                                        l.append(w[i+2])
                                elif x==i+3:
                                    if (jt[i+1]=='JJ' or jt[i+1]=='JJR' or jt[i+1]=='JJS' or jt[i+1]=='RB' or jt[i+1]=='RBR' or jt[i+1]=='RBS') and (jt[i+2]=='JJ' or jt[i+2]=='JJR' or jt[i+2]=='JJS' or jt[i+2]=='RB' or jt[i+2]=='RBR' or jt[i+2]=='RBS'):
                                        l.append(w[i]+' '+w[i+1]+' '+w[i+2]+' '+w[i+3])
                                        l.append(w[i+3])
                            except:
                                pass

    return l

#subjects involved in comparison
def R8(sent):
    l=[]
    t=tag(sent)
    jt=[x[1] for x in t]
    w=nltk.word_tokenize(sent)
    for i in range(len(w)-1):
        if w[i]=='as' or w[i]=='As':
            if w[i+1]=='if' and i<len(w)-2:
                l.extend(R1(' '.join(w[i+2:])))
                l.extend(R3(' '.join(w[i+2:])))
                l.extend(R5(' '.join(w[i+2:])))
                l.extend(R6(' '.join(w[i+2:])))
                l.extend(R7(' '.join(w[i+2:])))
                l.extend(R9(' '.join(w[i+2:])))

            else:
                try:
                    x=w[i+1:].index('as')+i+1
                    #print(x)
                    l.extend(R1(' '.join(w[x+1:])))
                    l.extend(R3(' '.join(w[x+1:])))
                    l.extend(R5(' '.join(w[x+1:])))
                    l.extend(R6(' '.join(w[x+1:])))
                    l.extend(R2(' '.join(w[x+1:])))
                    l.extend(R9(' '.join(w[x+1:])))
                    if i>0:
                        l.extend(R1(' '.join(w[:i])))
                        l.extend(R3(' '.join(w[:i])))
                        l.extend(R5(' '.join(w[:i])))
                        l.extend(R6(' '.join(w[:i])))
                        l.extend(R2(' '.join(w[:i])))
                        l.extend(R9(' '.join(w[:i])))
                except:
                    pass
    l=list(set(l))
    return l


def R4_on_single_sent(s):
    r=[]
    l= [parse.tree() for parse in dep_parser.raw_parse(s)]
    root=l[0].label()
    #print(root)
    t=tag(s)
    w=nltk.word_tokenize(s)
    try:
        x=w.index(root)
        jt=[z[1] for z in t]
        fct=[y[0] for y in jt]
        if x>0 and x<len(w)-1:
            if fct[x]=='V' and w[x] not in p:
                s1=' '.join(w[:x])
                s2=' '.join(w[x+1:])
                # print(s1)
                # print(s2)
                p1=abs(TextBlob(s1).sentiment.polarity)
                p2=abs(TextBlob(s2).sentiment.polarity)
                if p1<p2:
                    r.append(s1)
                    r.extend(R6(s1))
                if p1>p2:
                    r.append(s2)
                    r.extend(R6(s2))
    except:
        pass
    return r
#uses above implementation for single sentence to implement rule 4 - lower sentimental side of verb - to text
def R4(sent):
    l=[]
    t=tag(sent)
    w=nltk.word_tokenize(sent)
    if(len(w))<3:
        return l
    jt=[z[1] for z in t]
    try:
        x=jt.index('.')
        #print(x)
        c1=len(w[:x])
        c2=len(w[x+1:])
        #print(c2)
        if c1>2 and c2>2:
            s1=' '.join(w[:x+1])
            s2=' '.join(w[x+1:])
            p1=abs(TextBlob(s1).sentiment.polarity)
            p2=abs(TextBlob(s2).sentiment.polarity)
            if p1<p2:
                l.append(s1)
                l.extend(R6(s1))
            if p1>p2:
                l.append(s2)
                l.extend(R6(s2))
        elif c1>2:
            s1=' '.join(w[:x+1])
            #print(s1)
            l.extend(R4_on_single_sent(s1))
        elif c2>2:
            s2=' '.join(w[x+1:])
            l.extend(R4_on_single_sent(s2))
    except:
        try:
            x=jt.index(':')
            c1=len(w[:x])
            c2=len(w[x+1:])
            s1=' '.join(w[:x+1])
            s2=' '.join(w[x+1:])
            if c1>1 and c2>1:

                p1=abs(TextBlob(s1).sentiment.polarity)
                p2=abs(TextBlob(s2).sentiment.polarity)
                if p1<p2:
                    l.append(s1)
                    l.extend(R6(s1))
                if p1>p2:
                    l.append(s2)
                    l.extend(R6(s2))
            elif c1>1:
                l.extend(R4_on_single_sent(s1))
            elif c2>1:
                l.extend(R4_on_single_sent(s2))
        except:
            pass

    return l



#print(R4_on_single_sent('So happy to just find out it has been decided to reschedule all my lectures and tutorials for me to night classes at the exact same times!'))

#print(R4("Got rejected in a job interview today. I am the happiest person alive!"))

# f=open('sam2.txt','r')
# for line in f:
#     print('R1 ',R1(line))
#     print('R2 ',R2(line))
#     print('R3 ',R3(line))
#     print('R4 ',R4(line))
#     print('R5 ',R5(line))
#     print('R6 ',R6(line))
#     print('R7 ',R7(line))
#     print('R8 ',R8(line))
#     print('R9 ',R9(line))
#     print('\n')

#print(R2(" Pranav is as good at coding as Rakhi Sawant is at acting."))