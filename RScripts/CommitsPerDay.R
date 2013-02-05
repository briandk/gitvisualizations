# TODO: use ddply to summarize the data so I can plot raw counts

library(ggplot2)
library(plyr)
library(lubridate)

csv.file = "~/Desktop/test-student-repo/repo_statistics.csv"

repo.statistics <- read.csv(csv.file, stringsAsFactors=FALSE)

formatDatesAndTimes <- function(repo.statistics) {
  output <- within(repo.statistics, {
    date <- ymd(date)
    datetime <- ymd_hms(datetime)
  })
  return(output)
}

formatAdditionsAndDeletions <- function(repo.statistics) {
  output <- within(repo.statistics, {
    lines_added <- as.numeric(lines_added)
    lines_deleted <- as.numeric(lines_deleted)
  })
  return(removeNAs(output))
}

removeNAs <- function(repo.statistics) {
  return(repo.statistics[complete.cases(repo.statistics), ])
}

getCommitsPerDay <- function(repo.statistics) {
  output <- ddply(repo.statistics,
                  .(date),
                  summarize,
                  commits.per.day = length(lines_added)
            )
  output <- transform(output,
                      cumulative.commits = cumsum(commits.per.day)
            )
  return(output)
}

plotCommitsPerDay <- function(repo.statistics) {
  p <- ggplot(
            aes(x = date,
                y = commits.per.day),
            data = getCommitsPerDay(repo.statistics))
  p <- p + geom_line()
  p <- p + ylab("commits")
  p <- p + ggtitle("Commit Activity over Time")
  p <- p + cumulativeCommitsPerDay()
  return(p)
}

cumulativeCommitsPerDay <- function() {
  return(
    geom_line(
      aes(y = cumulative.commits,
          x = date)
    )
  )
}

getLinesAddedAndLinesDeletedByDay <- function(repo.statistics) {
  output <- ddply(repo.statistics,
                  .(date, filename),
                  summarize,
                  lines_added = sum(lines_added),
                  lines_deleted = sum(-lines_deleted)
            )
  return(output)
}

SummaryOfLinesAddedAndLinesDeletedByDay <- function(repo.statistics) {
  p <- ggplot(data = getLinesAddedAndLinesDeletedByDay(repo.statistics))
  p <- p + linesAddedByDay()
  p <- p + linesDeletedByDay()
  p <- p + theme(axis.text.x = element_text(angle = 90))
  p <- p + ggtitle("Summary of Lines Added/Deleted Over Time")
  p <- p + xlab("Date")
  p <- p + ylab("Lines Added/Deleted")
  p <- p + facet_wrap(~ filename)
  return(p)
}

linesAddedByDay <- function() {
  return(
    geom_area(
      aes(x = date,
          y = lines_added
      ),
      fill = "darkblue",
      alpha = 0.5
    )
  )
}

linesDeletedByDay <- function() {
  return(
    geom_area(
      aes(x = date,
          y = lines_deleted
      ),
      fill = "orange",
      alpha = 0.5
    )
  )
}

repo.statistics <- formatDatesAndTimes(repo.statistics)
repo.statistics <- formatAdditionsAndDeletions(repo.statistics)
p <- plotCommitsPerDay(repo.statistics)
print(p)
p <- SummaryOfLinesAddedAndLinesDeletedByDay(repo.statistics)
print(p)
