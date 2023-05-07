import sys
from math import log10
#from math import pow

lm_file=sys.argv[1]
l1=float(sys.argv[2])
l2=float(sys.argv[3])
l3=float(sys.argv[4])
test_data=sys.argv[5]
output_file=sys.argv[6]

def read_lm(lm_file):
    text,lm = [], {}
    with open(lm_file,'r') as f:
        text = f.readlines()
    for i in range(len(text)):
        text[i] = text[i].strip()
    text = text[5:] # removing initial data sumary part
    for line in text:
        tokens = line.split()
        if len(tokens)==4:
            cnt = int(tokens[0])
            prob = float(tokens[1])
            log_p = float(tokens[2])
            ngram = tokens[3]
            lm[ngram] = {'count':cnt,'p':prob,'log':log_p}
            
        elif len(tokens)>4:
            cnt = int(tokens[0])
            prob = float(tokens[1])
            log_p = float(tokens[2])
            ngram = ' '.join(tokens[3:])
            lm[ngram] = {'count':cnt,'p':prob,'log':log_p}
    #print(lm.keys())
            
    #print(lm.values()[:5])
    return lm
def read_sent(sent_file):
    sents = []
    with open(sent_file,'r') as f:
        sents = f.readlines()
        #print(len(sents))
    for i in range(len(sents)):
        sents[i] = sents[i].strip()
    #print(len(sents))
    return sents

def get_prob(cur_word,context,lm):
    ngram = context + ' '+ cur_word
    if ngram in lm.keys():
        return lm[ngram]['p']
    else:
        return 0

lm=read_lm(lm_file)
#print('lm',lm['influential'])
test_sents = read_sent(test_data)

f=open(output_file,'w+')
index, p_sum=1, 0
word_num, oov_num = 0, 0
BOS, EOS='<s>', '</s>'
sent_num = len(test_sents)
for sent in test_sents:
    sent_words = len(sent.split(' '))
    word_num += sent_words
    sent = sent+' '+ EOS
    sent_mod = BOS+' '+sent
    f.write('Sent #'+str(index)+': '+sent_mod+'\n')
    index += 1
    tokens = sent_mod.split(' ')
    ##for first word
    logprob,sent_oov = 0.0,0
    if tokens[1] in lm.keys():
        p = l1*lm[tokens[1]]['p'] + l2*get_prob(tokens[1],BOS,lm)
        logprob=log10(p)
        p_sum += logprob
        f.write('lg P('+tokens[1]+' | '+BOS+') = '+str(log10(p))+'\n')
        #print(p)
    else:
        sent_oov +=1
        oov_num +=1
        p=0
        f.write('lg P('+tokens[1]+' | '+BOS+') = -inf (unknown word)'+'\n')
    for i in range(2,len(tokens)):
        if tokens[i] in lm.keys():
            p3 = l3*get_prob(tokens[i],' '.join(tokens[i-2:i]),lm)
            p2 = l2*get_prob(tokens[i],tokens[i-1],lm)
            p1 = l1*lm[tokens[i]]['p']
            p = p1+p2+p3
            f.write('lg P('+tokens[i]+' | '+' '.join(tokens[i-2:i])+') = '+str(log10(p))+'\n')
            #print(p)
            logprob += log10(p)
            p_sum += log10(p)
        else:
            sent_oov +=1
            oov_num +=1
            p=0
            f.write('lg P('+tokens[i]+' | '+' '.join(tokens[i-2:i])+') = -inf (unknown word)'+'\n')
    f.write('1 sentence, '+str(sent_words)+' words, '+str(sent_oov)+' OOVs:'+'\n')
    sent_ppl =pow(10, -logprob/(1+sent_words-sent_oov))
    f.write('logprob='+str(logprob)+' ppl='+str(sent_ppl)+'\n\n\n\n')
f.write('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
f.write('sent_num='+str(sent_num)+' word_num='+str(word_num) + ' oov_num='+str(oov_num)+'\n')

count = word_num + sent_num - oov_num
print('p_sum',p_sum)
total = -p_sum/count
ppl = pow(10,total)
print(ppl)
f.write('lgprob='+str(p_sum)+' ave_lgprob='+str(-total)+' ppl='+str(ppl)+'\n')
   
f.close()