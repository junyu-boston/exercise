from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, TimeDistributed, RepeatVector, GRU
import tensorflow.keras as keras
from tensorflow.keras.preprocessing.text import Tokenizer

en_len = 15
en_vocab = 150
hsize = 48

# Define an input layer
en_inputs = keras.layers.Input(shape=(en_len, en_vocab))
# Define a GRU layer which returns the state
en_gru = keras.layers.GRU(hsize, return_state=True)
# Get the output and state from the GRU
en_out, en_state = en_gru(en_inputs)
# Define and print the model summary
encoder = keras.models.Model(inputs=en_inputs, outputs=en_state)
print(encoder.summary())


fr_len = 20
# Define a RepeatVector layer
de_inputs = RepeatVector(fr_len)(en_state)

# Define a GRU model that returns all outputs
decoder_gru = GRU(hsize, return_sequences=True)
# Get the outputs of the decoder
gru_outputs = decoder_gru(de_inputs, initial_state=en_state)
# Define a model with the correct inputs and outputs
enc_dec = Model(inputs=en_inputs, outputs=gru_outputs)
enc_dec.summary()

en_st = ['the united states is sometimes chilly during december , but it is sometimes freezing in june .']
print('English: {}'.format(en_st))

# Convert the English sentence to a sequence
en_seq = sents2seqs('source', en_st, onehot=True, reverse=True)

# Predict probabilities of words using en_seq
fr_pred = model.predict(en_seq)

# Get the sequence indices (max argument) of fr_pred
fr_seq = np.argmax(fr_pred, axis=-1)[0]

# Convert the sequence of IDs to a sentence and print
fr_sent = [ fr_id2word[i] for i in fr_seq if i != 0]
print("French (Custom): {}".format(' '.join(fr_sent)))
print("French (Google Translate): les etats-unis sont parfois froids en décembre, mais parfois gelés en juin")


# Define a softmax dense layer that has fr_vocab outputs
de_dense = Dense(fr_vocab, activation="softmax")
# Wrap the dense layer in a TimeDistributed layer
de_dense_time = TimeDistributed(de_dense)
# Get the final prediction of the model
de_pred = de_dense_time(de_out)
print("Prediction shape: ", de_pred.shape)

nmt = Model(inputs=en_inputs, outputs=de_pred)

# Compile the model with an optimizer and a loss
nmt.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])

# View the summary of the model 
nmt.summary()

# Define a tokenizer with vocabulary size 50 and oov_token 'UNK'
en_tok = Tokenizer(num_words=50, oov_token='UNK')

# Fit the tokenizer on en_text
en_tok.fit_on_texts(en_text)

def sents2seqs(input_type, sentences, onehot=False, pad_type='post', reverse=False):     
    encoded_text = en_tok.texts_to_sequences(sentences)
    preproc_text = pad_sequences(encoded_text, padding=pad_type, truncating='post', maxlen=en_len)
    if reverse:
      # Reverse the text using numpy axis reversing
      preproc_text = preproc_text[:, ::-1]
    if onehot:
        preproc_text = to_categorical(preproc_text, num_classes=en_vocab)
    return preproc_text
  

n_epochs, bsize = 3, 250

for ei in range(n_epochs):
  for i in range(0,data_size,bsize):
    # Get a single batch of encoder inputs
    en_x = sents2seqs('source', en_text[i:i+bsize], onehot=True, reverse=True)
    # Get a single batch of decoder outputs
    de_y = sents2seqs('target', fr_text[i:i+bsize], onehot=True)
    
    # Train the model on a single batch of data
    nmt.train_on_batch(en_x, de_y)    
    # Obtain the eval metrics for the training data
    res = nmt.evaluate(en_x, de_y, batch_size=bsize, verbose=0)
    print("{} => Train Loss:{}, Train Acc: {}".format(ei+1,res[0], res[1]*100.0))  
    
train_size, valid_size = 800, 200
# Define a sequence of indices from 0 to len(en_text)
inds = np.arange(len(en_text))
np.random.shuffle(inds)
train_inds = inds[:train_size]
# Define valid_inds: last valid_size indices
valid_inds = inds[train_size:train_size+valid_size]
# Define tr_en (train EN sentences) and tr_fr (train FR sentences)
tr_en = [en_text[ti] for ti in train_inds]
tr_fr = [fr_text[ti] for ti in train_inds]
# Define v_en (valid EN sentences) and v_fr (valid FR sentences)
v_en = [en_text[vi] for vi in valid_inds]
v_fr = [fr_text[vi] for vi in valid_inds]
print('Training (EN):\n', tr_en[:3], '\nTraining (FR):\n', tr_fr[:3])
print('\nValid (EN):\n', v_en[:3], '\nValid (FR):\n', v_fr[:3])

# Convert validation data to onehot
v_en_x = sents2seqs('source', v_en, onehot=True, reverse=True)
v_de_y = sents2seqs('target', v_fr, onehot=True)

n_epochs, bsize = 3, 250
for ei in range(n_epochs):
  for i in range(0,train_size,bsize):
    # Get a single batch of inputs and outputs
    en_x = sents2seqs('source', tr_en[i:i+bsize], onehot=True, reverse=True)
    de_y = sents2seqs('target', tr_fr[i:i+bsize], onehot=True)
    # Train the model on a single batch of data
    nmt.train_on_batch(en_x, de_y)    
  # Evaluate the trained model on the validation data
  res = nmt.evaluate(v_en_x, v_de_y, batch_size=valid_size, verbose=0)
  print("{} => Loss:{}, Val Acc: {}".format(ei+1,res[0], res[1]*100.0))
  
 
