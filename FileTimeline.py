import codecs
import os
import sys
import time
import argparse
import shutil

# User-installed dependencies
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from git import *

class FileHandler(object):
    def __init__(self):
        self.args = self.parseCommandLineArguments()
        self.input = self.sanitizeFilepath(self.args.input)
        self.outputDirectory, self.outputFilename = self.getOutput()
        self.html = '%s.html' % os.path.join(self.outputDirectory, self.outputFilename)
        self.externalFiles = ['TimelineStyle.css']
        self.copyExternalFiles()

    def parseCommandLineArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("input", help="The file you'd like to see a timeline of")
        parser.add_argument("--output", "-o", help="An optional name for the output file")
        return parser.parse_args()

    def sanitizeFilepath(self, filepath):
        filepath = os.path.expanduser(filepath)
        if os.path.isabs(filepath) == False:
            filepath = os.path.join(os.getcwd(), filepath)
        filepath = os.path.normpath(filepath)
        return filepath

    def getOutputFile(self):
        outputPath = self.makeOutputDirectory()
        return codecs.open(path, 'w', 'utf_8')

    def getOutput(self):
        (rootPath, fileExtension) = os.path.splitext(self.sanitizeFilepath(self.args.input))
        (inputFilePath, filename) = os.path.split(rootPath)
        if self.args.output is None:
            outputPath = self.sanitizeFilepath(os.path.join('~/gitvisualizations', filename))
        else:
            outputPath = self.sanitizeFilepath(self.args.output)
        self.makeOutputDirectory(outputPath)
        return (os.path.join(outputPath), filename)

    def makeOutputDirectory(self, path):
        if os.path.exists(path) is not True:
            os.makedirs(path)

    def copyExternalFiles(self):
        for filename in self.externalFiles:
            source = os.path.join(os.path.dirname(__file__), filename)
            destination = os.path.join(self.outputDirectory, filename)
            shutil.copy(source, destination)


class GitTimeline(object):

    def __init__(self):
        self.files = FileHandler()
        self.repo = Repo(self.files.input)
        self.fileRevisions = self.repo.git.log(self.files.input, format='%H').splitlines()

    def writeTimeline(self):
        self.fileRevisions.reverse()
        with codecs.open(self.files.html, 'w', 'utf_8') as output:
            output.write("<html><head><link rel='stylesheet' href='TimelineStyle.css'></head><body><table><tr>\n")
            [self.writeBlame(revision, output) for revision in self.fileRevisions]
        return None

    def writeBlame(self, revision, output):
        blame = self.repo.git.blame(revision, '--root', '--show-number', '--show-name', '-s', self.files.input)
        formattedCode = self.extractAndFormatCodeFromBlame(blame, revision)
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(self.repo.commit(revision).committed_date))
        output.write('<td><a class=timestamp, name=%s>%s</a><br />' % (revision, timestamp))
        output.write('<pre>%s</pre></td>' % formattedCode)
        return None

    def extractAndFormatCodeFromBlame(self, blame, revision):
        code = [self.parseBlameLine(line, revision)['code']
                    for line in blame.splitlines()]
        code = '%s\n' % '\n'.join(code)
        lexer = get_lexer_for_filename(self.files.input)
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
    t.writeTimeline()
    return None

if __name__ == '__main__':
    outputCommits()






