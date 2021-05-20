def get_next_char(model, initial_text, chars_window, char_to_index, index_to_char):
  	# Initialize the X vector with zeros
    X = initialize_X(initial_text, chars_window, char_to_index)
    
    # Get next character using the model
    next_char = predict_next_char(model, X, index_to_char)
	
    return next_char

# Define context sentence and print the generated text
initial_text = "I am not insane, "
print("Next character: {0}".format(get_next_char(model, initial_text, 20, char_to_index, index_to_char)))


# Instantiate the vectors
sentences = []
next_chars = []
# Loop for every sentence
for sentence in sheldon.split('\n'):
    # Get 20 previous chars and next char; then shift by step
    for i in range(0, len(sentence) - chars_window, step):
        sentences.append(sentence[i:i + chars_window])
        next_chars.append(sentence[i + chars_window])

# Define a Data Frame with the vectors
df = pd.DataFrame({'sentence': sentences, 'next_char': next_chars})

# Print the initial rows
print(df.head())

# Instantiate the variables with zeros
numerical_sentences = np.zeros((num_seqs, chars_window, n_vocab), dtype=np.bool)
numerical_next_chars = np.zeros((num_seqs, n_vocab), dtype=np.bool)

# Loop for every sentence
for i, sentence in enumerate(sentences):
  # Loop for every character in sentence
  for t, char in enumerate(sentence):
    # Set position of the character to 1
    numerical_sentences[i, t, char_to_index[char]] = 1
    # Set next character to 1
    numerical_next_chars[i, char_to_index[next_chars[i]]] = 1

# Print the first position of each
print(numerical_sentences[0], numerical_next_chars[0], sep="\n")


