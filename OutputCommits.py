import os
import sys
import pdb

from git import *

class GitTimeline(dict):
    def __init__(self):
        file = '/Users/briandanielak/Dropbox/dev/roxygen/DESCRIPTION' # replace with sys.argv[1]
        self['repo'] = Repo(file)
        self['fileRevisions'] = self['repo'].git.log(file, format='%H').splitlines()
        self['blames'] = [self['repo'].git.blame(revision, '--root', '--show-number', '-s', file).splitlines()
                            for revision in self['fileRevisions']]
        self['css'] = open(os.path.normpath('%s/../TimelineStyle.css' % sys.argv[0]), 'r').read()
        self['output'] = ''

    def openOutputFile(self, pathname='~/gitdatacollection/foo.html'):
        pathname = os.path.expanduser(pathname)
        if os.path.isfile(pathname):
            try:
                f = open(pathname, 'w')
                f.write('')
                f.close()
            except IOError:
                pass

        self['output'] = open(pathname, 'a')
        return self

    def writeTimeline(self):
        self['output'].write('<html><head>\n%s\n</head><body><table><tr>' % t['css'])

        return None

    def closeFiles(self):
        [v.close() for v in self.values() if type(v) is file]
        return None


def outputCommits(
    repositoryPath = '/Users/briandanielak/Dropbox/dev/roxygen',
    filename = 'DESCRIPTION'
    ):
    '''Creates an HTML timeline
    of all a file's revisions.
    '''

    t = GitTimeline()
    t = t.openOutputFile()
    t.closeFiles()
    # revisions = getHashesOfFileCommits(repo, filename)
    # blames = getBlames(repo, revisions)
    # pdb.set_trace()
    # writeTimeline(revisions, blames)

    return None

def writeBlames(blames):
    print '\n'.join(blames[0])

    return None

if __name__ == '__main__':
    outputCommits()






