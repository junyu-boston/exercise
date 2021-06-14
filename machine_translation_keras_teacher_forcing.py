# Import the layers submodule from keras
import tensorflow.keras.layers as layers

en_inputs = layers.Input(shape=(en_len, en_vocab))
en_gru = layers.GRU(hsize, return_state=True)
# Get the encoder output and state
en_out, en_state = en_gru(en_inputs)

# Define the decoder input layer
de_inputs = layers.Input(shape=(fr_len-1, fr_vocab))
de_gru = layers.GRU(hsize, return_sequences=True)
de_out = de_gru(de_inputs, initial_state=en_state)
# Define a TimeDistributed Dense softmax layer with fr_vocab nodes
de_dense = layers.TimeDistributed(layers.Dense(fr_vocab, activation='softmax'))
de_pred = de_dense(de_out)

# Import the Keras Model object
from tensorflow.keras.models import Model

# Define a model
nmt_tf = Model(inputs=[en_inputs, de_inputs], outputs=de_pred)
# Compile the model with optimizer and loss
nmt_tf.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["acc"])
# Print the summary of the model
nmt_tf.summary()


n_epochs, bsize = 3, 250


train_size, valid_size = 800, 200
# Define a sequence of indices from 0 to size of en_text
inds = np.arange(len(en_text))
np.random.shuffle(inds)
# Define train_inds as first train_size indices
train_inds = inds[:train_size]
valid_inds = inds[train_size:train_size+valid_size]
# Define tr_en (train EN sentences) and tr_fr (train FR sentences)
tr_en = [en_text[ti] for ti in train_inds]
tr_fr = [fr_text[ti] for ti in train_inds]
# Define v_en (valid EN sentences) and v_fr (valid FR sentences)
v_en = [en_text[vi] for vi in valid_inds]
v_fr = [fr_text[vi] for vi in valid_inds]
print('Training (EN):\n', tr_en[:3], '\nTraining (FR):\n', tr_fr[:3])
print('\nValid (EN):\n', v_en[:3], '\nValid (FR):\n', v_fr[:3])

for ei in range(n_epochs):
  for i in range(0,train_size,bsize):    
    en_x = sents2seqs('source', tr_en[i:i+bsize], onehot=True, reverse=True)
    de_xy = sents2seqs('target', tr_fr[i:i+bsize], onehot=True)
    # Create a single batch of decoder inputs and outputs
    de_x, de_y = de_xy[:,:-1,:], de_xy[:,1:,:]
    # Train the model on a single batch of data
    nmt_tf.train_on_batch([en_x, de_x], de_y)      
  v_en_x = sents2seqs('source', v_en, onehot=True, reverse=True)
  # Create a single batch of validation decoder inputs and outputs
  v_de_xy = sents2seqs('target', v_fr, onehot=True)
  v_de_x, v_de_y = v_de_xy[:, :-1, :], v_de_xy[:, 1:, :]
  # Evaluate the trained model on the validation data
  res = nmt_tf.evaluate([v_en_x, v_de_x], v_de_y, batch_size=valid_size, verbose=0)
  print("{} => Loss:{}, Val Acc: {}".format(ei+1,res[0], res[1]*100.0))
  
  
### translation

# Define an input layer that accepts a single onehot encoded word
de_inputs = layers.Input(shape=(1, fr_vocab))
# Define an input to accept the t-1 state
de_state_in = layers.Input(shape=(hsize,))
de_gru = layers.GRU(hsize, return_state=True)
# Get the output and state from the GRU layer
de_out, de_state_out = de_gru(de_inputs, initial_state=de_state_in)
de_dense = layers.Dense(fr_vocab, activation='softmax')
de_pred = de_dense(de_out)

# Define a model
decoder = Model(inputs=[de_inputs, de_state_in], outputs=[de_pred, de_state_out])
print(decoder.summary())

# Load the weights to the encoder GRU from the trained model
en_gru_w = tr_en_gru.get_weights()
# Set the weights of the encoder GRU of the inference model
en_gru.set_weights(en_gru_w)
# Load and set the weights to the decoder GRU
de_gru.set_weights(tr_de_gru.get_weights())
# Load and set the weights to the decoder Dense
de_dense.set_weights(tr_de_dense.get_weights())

en_sent = ['the united states is sometimes chilly during december , but it is sometimes freezing in june .']
print('English: {}'.format(en_sent))
en_seq = sents2seqs('source', en_sent, onehot=True, reverse=True)
# Predict the initial decoder state with the encoder
de_s_t = encoder.predict(en_seq)
de_seq = word2onehot(fr_tok, 'sos', fr_vocab)
fr_sent = ''
for i in range(fr_len):    
  # Predict from the decoder and recursively assign the new state to de_s_t
  de_prob, de_s_t = decoder.predict([de_seq,de_s_t])
  # Get the word from the probability output using probs2word
  de_w = probs2word(de_prob, fr_tok)
  # Convert the word to a onehot sequence using word2onehot
  de_seq = word2onehot(fr_tok, de_w, fr_vocab)
  if de_w == 'eos': break
  fr_sent += de_w + ' '
print("French (Ours): {}".format(fr_sent))
print("French (Google Translate): les etats-unis sont parfois froids en décembre, mais parfois gelés en juin")



