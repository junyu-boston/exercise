clean_corpus <- function(corpus){
  corpus <- tm_map(corpus, content_transformer(replace_abbreviation))
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, removeNumbers)
  corpus <- tm_map(corpus, removeWords, c(stopwords("en"), "coffee"))
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, stripWhitespace)
  return(corpus)
}

tm_define
# [1] "Text mining is the process of distilling actionable insights from text."                          
# [2] "Sentiment analysis represents the set of tools to extract an author's feelings towards a subject."

# Create a VectorSource
tm_vector <- VectorSource(tm_define)

# Apply VCorpus
tm_corpus <- VCorpus(tm_vector)

# Examine the first document's contents
content(tm_corpus[[1]])

# Clean the text
tm_clean <- clean_corpus(tm_corpus)

# Reexamine the contents of the first doc
content(tm_clean[[1]])

# clean_text is pre-defined
clean_text

# Create tf_dtm
tf_dtm <- DocumentTermMatrix(clean_text)

# Create tf_dtm_m
tf_dtm_m <- as.matrix(tf_dtm)

# Dimensions of DTM matrix
dim(tf_dtm_m)

# Subset part of tf_dtm_m for comparison
tf_dtm_m[16:20, 2975:2985]

