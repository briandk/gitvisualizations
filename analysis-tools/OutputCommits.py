from git import *

def outputCommits(
  repositoryPath = '/Users/briandanielak/Dropbox/dev/testrepo',
  filename = 'test.txt'
  ):
  '''Creates an HTML timeline of all a file's revisions.

  '''
  repo = Repo(repositoryPath)
  print repo.blame('master', filename)


if __name__ == '__main__':
  outputCommits()



