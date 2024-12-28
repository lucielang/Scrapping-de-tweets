import re
import pandas as pd
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# **Étape 1 : Charger le tokenizer**
tokenizer_path = '/home/onyxia/Scrapping_tweets-1/training_data/tokenizer.pickle'
model_path = '/home/onyxia/Scrapping_tweets-1/training_data/saved_model_optimized_3.h5'

# Charger le tokenizer sauvegardé
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

# **Étape 2 : Charger le modèle**
model = load_model(model_path)

# **Étape 3 : Définir les fonctions utilitaires**
def clean_tweet(tweet):
    """
    Fonction pour nettoyer les tweets : supprimer URLs, mentions, hashtags, ponctuations, etc.
    """
    tweet = str(tweet)  # Convertir en chaîne de caractères si nécessaire
    tweet = re.sub(r'\d+', '', tweet)  # Supprimer les nombres
    tweet = tweet.lower()
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)  # Supprimer les URLs
    tweet = re.sub(r'\@\w+|\#', '', tweet)  # Supprimer les mentions et hashtags
    tweet = re.sub(r'[^\w\s]', '', tweet)  # Supprimer la ponctuation
    tweet = tweet.strip()
    return tweet

# **Étape 4 : Charger et nettoyer la base de données**
input_file = ''
df = pd.read_csv(input_file)

# Appliquer le nettoyage sur les tweets
df['cleaned_tweet'] = df['Content'].apply(clean_tweet)

# **Étape 5 : Convertir les tweets en séquences et appliquer le padding**
max_len = 300  # Utilisez la même longueur que pendant l'entraînement !

# Convertir les tweets nettoyés en séquences numériques
sequences = tokenizer.texts_to_sequences(df['cleaned_tweet'])

# Appliquer le padding sur les séquences
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# **Étape 6 : Prédire la violence avec le modèle**
predictions = model.predict(padded_sequences, batch_size=64)  # Batch size pour accélérer les prédictions

# Convertir les probabilités en classes binaires (0 = non violent, 1 = violent)
df['violence_prédite'] = (predictions >= 0.5).astype(int)

# **Étape 7 : Sauvegarder les résultats**
output_file = ''
df.to_csv(output_file, index=False)

print("Prédictions ajoutées et fichier sauvegardé à l'emplacement :", output_file)
