import pandas as pd

# Charger le fichier CSV
csv_file = '/home/onyxia/work/Scrapping_tweets/Scrapping_tweets/labeled_data_with_predictions.csv'  # Remplacez par le chemin de votre fichier CSV
df = pd.read_csv(csv_file)

# Sauvegarder le fichier en format Excel (XLSX)
xlsx_file = '/home/onyxia/work/Scrapping_tweets/Scrapping_tweets/data_predictions.xlsx'  # Nom du fichier Excel de sortie
df.to_excel(xlsx_file, index=False)  # index=False pour ne pas inclure l'index dans le fichier Excel
