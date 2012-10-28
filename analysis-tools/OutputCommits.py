from git import *

def outputCommits(
  repositoryPath = '/Users/briandanielak/Dropbox/dev/roxygen',
  filename = 'DESCRIPTION'
  ):
  '''Creates an HTML timeline of all a file's revisions.

  '''
  def getHashesOfFileCommits(file):
    return repo.git.log(file, format='%H').splitlines()

  repo = Repo(repositoryPath)
  hashes = getHashesOfFileCommits(filename)
  blame = repo.git.blame('-s', filename)
  print hashes



if __name__ == '__main__':
  outputCommits()



