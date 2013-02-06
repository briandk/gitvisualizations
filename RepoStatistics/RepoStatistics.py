import argparse
import subprocess
import os.path

# user-installed dependencies
import git

# Locally-defined modules
from Loglet import Loglet

class GitLogData(object):
    def __init__(self):
        self.args = self.parseCommandLineArguments()
        self.git_log_lines = self.get_git_log().splitlines(True)
        self.loglets = self.parse_log_lines(self.git_log_lines)
        self.write_output()
        self.call_R()

    def get_git_log(self):
        arguments = ['--numstat', '--date=iso', '--format= %H,%ad']
        optional_arguments = self.get_optional_arguments()
        if optional_arguments is not []:
            arguments.extend(optional_arguments)
        repo = git.Repo(self.sanitize_filepath(self.args.repo_path))
        return repo.git.log(arguments)

    def sanitize_filepath(self, filepath):
        filepath = os.path.expanduser(filepath)
        if os.path.isabs(filepath) == False:
            filepath = os.path.join(os.getcwd(), filepath)
        filepath = os.path.normpath(filepath)
        return filepath

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
                if line.startswith(datetime_indicator):
                    output.append(working_loglet)
                    working_loglet = Loglet()
                    working_loglet.add_header(line)
                elif line.startswith('\n'):
                    pass
                else:
                    working_loglet.add_content(line)
        return output

    def write_output(self):
        output_path = os.path.join(self.args.repo_path, "repo_statistics.csv")
        with open(output_path, 'w') as output_file:
            self.write_columns(output_file)
            self.write_loglets(output_file)

    def write_columns(self, output_file):
        columns = ['sha',
                   'date',
                   'time',
                   'datetime',
                   'filename',
                   'lines_added',
                   'lines_deleted']
        output_file.write('%s\n' % ','.join(columns))

    def write_loglets(self, output_file):
        for loglet in self.loglets:
            for item in loglet.diffstats:
                output = '%s,%s,%s,%s,%s,%s,%s' % (loglet.sha,
                                                   loglet.date,
                                                   loglet.time,
                                                   loglet.datetime,
                                                   item.filename,
                                                   item.lines_added,
                                                   item.lines_deleted)
                output_file.write('%s\n' % output)

    def call_R(self):
        script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RepoStatistics.R')
        with open(script_path) as r_script:
            subprocess.call(['R',
                             '--vanilla',
                             '--args',
                             self.args.repo_path],
                             stdin = r_script)

g = GitLogData()