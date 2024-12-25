import pandas as pd

# Charger le fichier CSV
csv_file = '/home/onyxia/work/Scrapping_tweets/Scrapping_tweets/labeled_data_with_predictions.csv'  # Remplacez par le chemin de votre fichier CSV
df = pd.read_csv(csv_file)

# Sauvegarder le fichier en format Excel (XLSX)
xlsx_file = '/home/onyxia/work/Scrapping_tweets/Scrapping_tweets/data_predictions.xlsx'  # Nom du fichier Excel de sortie
df.to_excel(xlsx_file, index=False)  # index=False pour ne pas inclure l'index dans le fichier Excel


df = merged_df

# Vérifier que les colonnes nécessaires existent
if 'Content' not in df.columns or 'Views' not in df.columns:
    raise ValueError("Les colonnes 'Content' et 'Views' sont nécessaires pour ce traitement.")

# Compter les occurrences de chaque tweet
content_counts = df['Content'].value_counts()

# Filtrer les contenus apparaissant au moins 4 fois
repeated_contents = content_counts[content_counts >= 4].index

# Identifier les tweets répétitifs
repeated_tweets = df[df['Content'].isin(repeated_contents)]

# Identifier les groupes où un tweet a plus de 1000 vues
to_keep = repeated_tweets.groupby('Content')['Views'].max()  # Max des vues pour chaque groupe
valid_tweets = to_keep[to_keep > 1000].index  # Conserver les groupes avec au moins un tweet > 1000 vues

# Séparer les tweets répétitifs en deux groupes
# Tweets à conserver (au moins 1 tweet > 1000 vues dans le groupe)
tweets_to_keep = repeated_tweets[repeated_tweets['Content'].isin(valid_tweets)]

# Tweets à supprimer (aucun tweet > 1000 vues dans le groupe)
tweets_to_remove = repeated_tweets[~repeated_tweets['Content'].isin(valid_tweets)]

# Combiner les données finales
df_cleaned = pd.concat([df[~df['Content'].isin(repeated_contents)], tweets_to_keep])

# Sauvegarder les tweets répétitifs supprimés
tweets_to_remove.to_excel('removed_repeated_tweets.xlsx', index=False)

# Sauvegarder la base nettoyée
df_cleaned.to_excel('/home/onyxia/work/Scrapping_tweets/Scrapping_tweets/tweets_fusionnes.xlsx', index=False)
