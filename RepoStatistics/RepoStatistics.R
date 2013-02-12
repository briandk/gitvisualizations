# TODO: use ddply to summarize the data so I can plot raw counts

# Base R dependencies
library(RColorBrewer)

# User-installed dependencies
library(ggplot2)
library(plyr)
library(lubridate)

# Set the working directory
working.directory <- commandArgs(trailingOnly = TRUE)
setwd(working.directory)
csv.file <- "repo_statistics.csv"
pdf.file <- "repo_statistics.pdf"

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
                  commits.per.day = length(sha)
            )
  return(output)
}

getCumulativeCommitsOverTime <- function(repo.statistics) {
  output <- ddply(repo.statistics,
                  .(sha, datetime),
                  summarize,
                  number.of.commits = length(unique(sha)))
  output <- arrange(output, datetime)
  output <- transform(output, cumulative.commits = cumsum(number.of.commits))
  return(output)
}

plotCommitsPerDay <- function(repo.statistics) {
  p <- ggplot(
            aes(x = date,
                y = commits.per.day),
            data = getCommitsPerDay(repo.statistics))
  p <- p + geom_area(
             fill = brewer.pal(n=8, name="Set1")[2],
             alpha = 0.5)
  p <- p + cumulativeCommitsOverTime(repo.statistics)
  p <- p + geom_point()
  p <- p + ylab("commits")
  p <- p + ggtitle("Commit Activity over Time")
  return(p)
}

cumulativeCommitsOverTime <- function(repo.statistics) {
  return(
    geom_line(
      aes(y = cumulative.commits,
          x = datetime),
      color = brewer.pal(n=8, name="Set1")[1],
      alpha = 0.75,
      data = getCumulativeCommitsOverTime(repo.statistics)
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

SmallMultiplesOfAdditionsAndDeletions <- function(repo.statistics) {
  p <- ggplot(data = getLinesAddedAndLinesDeletedByDay(repo.statistics))
  p <- p + linesAddedByDay()
  p <- p + linesDeletedByDay()
  p <- p + theme(axis.text.x = element_text(angle = 90))
  p <- p + ggtitle("Summary of Lines Added/Deleted Per Day")
  p <- p + xlab("Date")
  p <- p + ylab("Lines Added/Deleted")
  p <- p + facet_wrap(~ filename)
  return(p)
}

linesAddedByDay <- function() {
  return(
    geom_bar(
      aes(x = date,
          y = lines_added
      ),
      stat = "identity",
      fill = brewer.pal(n=5, name="Dark2")[1],
      alpha = 1.0
    )
  )
}

linesDeletedByDay <- function() {
  return(
    geom_bar(
      aes(x = date,
          y = lines_deleted
      ),
      stat = "identity",
      fill = brewer.pal(n=5, name="Dark2")[2],
      alpha = 1.0
    )
  )
}

getFilesThatWereChangedMoreThanOnce <- function(repo.statistics) {
  files <- daply(repo.statistics,
                 .(filename),
                 summarize,
                 length(sha))
  files.changed.more.than.once <- names(files)[files > 4]
  return(files.changed.more.than.once)
}

IndividialLinesAddedAndDeletedByDay <- function(repo.statistics) {
  for(unique.name in getFilesThatWereChangedMoreThanOnce(repo.statistics)) {
    additions.deletions.data <- getLinesAddedAndLinesDeletedByDay(repo.statistics)
    per.file.data <- subset(additions.deletions.data, filename == unique.name)
    p <- ggplot(aes(x = date, y = lines_added), data = per.file.data)
    p <- p + geom_line()
    p <- p + ggtitle(unique.name)
    # p <- p + linesDeletedByDay()
    print(per.file.data)
    print(p)
  }
}

makePDF <- function(output.file) {
  pdf(file = output.file, 
      width = 1.3*11.5,
      height = 1.3*8,
      onefile = TRUE)
  repo.statistics <- formatDatesAndTimes(repo.statistics)
  repo.statistics <- formatAdditionsAndDeletions(repo.statistics)
  p <- plotCommitsPerDay(repo.statistics)
  print(p)
  p <-SmallMultiplesOfAdditionsAndDeletions(repo.statistics)
  print(p)
  dev.off()
}

makePDF(pdf.file)



