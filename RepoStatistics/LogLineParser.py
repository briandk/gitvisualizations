import argparse
import subprocess

def create_git_log_call():
    command_line_arguments = ["--%s=%s" % (k,v)
                                  for k,v
                                  in vars(parseCommandLineArguments()).iteritems()
                                  if v is not None]
    print command_line_arguments

def parseCommandLineArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path", help="Path to the repo of interest")
    parser.add_argument("--since", help="the beginning of the time interval of interest")
    parser.add_argument("--until", help="the endpoint of the time interval of interest")
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

create_git_log_call()
