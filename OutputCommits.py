import os
import sys
import pdb

from git import *

class GitTimeline(dict):
    def __init__(self):
        dict.__init__(self)
        self['repo'] = Repo('/Users/briandanielak/Dropbox/dev/roxygen') # replace with sys.argv[1]

def outputCommits(
  repositoryPath = '/Users/briandanielak/Dropbox/dev/roxygen',
  filename = 'DESCRIPTION'
  ):
  '''Creates an HTML timeline
  of all a file's revisions.
  '''

  t = GitTimeline()
  print t['repo']
  # revisions = getHashesOfFileCommits(repo, filename)
  # blames = getBlames(repo, revisions)
  # pdb.set_trace()
  # writeTimeline(revisions, blames)

  return None

def checkArguments(inputFile, outputFile):
  '''
  if inputFile is None or !(git repo), throw exception
  if outputFile is None, throw a helpful exception
  '''

def getHashesOfFileCommits(repo, file):
  return repo.git.log(file, format='%H').splitlines()

def getBlames(repo, revisions):
  return (
    [repo.git.blame(revision, '--root', '--show-number', '-s', 'DESCRIPTION').splitlines() for revision in revisions]
  )

def writeBlames(blames):
  print '\n'.join(blames[0])

  return None

def openOutputFile(pathname):
    pathname = os.path.expanduser(pathname)
    if os.path.isfile(pathname):
        try:
            f = open(pathname, 'w')
            f.write('')
            f.close()
        except IOError:
            pass

    f = open(pathname, 'a')
    return f


if __name__ == '__main__':
  outputCommits()

def writeTimeline(revisions, blames, outputFile='~/gitdatacollection/aaa.html'):
  css = open(os.path.normpath('%s/../TimelineStyle.css' % sys.argv[0]), 'r')
  output =  openOutputFile(outputFile)

  print css
  return None





