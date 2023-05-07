import sys

def preprocess(text): #type List
    for i in range(len(text)):
        text[i] = text[i].strip()
        text[i] = '<s> ' + text[i] + ' </s>'
    return text

def get_unigrams(text):
    #blob = ' '.join(text)
    unigrams = {} # of type (t1): value

    for line in text:
        tokens = line.split(' ')
        for token in tokens:
            if token in unigrams.keys():
                unigrams[(token)] += 1
            else:
                unigrams[(token)] = 1
    sorted_unigrams = dict(sorted(unigrams.items(),
                        key=lambda item:item[1],
                        reverse=True))
    return sorted_unigrams

def get_bigrams(text):
    bigrams = {} # of type (t1,t2): value
    for line in text:
        tokens = line.split(' ')
        for i in range(0,len(tokens)-1):
            if (tokens[i],tokens[i+1]) not in bigrams:
                bigrams[(tokens[i],tokens[i+1])] = 1
                #print(tokens[i],tokens[i+1])
            else:
                bigrams[(tokens[i],tokens[i+1])]+=1
    sorted_bigrams = dict(sorted(bigrams.items(),
                        key=lambda item:item[1],
                        reverse=True))
    return sorted_bigrams

def get_trigrams(text):
    trigrams = {} # of type (t1,t2): value
    for line in text:
        tokens = line.split(' ')
        for i in range(0,len(tokens)-2):
            if (tokens[i],tokens[i+1],tokens[i+2]) not in trigrams:
                trigrams[(tokens[i],tokens[i+1],tokens[i+2])] = 1
            else:
                trigrams[(tokens[i],tokens[i+1],tokens[i+2])]+=1
    sorted_trigrams = dict(sorted(trigrams.items(),
                        key=lambda item:item[1],
                        reverse=True))
    return sorted_trigrams

def unigram_to_txt(unigram_di):
    li = [str(unigram_di[x])+'\t'+str(x) for x in unigram_di.keys()]
    txt = '\n'.join(li)
    return txt

def ngram_to_txt(ngram_di):
    li = [str(ngram_di[x])+'\t'+ ' '.join(x) for x in ngram_di.keys()]
    txt = '\n'.join(li)
    return txt

if __name__=="__main__":
    training_data = sys.argv[1]
    ngram_count_file = sys.argv[2]
    text = []
    with open(training_data,'r') as f:
        text=f.readlines()
    text = preprocess(text)
    unigram_di = get_unigrams(text)
    bigram_di = get_bigrams(text)
    trigram_di = get_trigrams(text)
    unigram_txt = unigram_to_txt(unigram_di)
    bigram_txt = ngram_to_txt(bigram_di)
    trigram_txt = ngram_to_txt(trigram_di)
    with open(ngram_count_file,'w+') as f:
        f.write(unigram_txt)
        f.write('\n')
        f.write(bigram_txt)
        f.write('\n')
        f.write(trigram_txt)


