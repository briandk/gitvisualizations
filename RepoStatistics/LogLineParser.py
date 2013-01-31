import argparse
import subprocess

# user-installed dependencies
import git

# Locally-defined modules
import Loglet

class GitLogData(object):
    def __init__(self):
        self.args = self.parseCommandLineArguments()
        self.git_loglines = self.get_git_log().splitlines(True)
        print self.git_loglines[0:4]

    def get_git_log(self):
        arguments = ["git", "log", "--numstat", "--date=iso", "--format=' %H,%ad'"]
        arguments = arguments.extend(self.get_optional_arguments())
        repo = git.Repo(self.args.repo_path)
        return repo.git.log(arguments)

    def get_optional_arguments(self):
        optional_flags = ["since", "until"]
        return ["--%s='%s'" % (k,v)
                    for k,v
                    in vars(self.args).iteritems()
                    if k in optional_flags and v is not None]


    def parseCommandLineArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("repo_path", help="Path to the repo of interest")
        parser.add_argument("--since", help="the beginning of the time interval of interest")
        parser.add_argument("--until", help="the endpoint of the time interval of interest")
        return parser.parse_args()

    def parse_log_lines(self):
        datetime_indicator = ' '
        blank_line_indicator = '\n'
        working_loglet = Loglet()
        output = []
        with open(logfile) as f:
            current_line = f.readline()
            while f.readline():
                if currentLine.startswith(blank_line_indicator):
                    output.append(working_loglet)
                    working_loglet = Loglet()
                elif currentLine.startswith(datetime_indicator):
                    working_loglet.add_header(current_line)
                else:
                    working_loglet.add_content()
                currentLine = f.readline()
            output.append(loglet)
        return output

g = GitLogData()
