import pandas as pd
import spacy
from collections import Counter
import nltk
from nltk.probability import FreqDist
import plotly.express as px

# Charger les données
df = pd.read_csv('labeled_data_with_predictions.csv')

# Charger le modèle SpaCy
nlp = spacy.load("en_core_web_sm")

# Stopwords personnalisés (ajouter ici les mots que vous voulez exclure)
custom_stopwords = {"https", "twitter", "elon", "musk", "people","quit","leave","stay", "like", "amp", "com", "user", "retweet", "x"}

def clean_and_tokenize_spacy(text):
    """
    Utiliser SpaCy pour tokeniser et nettoyer le texte.
    """
    if not isinstance(text, str):
        return []
    doc = nlp(text.lower())
    tokens = [
        token.lemma_  # Récupérer le lemme (forme de base du mot)
        for token in doc
        if not token.is_stop  # Exclure les stopwords de SpaCy
        and token.is_alpha  # Exclure les caractères non alphabétiques
        and token.lemma_ not in custom_stopwords  # Exclure les mots personnalisés
    ]
    return tokens

# Appliquer le nettoyage et la tokenisation avec SpaCy
df['tokens'] = df['cleaned_tweet'].apply(clean_and_tokenize_spacy)

liste = []
for ligne in df['tokens']:
    liste = liste + ligne

fdist = FreqDist(liste)
fd = pd.DataFrame(fdist.most_common(10), columns = ["Word","Frequency"]).drop([0]).reindex()
fig = px.bar(fd, x="Word", y="Frequency")
fig.update_traces(marker_color='rgb(240,128,128)',marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.8)
fig.show()