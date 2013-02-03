# TODO: use ddply to summarize the data so I can plot raw counts
# Export several CSVs from the additions/deletions data, then merge()

library(ggplot2)
library(plyr)
library(lubridate)
commits <- read.csv("~/Dropbox/2013Spring/PracticePub/RebeccasProject2Commits.csv",
                    stringsAsFactors=FALSE)
convertToDates <- function (x) {
  return(ymd_hms(x))
}

commits$commit <- convertToDates(commits$commit)
str(commits)
p <- ggplot(aes(x = commit), data=commits)
p + geom_line() + geom_density(aes(y = ..scaled..))