# TODO: use ddply to summarize the data so I can plot raw counts

library(ggplot2)
library(plyr)
library(lubridate)

csv.file = "~/Dropbox/dev/granovaGG/repo_statistics.csv"

repo.statistics <- read.csv(csv.file, stringsAsFactors=FALSE)

formatDatesAndTimes <- function(repo.statistics) {
  repo.statistics$date <- ymd(repo.statistics$date)
  repo.statistics$time <- hms(repo.statistics$time)
  repo.statistics$datetime <- ymd_hms(repo.statistics$datetime)
  return(repo.statistics)
}

formatAdditionsAndDeletions <- function()

repo.statistics <- formatDatesAndTimes(repo.statistics)
str(repo.statistics)