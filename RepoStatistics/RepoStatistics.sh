#! /usr/bin/bash
# Takes a single argument: the path to a repository

cd ${1}
TEMPLOG=$(mktemp /tmp/output.XXXXXXXXXX)
TMPCSV=$(mktemp /tmp/output.XXXXXXXXXX)
git log --numstat --date=iso --format=' %H,%ad' > $TEMPLOG

# To generate repo statistics
#   X change to the directory of interest
#   X make temporary log output file
#   X make temporary CSV output file
#   X git log > temporary file
#   python templog > tempcsv
#   R csv

