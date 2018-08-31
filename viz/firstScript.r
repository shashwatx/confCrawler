library(stringr)

# specify data-file
datafile <- "data.all"

# read data
data <- read.table(datafile, header = T, sep = "|",quote="\"", comment.char="")

# show some info
str(data)

# correlation between numeric columns
cor(data[c(4, 5, 6, 7)])

# module to extract year from conference column
extractYear <- function(conference) {
  conference <- as.character(conference)
  ttx<-str_sub(conference,str_length(conference)-3,str_length(conference))
  tt<-as.integer(ttx)
  return(tt)
}

# module to extract conference from conference string
extractConference <- function(conferenceString) {
  #conferenceString <- as.character(conferenceString)
  ttx<-str_sub(conferenceString,str_length(conference)-8,str_length(conference))
  return(ttx)
}

extractAge <- function(conference) {
  year <- extractYear(conference)
  age <- 2017-year
  return(age)
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
  xlab("Year") +
  ylab("#Papers") +
  labs(fill = "large self citations")

ggplot(valid, aes(x = extractYear(conference),y=citations)) +
  geom_bar(stat="identity") +
  xlab("VLDB Year") +
  ylab("#Citations")
  
ggplot(valid, aes(x = extractYear(conference),y=self)) +
  geom_bar(stat="identity") +
  xlab("VLDB Year") +
  ylab("#SelfCitations")

#aggregate(data$citations, by=list(Category=x$conference), FUN=sum)
newdata<-data %>% 
          group_by(conference) %>% 
          summarise(totalCitations = sum(citations),
          totalSelfCitations=sum(self),
          numPapers=n(),
          fracSelf=sum(self)/sum(citations))

newdata <- transform(newdata, age=extractAge(conference))
#newdata <- transform(newdata, conference=extractConference(conference))

library(plotly)
p <- plot_ly(
  newdata, mode='markers', x = newdata$totalCitations, y = newdata$totalSelfCitations,
  color = newdata$age, size = newdata$numPapers, sizeref=2,
  text = ~paste("Conference: ", as.character(conference),"<br>",numPapers)
)


#valid <- transform(valid, citations=as.numeric(citations))
#cor(valid[c(4, 8)])

# find papers with NaN in selfCite
#curious <- data[is.nan(data$selfCite),]
#ggplot(curious, aes(x = extractYear(conference))) +
#  geom_bar() +
#  xlab("Year") +
#  ylab("#CuriousPapers")
