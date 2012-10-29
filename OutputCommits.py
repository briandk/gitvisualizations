from git import *

def outputCommits(
  repositoryPath = '/Users/briandanielak/Dropbox/dev/roxygen',
  filename = 'DESCRIPTION'
  ):
  '''Creates an HTML timeline
  of all a file's revisions.
  '''

  repo = Repo(repositoryPath)
  revisions = getHashesOfFileCommits(repo, filename)
  blames = getBlames(repo, revisions)
  writeBlames(blames)

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


if __name__ == '__main__':
  outputCommits()



