import sys
import os 

def map_pos_lex(lexicon):
    lex_map = {}
    for t in lexicon:
        if len(t)== 2:
            if t[1] not in lex_map.keys():
                lex_map[t[1]] = [t[0]]
            else:
                lex_map[t[1]].append(t[0])
    return lex_map

with open(sys.argv[1],'r') as f:
    li_lexicon = f.readlines()
for i in range(len(li_lexicon)):
    li_lexicon[i] = li_lexicon[i].split()

lex_map = map_pos_lex(li_lexicon)

with open(sys.argv[2],'r') as f:
    morph = f.read().strip()
    morph = morph.split('\n')



op = []
op.append(morph.pop(0))
#print(op)
for rule in morph :
    rule = rule.strip()
    #op.append(rule)
    splits = rule.split()
    state1 = splits[0][1:]
    state2 = splits[1][1:]
    pos = splits[2][:-2]
    #print(lex_map)
    #print(state1,state2,pos)
    if pos in lex_map.keys():
        lexemes = lex_map[pos] #list eg:[walk,talk,impeach]
        for i in range(len(lexemes)):
            new_pos_state = str(pos) + '_'+ str(i)
            new_rule = '('+state1+ ' (' + new_pos_state + ' "'+lexemes[i][0]+'"))'
            op.append(new_rule)
            prev_state = new_pos_state
            for j in range(1,len(lexemes[i])):
                new_lex_state = new_pos_state + '_'+str(j)
                new_rule = '('+prev_state+ ' (' + new_lex_state + ' "'+lexemes[i][j]+'"))'
                op.append(new_rule)
                prev_state = new_lex_state
            new_rule = '('+prev_state+ ' (' + state2 + ' *e*))'
            op.append(new_rule)
    else:
        op.append(rule)
    

with open(sys.argv[3],'w+') as f:
    text = '\n'.join(op)
    f.write(text)
