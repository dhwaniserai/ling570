import sys
import re
import numpy as np
from collections import defaultdict


class Bigram_HMM:

    def __init__(self):
        """set that contains all distinct words"""
        self.known_words = set()

        """numpy array of shape(N,) which contains all distinct words"""
        self.order_known_words = np.array([])

        """set that contains all distinct tags"""
        self.tags = set()

        """numpy array of shape(N,) which contains all distinct tags"""
        self.order_tags = np.array([])

        """dict which counts num of occurrence for each word"""
        self.count_words = defaultdict(int)

        """dict which counts occurrence of tags."""
        self.count_tags = defaultdict(int)

        """dict which counts occurrence of all pairs (word, tag)."""
        self.count_word_tag_pairs = defaultdict(int)

    def read_data(text_file):
        text_file=text_file.strip()
        raw_sents = text_file.split('\n')
        #raw_sents = ['<s>/BOS '+sent+' <\/s>/EOS' for sent in raw_sents]
        text_sentences = [sent.split(' ') for sent in raw_sents]
        final_sentences = [] #"/[!\]*$"
        for sentence in text_sentences:
            sentence.insert(0, '<s>/BOS')
            sentence.append('<\/s>/EOS')
            for i in range(len(sentence)):
                #print(sentence[i])
                word,tag= re.split(r"(?<!\\)/", sentence[i])
                
                sentence[i] = (word,tag)
            final_sentences.append(sentence)
        return final_sentences

    def populate_counts(self, training_data):
        #training = flattened sentence list
        WORD = 0
        TAG = 1
        temp1 = []
        temp2 = []

        for word in training_data: # note that word is actually a tuple of (word, POS)
            if word[WORD] not in self.known_words:
                temp2.append(word[WORD])

            if word[TAG] not in self.tags:
                temp1.append(word[TAG])

            self.known_words.add(word[WORD])
            self.tags.add(word[TAG])
            self.count_words[word[WORD]] += 1
            self.count_tags[word[TAG]] += 1
            self.count_word_tag_pairs[word] += 1

        self.order_known_words = np.sort(np.array(temp2))
        self.order_tags = np.sort(np.array(temp1))
    
    def count_consecutive_tags(self, training_data): #non-flat training_data
        """
        Return a dict which contains:
        result[(tag_n, tag_m)] = Count(tag_n, tag_m)
        """
        WORD = 0
        TAG = 1
        result = defaultdict(int)

        for sent in training_data:

            for i in range(len(sent)-1):
                result[(sent[i][TAG], sent[i+1][TAG])] += 1

        return result

    def transition_probabilities(self, training_data):
        """
        Computes the transition probabilities of a bigram HMM tagger
        on the training set, using MLE.
        :return: t - a 2D numpy array of shape (#training_tags, #training_tags)
         which contains the probabilities to get tag_i given tag_j was previous:
         t[i][j] =P(tag_i|tag_j) = Count(tag_j, tag_i)/Count(tag_j)
         where:
         i = np.where(order_training_tags == tag_i)[0][0]
         j = np.where(order_training_tags == tag_j)[0][0]
        """

        count_tags_pairs = self.count_consecutive_tags(training_data)

        #number of distinct tags in training set
        num_tags = self.order_tags.shape[0]
        t = np.empty((num_tags, num_tags), dtype=float)

        for i in range(num_tags):
            tag1 = self.order_tags[i]
            for j in range(num_tags):
                tag2 = self.order_tags[j]
                t[i, j] = count_tags_pairs[(tag1, tag2)] / self.count_tags[tag2]

        return t

    def emission_probabilities(self, add_one=False):
        """
        Computes the emission probabilities of a bigram HMM tagger
        on the training set, using MLE.
        :param add_one: if True, calculate the probability with add-one smoothing.
        :return: e -  a 2D numpy array of shape(#training_tags, #training_words_type)
        which contains the probabilities to assign word_i to a given tag_i:
        e[i1][i2] =P(word_i2|tag_i1) = Count(tag_i1, word_i2) / Count(tag_i1)
        and with add-one:            = (Count(tag_i1, word_i2)+1) / (Count(tag_i1) +V)
        where:
        V = current vocabulary length (distinct known and unknown words)
        i1 = np.where(order_training_tags == tag_i1)[0][0]
        i2 = np.where(order_known_words == word_i2)[0][0]
        """

        #number of distinct tags in training set
        num_tags = self.order_tags.shape[0]
        #number of distinct words in training set
        num_words_type = self.order_known_words.shape[0]

        e = np.empty((num_tags, num_words_type), dtype=float)

        for i in range(num_tags):
            tag = self.order_tags[i]
            for j in range(num_words_type):
                word = self.order_known_words[j]
                if (add_one):
                    e[i, j] = (self.count_word_tag_pairs[(word, tag)] + 1) /\
                              (self.count_tags[tag] + len(self.known_words)
                                                                    + len(self.unknown_words))
                else:
                    e[i, j] = self.count_word_tag_pairs[(word, tag)] / self.count_tags[tag]
        return e
    def write_output(self,output_file, trans_prob, emiss_prob):
        op = []
        op.append("state_num="+str(len(self.known_words)))
        op.append("sym_num="+str(len(self.tags)))
        op.append("init_line_num=1")
        op.append("trans_line_num="+str(trans_prob.size))
        op.append("emiss_line_num="+str(emiss_prob.size))

        f=open(output_file,'w+')
        f.write('\n'.join(op))
        f.write('\n\n\\init\nBOS\t1.0\n')
        f.write('\n\n\n\\transition\n')
        
        num_tags = self.order_tags.shape[0]

        for i in range(num_tags):
            tag1 = self.order_tags[i]
            for j in range(num_tags):
                tag2 = self.order_tags[j]
                if trans_prob[i,j]!=0:
                    f.write(tag1+'\t'+tag2+'\t'+str(trans_prob[i,j]))
                    f.write('\n')
        #f.write(str(np.matrix(trans_prob)))
        f.write('\n\n\n\\emission\n')
        num_words_type = self.order_known_words.shape[0]
        for i in range(num_tags):
            tag = self.order_tags[i]
            for j in range(num_words_type):
                word = self.order_known_words[j]
                if emiss_prob[i,j]!=0:
                    f.write(tag+'\t'+word+'\t'+str(emiss_prob[i,j]))
                    f.write('\n')
        #f.write(str(np.matrix(emiss_prob)))


if __name__== "__main__":
    output_file = sys.argv[1]
    training_file = open('/dev/stdin').read()
    #print(training_file[:20])
    train_data = Bigram_HMM.read_data(training_file)
    #print(train_data)
    flat_training_data = [item for sublist in train_data for item in sublist]
    bigram = Bigram_HMM()
    bigram.populate_counts(flat_training_data)
    trans_prob = bigram.transition_probabilities(train_data)
    emiss_prob = bigram.emission_probabilities()
    bigram.write_output(output_file, trans_prob, emiss_prob)


