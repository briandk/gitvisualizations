import os
print os.getcwd()
with open("loglines.txt") as f:
    lines = f.read().splitlines()
    print lines

lines = [line for line in lines if line is not '']
print lines