import sys
from math import log10
ngram_count_file = sys.argv[1]
lm_file = sys.argv[2]

def unigram_lm(unigram_dict):
    lm = []
    total_count = int(sum(unigram_dict.values()))
    for uni in unigram_dict.keys():
        uni_count = int(unigram_dict[uni])
        prob = uni_count / total_count
        log_prob = log10(prob)
        gram_entry = [str(uni_count),str(prob),str(log_prob),str(uni)]
        lm.append(gram_entry)
    return lm

def ngram_lm(ngram_dict,one_less_gram_dict):
    lm = []
    for gram in ngram_dict.keys():
        one_less_gram = ' '.join(gram.split(' ')[:-1])
        total_count = int(one_less_gram_dict[one_less_gram])
        ngram_count = int(ngram_dict[gram])
        prob = ngram_count / total_count
        log_prob = log10(prob)
        gram_entry = [str(ngram_count),str(prob),str(log_prob),str(gram)]
        lm.append(gram_entry)
    return lm

#reading all ngrams
raw_text = []
with open(ngram_count_file,'r') as f:
    raw_text = f.readlines()
unigrams,bigrams,trigrams = {},{},{}
for line in raw_text:
    tokens = line.split()
    if len(tokens)==2:
        unigrams[tokens[1]]=int(tokens[0])
    elif len(tokens)==3:
        count = int(tokens.pop(0))
        bigrams[' '.join(tokens)]=count
    else:
        count = int(tokens.pop(0))
        trigrams[' '.join(tokens)]=count

lm_unigram = unigram_lm(unigrams)
lm_bigram = ngram_lm(bigrams,unigrams)
lm_trigram = ngram_lm(trigrams,bigrams)

#output write
f=open(lm_file,'w+')
f.write('\\data\\\n')
f.write('ngram 1: type='+str(len(unigrams.keys()))+' token='+str(sum(unigrams.values()))+'\n')
f.write('ngram 2: type='+str(len(bigrams.keys()))+' token='+str(sum(bigrams.values()))+'\n')
f.write('ngram 1: type='+str(len(trigrams.keys()))+' token='+str(sum(trigrams.values()))+'\n')
f.write('\n'+'\\1-grams:\n')
for ele in lm_unigram:
    f.write(' '.join(ele))
    f.write('\n')
f.write('\n'+'\\2-grams:\n')
for ele in lm_bigram:
    f.write(' '.join(ele))
    f.write('\n')
f.write('\n'+'\\3-grams:\n')
for ele in lm_trigram:
    f.write(' '.join(ele))
    f.write('\n')
f.write('\n'+'\\end\\\n')
f.close()
#print(unigram.keys())
#print(bigram.keys())
#print(trigram.keys())