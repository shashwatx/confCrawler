# specify data-file
datafile <- "data.sigmod"

# read data
data <- read.table(datafile, header = T, sep = "|",quote="\"", comment.char="")

# show some info
str(data)

# correlation between numeric columns
cor(data[c(4, 5, 6, 7)])

# module to extract year from conference column
extractYear <- function(conference) {
  conference <- as.character(conference)
  tt<-as.integer(substr(conference, 7, 10))
  return(tt)
}

# extract first author
extractFirstAuthors <- function(authors) {
  str(authors)
  authorList <- strsplit(authors,",")
  firstAuthorList <- lapply(authorList, function(l) l[[1]])
  return(firstAuthorList)
}

# papers against time
library(ggplot2)
ggplot(data, aes(x = extractYear(conference))) +
  geom_bar() +
  xlab("Year") +
  ylab("#Papers")

data <- transform(data, selfCite = self/citations)
data <- transform(data, selfCiteFlag = selfCite>0.2)
data <- transform(data, authors=as.character(authors))
data$firstAuthor <- extractFirstAuthors(data$authors)

# plot fraction of papers with high proportion of self citations
# omit NaNs (papers with no citations)
valid <- data[!is.nan(data$selfCite),]
ggplot(valid, aes(x = extractYear(conference), fill=factor(selfCiteFlag))) +
  geom_bar() +
  xlab("VLDB Year") +
  ylab("#Papers") +
  labs(fill = "large self citations")

valid <- transform(valid, citations=as.numeric(citations))
cor(valid[c(4, 8)])

# find papers with NaN in selfCite
#curious <- data[is.nan(data$selfCite),]
#ggplot(curious, aes(x = extractYear(conference))) +
#  geom_bar() +
#  xlab("Year") +
#  ylab("#CuriousPapers")
