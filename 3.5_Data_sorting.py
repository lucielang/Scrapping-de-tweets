import re
import pandas as pd 
from keras.regularizers import l2
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, GRU, Dense, Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Chargement des données
input_file = '/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/data_set/tweets_fusionnes.csv'
df = pd.read_csv(input_file)

# Nettoyer les tweets (fonction déjà définie dans ton code)
def clean_tweet(tweet):
    tweet = str(tweet)
    tweet = re.sub(r'\d+', '', tweet)  # Supprimer les nombres
    tweet = tweet.lower()
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)  # Supprimer les URLs
    tweet = re.sub(r'\@\w+|\#', '', tweet)  # Supprimer les mentions et hashtags
    tweet = re.sub(r'[^\w\s]', '', tweet)  # Supprimer la ponctuation
    tweet = tweet.strip()
    return tweet

# Appliquer la fonction de nettoyage
df['cleaned_tweet'] = df['Content'].apply(clean_tweet)

# Charger le modèle
model = load_model('/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/model/saved_model.h5')

# Définir les paramètres de Tokenizer
max_words = 5000  # Le nombre maximum de mots à garder
max_len = 20  # Longueur maximale des séquences (nombre de mots par tweet)

# Initialiser le Tokenizer et l'entraîner sur les tweets nettoyés
tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(df['cleaned_tweet'])  # Entraîner le tokenizer sur les tweets

# Préparer les tweets pour la prédiction
sequences = tokenizer.texts_to_sequences(df['cleaned_tweet'])  # Convertir les tweets en séquences
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')  # Padding des séquences

# Prédire la violence
predictions = model.predict(padded_sequences)

# Convertir les probabilités en classes binaires
df['violence_prédite'] = (predictions >= 0.5).astype(int)  # 1 pour violent, 0 pour non violent

# Sauvegarder le tableau mis à jour
df.to_csv('/Users/thibaultkarpel/Desktop/python_ensae/Python_for_data_science/data_set/labeled_data_with_predictions.csv', index=False)
print("Colonne 'violence_prédite' ajoutée et tableau sauvegardé.")