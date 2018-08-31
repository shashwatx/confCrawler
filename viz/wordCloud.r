
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")
library("Cairo")

#arguments <- commandArgs(trailingOnly=TRUE)

#for (i in 1:length(arguments)) {
#    print(paste("arg",as.character(i),"=",arguments[i]))
#}

#filePath <- arguments[1]
filePath <- "~/raw.txt"
text <- readLines(filePath)

docs <- Corpus(VectorSource(text))
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "/")
docs <- tm_map(docs, toSpace, "@")
docs <- tm_map(docs, toSpace, "\\|")
docs <- tm_map(docs, toSpace, "[^[:alnum:]]")

docs <- tm_map(docs, content_transformer(tolower))
docs <- tm_map(docs, removeNumbers)
docs <- tm_map(docs, removeWords, stopwords("english"))

#customStopWords<-tail(arguments,length(arguments)-1)
customStopWords<-c("the","databases","based","using","abstract","extended","en")

#docs <- tm_map(docs, stemDocument)

docs <- tm_map(docs, removeWords, customStopWords)

docs <- tm_map(docs, removePunctuation)

docs <- tm_map(docs, stripWhitespace)

writeLines(as.character(docs), con="mycorpus.txt")

dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)

head(d, 10)

#svg('sigmod.svg')
#par(bg="black",font=146)
#wordcloud(words = d$word, freq = d$freq, min.freq = 1,
#        max.words=100, random.order=FALSE, rot.per=0.35, 
#        colors=brewer.pal(8, "Dark2"), vfont=c("sans serif", "plain"))

#wordcloud(d$word,d$freq, scale=c(8,.3),min.freq=2,max.words=100, random.order=T, rot.per=.15, colors=pal, vfont=c("sans serif","plain"))

dev.off()
# 