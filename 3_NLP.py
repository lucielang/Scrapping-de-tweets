import pandas as pd
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, GRU, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from keras.regularizers import l2
import numpy as np
import matplotlib.pyplot as plt
import pickle

# Charger et nettoyer les données
tweet = pd.read_csv('/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/training_data/train.csv')

# Combiner les colonnes de toxicité pour une classification binaire
df_fixed = tweet
df_fixed['class'] = df_fixed[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']].sum(axis=1)
df_fixed['class'] = df_fixed['class'].apply(lambda x: 1 if x > 0 else 0)

# Fonction de nettoyage des tweets
def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@\w+|\#','', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    tweet = tweet.strip()
    return tweet

df_fixed['cleaned_tweet'] = df_fixed['comment_text'].apply(clean_tweet)

# Mélanger les données
df_fixed = df_fixed.sample(frac=1, random_state=42).reset_index(drop=True)

# Chargement des embeddings GloVe
embedding_index = {}
with open('/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/glove.6B/glove.6B.100d.txt', encoding='utf-8') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embedding_index[word] = coefs

# Préparer la tokenisation et le padding
max_words = 10000
max_len = 150

tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(df_fixed['cleaned_tweet'])
sequences = tokenizer.texts_to_sequences(df_fixed['cleaned_tweet'])
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Préparer les embeddings
word_index = tokenizer.word_index
embedding_dim = 100

embedding_matrix = np.zeros((max_words, embedding_dim))
for word, i in word_index.items():
    if i < max_words:
        embedding_vector = embedding_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

# Diviser les données
X_train, X_val, y_train, y_val = train_test_split(
    padded_sequences, 
    df_fixed['class'], 
    test_size=0.25, 
    random_state=42
)

# Construire le modèle
model = Sequential([
    Embedding(input_dim=max_words, output_dim=embedding_dim, weights=[embedding_matrix], input_length=max_len, trainable=False),
    Bidirectional(GRU(64, return_sequences=True, kernel_regularizer=l2(0.01))),
    Dropout(0.3),
    Bidirectional(GRU(32, return_sequences=False, kernel_regularizer=l2(0.01))),
    Dropout(0.4),
    Dense(64, activation='relu', kernel_regularizer=l2(0.01)),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Callbacks pour éviter l'overfitting
early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-5)

# Entraîner le modèle
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=64,
    validation_data=(X_val, y_val),
    callbacks=[early_stop, reduce_lr],
    verbose=1
)


# Sauvegarder le tokenizer
with open('/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/model/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("Tokenizer sauvegardé avec succès !")

# Visualisation des métriques
plt.plot(history.history['accuracy'], label='Précision entraînement')
plt.plot(history.history['val_accuracy'], label='Précision validation')
plt.xlabel('Époque')
plt.ylabel('Précision')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='Perte entraînement')
plt.plot(history.history['val_loss'], label='Perte validation')
plt.xlabel('Époque')
plt.ylabel('Perte')
plt.legend()
plt.show()

# Sauvegarder le modèle
model.save('/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/model/saved_model_optimized_2.h5')
print("Modèle optimisé sauvegardé avec succès !")