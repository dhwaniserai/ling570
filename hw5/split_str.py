import sys


og_str = sys.argv[1]
# og_li = og_str.split('')

new_str=''
for ele in og_str:
    new_str += '\"'+ele+'\"' + ' '
    #new_str += ele
#new_str = ' '.join(new_li)

#print(new_str)
sys.stdout.write(new_str)
