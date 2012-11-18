import codecs
import os
import sys
import time
import argparse

# User-installed dependencies
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from git import *

class GitTimeline(object):
    def __init__(self):
        self.files = dict()
        self.args = self.parseCommandLineArguments()
        self.input = self.args.input
        self.repo = Repo(self.input)
        self.fileRevisions = self.repo.git.log(self.input, format='%H').splitlines()
        self.css = open(self.sanitizeFilepath('%s/../TimelineStyle.css' % sys.argv[0]), 'r').read()

    @property
    def input(self):
        return self.files['input']

    @input.setter
    def input(self, value):
        self.files['input'] = self.sanitizeFilepath(value)

    @property
    def output(self):
        return self.files['output']

    @output.setter
    def output(self, value):
        self.files['output'] = value

    def parseCommandLineArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("input", help="The file you'd like to see a timeline of")
        parser.add_argument("--output", "-o", help="An optional name for the output file")
        parser.add_argument("--debug", "-d", action="store_true", help="output CSS and JS as separate files")
        return parser.parse_args()

    def getOutputFile(self):
        if self.args.output:
            self.output = self.safelyOpenOutputFile(self.args.output)
        else:
            (head, tail) = os.path.split(self.args.input)
            path = self.sanitizeFilepath('~/gitvisualizations/%s.html' % tail)
            self.output = self.safelyOpenOutputFile(pathname=path)
        return self

    def safelyOpenOutputFile(self, pathname):
        pathname = self.sanitizeFilepath(pathname)
        f = codecs.open(pathname, 'w', 'utf_8')
        return f

    def writeTimeline(self):
        self.fileRevisions.reverse()
        self.output.write('<html><head>\n%s\n</head><body><table><tr>\n' % self.css)
        [self.writeBlame(revision) for revision in self.fileRevisions]

        return None

    def writeBlame(self, revision):
        blame = self.repo.git.blame(revision, '--root', '--show-number', '--show-name', '-s', self.input)
        formattedCode = self.extractAndFormatCodeFromBlame(blame, revision)
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(self.repo.commit(revision).committed_date))
        self.output.write('<td><a class=timestamp, name=%s>%s</a><br />' % (revision, timestamp))
        self.output.write('<pre>%s</pre></td>' % formattedCode)
        return None

    def extractAndFormatCodeFromBlame(self, blame, revision):
        code = [self.parseBlameLine(line, revision)['code']
                    for line in blame.splitlines()]
        code = '%s\n' % '\n'.join(code)
        lexer = get_lexer_for_filename(self.input)
        formatter = HtmlFormatter(linenos=True, cssclass="source", style="monokai")
        return highlight(code, lexer, formatter)

    def parseBlameLine(self, line, revision):
        (blameInfo, code) = line.split(')', 1)
        (sha, fileName, oldLineNumber, newLineNumber) = blameInfo.split()
        isChanged = "unchanged"
        if (revision.startswith(sha)):
            isChanged = "changed"
        output = {'sha': sha,
                  'fileName': fileName,
                  'oldLineNumber': oldLineNumber,
                  'newLineNumber': newLineNumber,
                  'isChanged': isChanged,
                  'code': code}
        return output

    def closeFiles(self):
        [v.close() for v in self.files.values() if type(v) is file]
        return None

    def sanitizeFilepath(self, filepath):
        filepath = os.path.expanduser(filepath)
        if os.path.isabs(filepath) == False:
            filepath = os.path.join(os.getcwd(), filepath)
        filepath = os.path.normpath(filepath)
        return filepath

"""To handle the blame:

- Run the blame command
- Capture the result as a multi-line string
- split the string as line =  blame.splitlines()
- split the line as line = line.split(None, 4)
- Take the fourth element in each line list and concatenate them
    using '%s\n' % blame[24].split(None, 4)[4]

There's an issue of parsing, reconstructing, and splitting.

- The raw blame has to be split
- The split blame lines are parsed
- The extracted code is rejoined
- The rejoined code is pygmentized
- The pygmentized code is resplit
- The split pygmentized code is marked up with "changed"
- The split lines are reconstructed and written to file
"""




def outputCommits():
    '''Creates an HTML timeline
    of all a file's revisions.
    '''

    t = GitTimeline()
    t = t.getOutputFile()
    t.writeTimeline()
    t.closeFiles()
    return None

if __name__ == '__main__':
    outputCommits()






