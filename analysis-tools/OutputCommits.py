from git import *

def outputCommits(
  repositoryPath = '/Users/briandanielak/Dropbox/dev/roxygen',
  filename = 'DESCRIPTION'
  ):
  '''Creates an HTML timeline of all a file's revisions.

  '''

  repo = Repo(repositoryPath)
  hashes = getHashesOfFileCommits(repo, filename)
  blame = repo.git.blame('-s', filename)
  print hashes
  return None

def checkArguments(inputFile, outputFile):
  # if inputFile is None or !(git repo), throw exception
  # if outputFile is None, throw a helpful exception

def getHashesOfFileCommits(repo, file):
  return repo.git.log(file, format='%H').splitlines()


if __name__ == '__main__':
  outputCommits()



