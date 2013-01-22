import argparse

def create_csv():
    args = parseCommandLineArguments()
    lines = parse_log_lines(args.repo_path)

def parseCommandLineArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path", help="Path to the repo of interest")
    return parser.parse_args()

def parse_log_lines(logfile):
    datetime_indicator = ' '
    blank_line_indicator = '\n'
    loglet = {"header": '',
              "content": []}
    output = []
    with open(logfile) as f:
        currentLine = f.readline()
        while f.readline():
            if currentLine.startswith(blank_line_indicator):
                output.append(loglet)
                loglet['header'] = ''
                loglet['content'] = []
            elif currentLine.startswith(datetime_indicator):
                loglet['header'] = currentLine
            else:
                loglet['content'].append(currentLine)
            currentLine = f.readline()
        output.append(loglet)
    return output
