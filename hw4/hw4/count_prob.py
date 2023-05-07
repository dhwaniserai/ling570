import re
import sys
"""
split output of form "bb" into "b" "b"
"""
test_str = sys.argv[1]
#print("python")
#print(test_str)
test_str = test_str
test_li = test_str.split()
last = len(test_str)-1
prob = test_li.pop(-1)
#test_li.remove(last)
test_str = ' '.join(test_li)
#print(test_str)
#print("python end")
