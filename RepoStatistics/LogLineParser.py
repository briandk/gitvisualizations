import argparse
import subprocess

class GitLogCaller(object):
    def __init__(self):
        self.args = self.parseCommandLineArguments()
        self.git_log_call = ["git", "log", "--numstat", "--date=iso", "--format=' %H,%ad'"]
        self.git_log_call.extend(self.create_git_log_call())
        for item in self.git_log_call:
            print item

    def create_git_log_call(self):
        optional_arguments = ["since", "until"]
        command_line_arguments = ["--%s='%s'" % (k,v)
                                      for k,v
                                      in vars(self.args).iteritems()
                                      if k in optional_arguments and v is not None]
        return command_line_arguments

    def parseCommandLineArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("repo_path", help="Path to the repo of interest")
        parser.add_argument("--since", help="the beginning of the time interval of interest")
        parser.add_argument("--until", help="the endpoint of the time interval of interest")
        return parser.parse_args()

    def parse_log_lines(self):
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

g = GitLogCaller()
