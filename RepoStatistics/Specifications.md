# Repo Statistics

## Introduction

This software aims to produce a report of statistics and data visualizations derived from a given local git repository. It presents a command-line front-end to the user--implemented in python--and outputs a PDF file of graphics.

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

## Output

The program should output a single (multi-page, if necessary) PDF file containing statistical graphics.