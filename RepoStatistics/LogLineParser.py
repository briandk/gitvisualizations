import argparse
import subprocess

# user-installed dependencies
import git

# Locally-defined modules
from Loglet import Loglet

class GitLogData(object):
    def __init__(self):
        self.args = self.parseCommandLineArguments()
        self.git_log_lines = self.get_git_log().splitlines(True)
        loglets = self.parse_log_lines(self.git_log_lines)

    def get_git_log(self):
        arguments = ['--numstat', '--date=iso', '--format= %H,%ad']
        optional_arguments = self.get_optional_arguments()
        if optional_arguments is not []:
            arguments.extend(optional_arguments)
        repo = git.Repo(self.args.repo_path)
        return repo.git.log(arguments)

    def get_optional_arguments(self):
        optional_flags = ["since", "until"]
        output =  ["--%s=%s" % (k,v)
                       for k,v
                       in vars(self.args).iteritems()
                       if k in optional_flags and v is not None]
        return output


    def parseCommandLineArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("repo_path", help="Path to the repo of interest")
        parser.add_argument("--since", help="the beginning of the time interval of interest")
        parser.add_argument("--until", help="the endpoint of the time interval of interest")
        return parser.parse_args()

    def parse_log_lines(self, log_lines):
        datetime_indicator = ' '
        blank_line_indicator = '\n'
        working_loglet = Loglet()
        output = []
        for line in self.git_log_lines:
                if line.startswith(blank_line_indicator):
                    output.append(working_loglet)
                    working_loglet = Loglet()
                elif line.startswith(datetime_indicator):
                    working_loglet.add_header(line)
                else:
                    working_loglet.add_content(line)
        return output



g = GitLogData()
