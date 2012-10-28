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

def extractRepoAndFilename(inputFile):
  '''
    OutputCommits should take just a single inputFile
    argument and handle it gracefully

    repo = Repo(inputFile) automatically associates the
    nearest top-level Git directory.

    All that's needed is splitting the input file
    against the repo directory:

    repo.git_dir.split('/.git')[0]
  '''


def getHashesOfFileCommits(repo, file):
  return repo.git.log(file, format='%H').splitlines()


if __name__ == '__main__':
  outputCommits()



