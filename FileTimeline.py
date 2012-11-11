import os
import sys
import time
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from git import *

class GitTimeline(object):
    def __init__(self):
        self.files = dict()
        self.args = sys.argv
        self.input = self.getInputPathFromCommandline()
        self.repo = Repo(self.input)
        self.fileRevisions = self.repo.git.log(self.input, format='%h').splitlines()
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

    def getInputPathFromCommandline(self):
        try:
            path = self.args[1]
        except IndexError:
            print "\nSorry, it looks like you didn't specify an input file."
            print "proper usage for this script is 'python inputFile [outputFile]'\n"
        return path


    def getOutputFile(self):
        if (len(self.args) >= 3):
            self.output = self.safelyOpenOutputFile(self.args[2])
        else:
            path = os.path.split(self.args[1])[1]
            path = self.sanitizeFilepath('~/gitvisualizations/%s.html' % path)
            self.output = self.safelyOpenOutputFile(pathname=path)
        return self

    def safelyOpenOutputFile(self, pathname):
        pathname = self.sanitizeFilepath(pathname)
        f = open(pathname, 'w')
        return f

    def writeTimeline(self):
        self.fileRevisions.reverse()
        self.output.write('<html><head>\n%s\n</head><body><table><tr>\n' % self.css)
        [self.writeBlame(revision) for revision in self.fileRevisions]

        return None

    def writeBlame(self, revision):
        blame = self.repo.git.blame(revision, '--root', '--show-number', '--show-name', '-s', self.input)
        formattedCode = self.extractAndFormatCodeFromBlame(blame)
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(self.repo.commit(revision).committed_date))
        self.output.write('<td><a class=timestamp, name=%s>%s</a><br />' % (revision, timestamp))
        self.output.write('<pre>%s</pre></td>' % formattedCode)
        return None

    def extractAndFormatCodeFromBlame(self, blame):
        blame = blame.splitlines()
        code = [line.split(') ', 1)[1] for line in blame]
        code = '%s\n' % '\n'.join(code)
        lexer = get_lexer_for_filename(self.input)
        formatter = HtmlFormatter(linenos=True, cssclass="source", style="monokai")
        return highlight(code, lexer, formatter)

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






