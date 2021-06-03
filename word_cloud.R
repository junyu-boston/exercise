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
