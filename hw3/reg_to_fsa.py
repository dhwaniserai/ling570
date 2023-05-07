import sys
import nltk
input_file = ""
text = ""
#with open(input_file,"r") as f:
#    text = f.read()
#    text=text.strip()

#account for 3 types of right grammar productions
class Grammar:
    def __init__:
        self.text=""
        self.final = "_F_"
        self.final_states=[]
        #self.seen_states = []
    def convert_type1(self,prod):
        #type1 prods A t B where t is a terminal and B is a non-terminal
        elements = prod.split()
        if elements[1] == "*e*"
            print('('+elements[0]+' '+'('+elements[2]+' *e*))')

        else:
            print('('+elements[0]+' '+'('+elements[2]+' \"'+elements[1]+'\"))')

        if elements[0] in self.final_states:
            index = self.final_states.index(elements[0])
            self.final_states[index] = elements[2]
        else:
            self.final_states.append(elements[2])

    def convert_type2(self,prod): #A => terminal i.e. A t
        elements = prod.split()
        if elements[1] == "*e*"
            print('('+elements[0]+' '+'('+self.final+' *e*))')

        else:
            print('('+elements[0]+' '+'('+self.final+' \"'+elements[1]+'\"))')

    def convert_other_finals_to_final(self):
        if len(self.final_states) != 0:
            for state in self.final_states:
                print('('+state+' '+'('+self.final+' *e*))')
    
    if __name__ == "__main__":
        file_path = sys.argv[0]

        obj = Grammar()

        with open(file_path,"r") as f:
            obj.text = f.read()
            obj.text=obj.text.strip()
        for line in obj.text.split('\n'):
            if len(line.split())==3:
                obj.convert_type1(line)

            else:
                obj.convert_type2(line)
        obj.convert_other_finals_to_final()
            

