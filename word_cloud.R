# Load wordcloud package
library(wordcloud)

# Add to stopwords
stops <- c(stopwords(kind = 'en'), 'chardonnay')

# Apply to a corpus
cleaned_chardonnay_corp <- tm_map(chardonnay_corp, removeWords, stops)

# Get a terms vector
terms_vec <- names(chardonnay_words)

# Create a wordcloud for the values in word_freqs
wordcloud(terms_vec, chardonnay_words, 
          max.words = 50, colors = "red")
          
# Print the list of colors
colors()

library(viridisLite)
# Select 5 colors 
color_pal <- cividis(n=5)

# Examine the palette output
color_pal

# Create a word cloud with the selected palette
wordcloud(chardonnay_freqs$term, chardonnay_freqs$num, max.words=100, color=color_pal)

### commonality and comparison word cloud 
# Create all_coffee
all_coffee <- paste(coffee_tweets$text, collapse= " ")

# Create all_chardonnay
all_chardonnay <- paste(chardonnay_tweets$text, collapse=" ")

# Create all_tweets
all_tweets <- c(all_coffee, all_chardonnay)

# Convert to a vector source
all_tweets <- VectorSource(all_tweets)

# Create all_corpus
all_corpus <- VCorpus(all_tweets)

# Clean the corpus
all_clean <- clean_corpus(all_corpus)

# Create all_tdm
all_tdm <- TermDocumentMatrix(all_clean)

# Create all_m
all_m <- as.matrix(all_tdm)

# Print a commonality cloud
commonality.cloud(all_m, max.words=100, colors="steelblue1")

# Clean the corpus
all_clean <- clean_corpus(all_corpus)
# Create all_tdm
all_tdm <- TermDocumentMatrix(all_clean)

# Give the columns distinct names
colnames(all_tdm) <- c("coffee", "chardonnay")

# Create all_m
all_m <- as.matrix(all_tdm)

# Create comparison cloud
comparison.cloud(all_m, colors = c("orange", "blue"), max.words = 50)

#### pyrimad plot
top25_df <- all_tdm_m %>%
  # Convert to data frame
  as_data_frame(rownames = "word") %>% 
  # Keep rows where word appears everywhere
  filter_all(all_vars(. > 0)) %>% 
  # Get difference in counts
  mutate(difference = chardonnay - coffee) %>% 
  # Keep rows with biggest difference
  top_n(25, wt = difference) %>% 
  # Arrange by descending difference
  arrange(desc(difference))

#### Word assoication / network plot
# Word association
word_associate(coffee_tweets$text, match.string = "barista", 
               stopwords = c(Top200Words, "coffee", "amp"), 
               network.plot = TRUE, cloud.colors = c("gray85", "darkred"))

# Add title
title(main = "Barista Coffee Tweet Associations")

