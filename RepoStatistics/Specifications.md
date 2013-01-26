# Repo Statistics

## Introduction

This software aims to produce a report of statistics and data visualizations derived from a given local git repository. It presents a command-line front-end to the user and outputs a PDF file of graphics.

This document outlines the specifications for how different parts of this system relate to one another. 

## Input

There are three input parameters the interface should take:

- Path to the repository **(required)**
- a "Since" date, which defines the beginning of the time interval of interest *(optional)*
- an "Until" date, which defines the end of the time interval of interest *(optional)*

### Sample input

```bash
$ python RepoStatistics.py path/to/repo
$ python RepoStatistics.py path/to/repo --since=yesterday
$ python RepoStatistics.py path/to/repo --until="3-14-2012"
$ python RepoStatistics.py path/to/repo --since="last year" --until="last month"
```

## Intermediate Data

### Git Log File

The git log file is generated using the following command:

```bash
$ git log --numstat --date=iso --format=' %H,%ad' 
```

The output format that contains the following information for each commit:

- A datestamp line
- One or more diffstat lines

#### The datestamp line

##### Format

```text
 %40c,%4d-%2d-%2d %2d:%2d:%2d +/-%4d
```

- A leading space to denote the datestamp line
- The full 40-character SHA of the commit
- A comma
- The ISO-formatted datestamp

##### Example

```
 57f4d2d332470aea3c672c4ae5ca98f238b3b7c0,2012-12-04 01:40:27 -0500
```


#### The diffstat line

##### Format

```text
%d\t%d\t%s
```

- An integer representing the number of lines added to a file
- A tab (whitespace)
- An integer representing the number of lines deleted from a file
- A tab (whitespace)
- A path (relative to the root of the repo) identifying the file

#### Sample git log output

```
 f8e003f22d39236540e18eb8560266f4e5a32718,2013-01-21 15:14:29 -0500

8       0       tests/LogLineParser.py
48      0       tests/loglines.txt
 7cc1c1ebe80f5b15fe1b59e6560b64fe6eacc3fe,2013-01-19 22:30:12 -0500

134     0       CodeTimeline/CodeTimeline.py
0       139     CodeTimeline/FileTimeline.py
 72f07c5dc66cf95f024f8a5a0c2b6c17a947dcde,2013-01-19 22:24:50 -0500

5       0       CodeTimeline/FileTimeline.py
```

### The Loglet Class

As the log output is parsed, it's aggregated into what I've been calling a "loglet." Loglets are a conceptual way I'm using to organize how I chunk the information of the git log output. Roughly speaking, a loglet is a Python object with the following data attributes:

- SHA-1 hash (ex: 6e8c4c26c3046f7df7644ad00231f38e5baef365)
- Date (ex: 2013-01-25)
- 24-hour Time (ex: 01:02:47)
- DateTime (ex: 2013-01-25 01:02:47)
- GMT Offset (ex: -0500)
- A list of one or more diffstat objects

### The Diffstat data spec

Each diffstat contains:

- An integer representing the lines added
- An integer representing the lines deleted
- A string representing filename by the relative path (relative to the repo root) to the file

### CSV File ###

The CSV file is designed to be processed as input to the R Script. It's intentionally "long" data, which means essentially that any given commit will be represented by multiple observations, one observation per file in the commit.

Each observation will contain values for the following variables:

- SHA hash
- Date
- Time
- DateTime
- File Path
- Lines Added
- Lines Deleted

#### Example CSV Line ####

| sha	 	                             | date	    | time	 | dateTime	         | filePath  | linesAdded | linesDeleted
|----------------------------------------|----------|--------|-------------------|-----------|------------|-------------
d80ed5b2eceea5f3bd066153f32da63a98a878f2 |2012-11-30|01:40:46|2012-11-30 01:40:46|Timeline.js|6           |0

## Output

The program should output a single (multi-page, if necessary) PDF file containing statistical graphics.