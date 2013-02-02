# TODO: use ddply to summarize the data so I can plot raw counts

library(ggplot2)
library(plyr)
library(lubridate)

csv.file = "~/Dropbox/dev/granovaGG/repo_statistics.csv"

repo.statistics <- read.csv(csv.file, stringsAsFactors=FALSE)

formatDatesAndTimes <- function(repo.statistics) {
  output <- within(repo.statistics, {
    date <- ymd(date)
    time <- hms(time)
    datetime <- ymd_hms(datetime)
  })
  return(output)
}

# formatAdditionsAndDeletions <- function()

repo.statistics <- formatDatesAndTimes(repo.statistics)
str(repo.statistics)