import sys
op = sys.argv
op = op[1:]

if len(op)==0:
    sys.stdout.write("*NONE*")

else:
    new_op = ''.join(op)
    new_op = new_op.replace('#','/')
    new_op = new_op.replace('*',' ')
    sys.stdout.write(new_op)
