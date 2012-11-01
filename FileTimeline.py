import os
import sys
import time

from git import *

class GitTimeline(object):
    def __init__(self):
        file = '/Users/briandanielak/Desktop/testrepo/test.txt' # replace with sys.argv[1]
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

    def getInputPathFromCommandline(self):
        # path = None
        try:
            path = self.args[1]
        except IndexError:
            print "\nSorry, it looks like you didn't specify an input file."
            print "proper usage for this script is 'python inputFile [outputFile]'\n"
        return path


    def openOutputFile(self, pathname='~/gitdatacollection/foo.html'):
        pathname = os.path.expanduser(pathname)
        if os.path.isfile(pathname):
            try:
                f = open(pathname, 'w')
                f.write('')
                f.close()
            except IOError:
                pass

        self.output = open(pathname, 'a')
        return self

    def writeTimeline(self):
        self.fileRevisions.reverse()
        self.output.write('<html><head>\n%s\n</head><body><table><tr>\n' % self.css)
        [self.writeBlame(revision) for revision in self.fileRevisions]

        return None

    def writeBlame(self, revision):
        blame = self.repo.git.blame(revision, '--root', '--show-number', '--show-name', '-s', self.input).splitlines()
        blame = [line.startswith(revision) and '<span class="changed">%s</span>' % line or line
                    for line in blame]
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(self.repo.commit(revision).committed_date))
        self.output.write('<td><a class=timestamp, name=%s>%s</a><br />' % (revision, timestamp))
        self.output.write('<pre>%s</pre></td>' % '\n'.join(blame))
        return None

    def closeFiles(self):
        [v.close() for v in self.files.values() if type(v) is file]
        return None

    def sanitizeFilepath(self, filepath):
        p = os.path.expanduser(filepath)
        p = os.path.normpath(p)
        return p


def outputCommits():
    '''Creates an HTML timeline
    of all a file's revisions.
    '''

    t = GitTimeline()
    t = t.openOutputFile()
    t.writeTimeline()
    t.closeFiles()

    return None

if __name__ == '__main__':
    outputCommits()






