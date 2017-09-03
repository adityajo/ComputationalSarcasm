import nltk

def ne(sent):
    # with open(filename, 'r') as f:
    #     sample = f.read()


    #sentences = nltk.sent_tokenize(sample)
    # tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    # tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    # chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
    #print list(chunked_sentences)
    words=nltk.word_tokenize(sent)
    tagged=nltk.pos_tag(words)
    chunked=nltk.ne_chunk(tagged, binary=True)

    def extract_entity_names(t):
        entity_names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_entity_names(child))

        return entity_names
    #
    # entity_names = []
    # for tree in chunked:
    #     # Print results per sentence
    #     # print extract_entity_names(tree)
    #
    #     entity_names.extend(extract_entity_names(tree))

    entity_names = extract_entity_names(chunked)

    #Print all entity names
    #print entity_names

    # Print unique entity names
    return list(set(entity_names))

#print(ne('Pranav Goel is as good at coding as Tom Cruise is at stunts.'))