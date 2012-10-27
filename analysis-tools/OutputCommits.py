from git import *

def outputCommits(repositoryName = None):
  '''Creates an HTML timeline of all a file's revisions.

  '''
  repo = Repo(repositoryName)
  assert repo.bare == False

  print repo

outputCommits('/Users/briandanielak/Dropbox/dev/roxygen')



