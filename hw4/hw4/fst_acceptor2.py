#modifying fsa solution from hw2 for fst
from copy import deepcopy
import sys


class FST:
    def __init__(self, initial_state, final_states, states, vocab, rules, flag):
        self.initial_state = initial_state
        self.final_states = final_states
        self.states = states
        self.vocab = vocab
        self.rules = rules
        self.flag = flag

    @ classmethod
    def from_carmel_format(cls, fst_file):
        with open(fst_file, 'r', encoding='utf8') as f:
            lines = f.readlines()

        final_states = set()
        states = set()
        vocab = set()
        rules = {}
        final_states.add(lines[0].strip())
        initial_state = None
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                continue
            splits = line.split()
            from_state = splits[0][1:]
            to_state = splits[1][1:]
            input_symbol = splits[2]
            output_symb = splits[3][:-2] ##check
            trans_prob = 1.0
            if len(splits) == 5:
                output_symb = splits[3]
                trans_prob = float(splits[4][:-2])

            if initial_state is None:
                initial_state = from_state

            if from_state not in states:
                states.add(from_state)
            if to_state not in states:
                states.add(to_state)
            if input_symbol not in vocab and not input_symbol == '*e*':
                vocab.add(input_symbol)
            flag = True
            if from_state not in rules:
                rules[from_state] = {}
            if input_symbol in rules[from_state]:
                flag = False
            if input_symbol not in rules[from_state]:
                rules[from_state][input_symbol] = [to_state,output_symb,trans_prob]
            #rules[from_state][input_symbol].add(to_state) ##check
            
        
        #print(rules)
        fst = cls(initial_state, final_states, states, vocab, rules,flag)

        return fst

    def _get_to_sates(self, states, symbol):
        assert not symbol == '*e*'
        new_states = set()
        for state in states:
            if state not in self.rules or symbol not in self.rules[state]:
                continue
            to_states = self.rules[state][symbol]
            new_states.update(to_states)
        return new_states

    @ staticmethod
    def rename_set(states):
        return '_'.join(sorted(list(states)))

    ## removed to_dfa renamed accept_dfa to accept_fst
    def accept_fst(self, symbol_list):
        current_state = self.initial_state
        current_op = ''
        current_prob = 1.0

        if symbol_list[0] == '*e*':
            if self.initial_state in self.final_states:
                return (True, current_op, current_prob)
            else:
                return (False, current_op, current_prob)

        for symbol in symbol_list:
            if symbol not in self.vocab:
                return (False, current_op,current_prob)

            if current_state not in self.rules or symbol not in self.rules[current_state]:
                return (False, current_op,current_prob)

            to_states = self.rules[current_state][symbol]
            assert len(to_states) == 3

            current_state = to_states[0] #to_states is a list
            current_op += " "+ to_states[1]
            current_prob *= to_states[2]

        if current_state in self.final_states: #change return to account for output and probability
            return (True, current_op,current_prob)
        #epsilon = '*e*'
        elif ('*e*' in self.rules[current_state].keys()) and (self.rules[current_state]['*e*'][0] in self.final_states):
            current_op += " " + self.rules[current_state]['*e*'][1]
            current_prob *= self.rules[current_state]['*e*'][2]
            return (True, current_op,current_prob) 
            #not checked for S e A and A e B case
        else:
            return (False, current_op,current_prob)


fst_file = sys.argv[1]
symbol_file = sys.argv[2]

fst = FST.from_carmel_format(fst_file)
if fst.flag == False:
    print("The input FST is ambiguous")

else:

    with open(symbol_file, 'r', encoding='utf8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        symbols = line.split()

        accept = fst.accept_fst(symbols)

        if accept[0]:
            output_str = line + ' => ' + accept[1] + ' ' + str(accept[2])
        else:
            output_str = line + ' => *none* 0'

        print(output_str)
