# global variables (for now)
logfile = "loglines.txt"
datetime_indicator = ' '

loglet = {"header": '', "content": []}
output = []

with open(logfile) as f:
    currentLine = f.readline()
    while f.readline():
        if currentLine.startswith('\n'):
            print ("line is blank")
            output.append(loglet)
            loglet['header'] = ''
            loglet['content'] = []
        elif currentLine.startswith(datetime_indicator):
            print "entering if branch"
            print currentLine
            loglet['header'] = currentLine
        else:
            print "entering else branch"
            print currentLine
            loglet['content'].append(currentLine)
        currentLine = f.readline()
    output.append(loglet)

print output[0]['content']
print output[1]['header']



