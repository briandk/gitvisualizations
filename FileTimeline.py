import codecs
import os
import sys
import time
import argparse
import shutil

# User-installed dependencies
from git import *
import pystache

class FileHandler(object):
    def __init__(self):
        self.args = self.parseCommandLineArguments()
        self.input = self.sanitizeFilepath(self.args.input)
        self.outputDirectory, self.outputFilename = self.getOutput()
        self.html = '%s.html' % os.path.join(self.outputDirectory, self.outputFilename)
        self.externalFiles = ['TimelineStyle.css',
                              'prism.js',
                              'prism.css',
                              'jQuery.js',
                              'bootstrap.min.js',
                              'bootstrap.css']
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

    def getHTMLOutputFile(self):
        path = '%s.html' % os.path.join(self.outputDirectory, self.outputFilename)
        return codecs.open(path, 'w', 'utf_8')

    def getOutput(self):
        (rootPath, fileExtension) = os.path.splitext(self.sanitizeFilepath(self.args.input))
        (inputFilePath, filename) = os.path.split(rootPath)
        if self.args.output is None:
            outputPath = self.sanitizeFilepath(os.path.join('~/gitvisualizations', filename))
        else:
            outputPath = self.sanitizeFilepath(self.args.output)
        self.makeOutputDirectory(outputPath)
        return (outputPath, filename)

    def makeOutputDirectory(self, path):
        if os.path.exists(path) is not True:
            os.makedirs(path)

    def copyExternalFiles(self):
        for filename in self.externalFiles:
            source = os.path.join(os.path.dirname(__file__), filename)
            destination = os.path.join(self.outputDirectory, filename)
            shutil.copy(source, destination)

class TimelineView(object):
    def __init__(self, model):
        self.model = model

    def snapshots(self):
        return self.model.snapshots

    def revisions(self):
        return ','.join(['"%s"' % revision for revision in self.model.fileRevisions])

class Controller(object):
    def __init__(self):
        self.files = FileHandler()
        self.model = GitTimeline(self.files.input)
        self.view = TimelineView(self.model)

    def render(self):
        renderer = pystache.Renderer()
        with self.files.getHTMLOutputFile() as output:
            output.write(renderer.render(self.view))
        return None

class GitTimeline(object):

    def __init__(self, inputFile):
        self.repo = Repo(inputFile)
        self.fileRevisions = self.repo.git.log('--reverse', inputFile, format='%H').splitlines()
        self.blames = [self.repo.git.blame(revision, '--root', '--show-number', '--show-name', '-s', inputFile)
                          for revision in self.fileRevisions]
        self.snapshots = [self.composeSnapshot(blame, revision) for (blame, revision) in zip(self.blames, self.fileRevisions)]

    def composeSnapshot(self, blame, revision):
        blamelets = [self.parseBlameLine(line, revision) for line in blame.splitlines()]
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(self.repo.commit(revision).committed_date))
        return {'blamelets': blamelets,
                'code': '\n'.join([blamelet['code'] for blamelet in blamelets]),
                'changedLines': ','.join([blamelet['newLineNumber'] for blamelet in blamelets if blamelet['isChanged']]),
                'revision': revision,
                'timestamp': timestamp}

    def parseBlameLine(self, line, revision):
        (blameInfo, code) = line.split(')', 1)
        (sha, fileName, oldLineNumber, newLineNumber) = blameInfo.split()
        isChanged = False
        if (revision.startswith(sha) is True):
            isChanged = True
        return {'sha': sha,
                'fileName': fileName,
                'oldLineNumber': oldLineNumber,
                'newLineNumber': newLineNumber,
                'isChanged': isChanged,
                'code': code}

def outputCommits():
    '''Creates an HTML timeline
    of all a file's revisions.
    '''
    c = Controller()
    c.render()

if __name__ == '__main__':
    outputCommits()






