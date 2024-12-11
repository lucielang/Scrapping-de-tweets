import pandas as pd
from datetime import datetime, timedelta

# Charger le fichier Excel contenant les dates
df = pd.read_excel('~/work/Scrapping_tweets/Scrapping_tweets/essai.xlsx')

#nettoyer la base de données en mettant des 0 si pas de vues, reposts, comments ou likes
colonnes_a_nettoyer = ['Comments', 'Repost', 'Likes', 'Views']

# Remplacer les valeurs vides (NaN) par 0 dans les colonnes spécifiées

def convertir_en_nombre(valeur):
    if pd.isna(valeur):  # Si la valeur est NaN, retourne 0
        return 0
    if isinstance(valeur, str):  # Vérifie si la valeur est une chaîne de caractères
        valeur = valeur.strip()  # Supprime les espaces inutiles
        if 'K' in valeur:  # Si la valeur contient 'K', multiplier par 1 000
            return float(valeur.replace('K', '')) * 1000
        elif 'M' in valeur:  # Si la valeur contient 'M', multiplier par 1 000 000
            return float(valeur.replace('M', '')) * 1000000
    try:
        return float(valeur)  # Sinon, convertir directement en nombre
    except ValueError:
        return 0  # Si la conversion échoue, retourner 0

# Appliquer la fonction à toutes les colonnes spécifiées
for colonne in colonnes_a_nettoyer:
    df[colonne] = df[colonne].apply(convertir_en_nombre)

# enlever les lignes avec plus de 1000 vues
df = df[df['Views'] <= 1000]


## convertir en dates 

# Fonction pour convertir les durées et les dates absolues
def convert_date(value, previous_date):
    try:
        value = str(value).strip()  # S'assurer que la valeur est une chaîne
        # Cas 1 : Format relatif (durées)
        if 'm' in value:  # Minutes
            minutes = int(value.replace('m', ''))
            return previous_date - timedelta(minutes=minutes)
        elif 'h' in value:  # Heures
            hours = int(value.replace('h', ''))
            return previous_date - timedelta(hours=hours)
        
        # Cas 2 : Format "Nov 5" (pas d'année explicite)
        elif len(value.split()) == 2:
            value_with_year = value + " 2024"  # Ajouter l'année par défaut
            return datetime.strptime(value_with_year, '%b %d %Y')
        
        # Cas 3 : Format complet "Nov 5, 2023"
        elif len(value.split()) == 3:
            return datetime.strptime(value, '%b %d, %Y')
        
        # Cas 4 : Valeur non reconnue
        else:
            return pd.NaT
    except Exception as e:
        print(f"Erreur lors de la conversion de la date : {value} -> {e}")
        return pd.NaT  # Retourne NaT si la conversion échoue

# Parcourir les lignes pour calculer les dates
converted_dates = []
previous_date = None

for value in df['Date']:
    if previous_date is None:  # La première ligne doit être une date absolue
        converted_date = convert_date(value, datetime(2024, 1, 1))  # Supposition du début
    else:
        converted_date = convert_date(value, previous_date)
    
    converted_dates.append(converted_date)
    if pd.notna(converted_date):  # Mettre à jour la référence seulement si la conversion a réussi
        previous_date = converted_date

# Ajouter les dates converties dans le DataFrame
df['ConvertedDate'] = converted_dates

# Filtrer pour ne conserver que les tweets à partir du 1er janvier 2024
start_date = datetime(2024, 1, 1)
df = df[df['ConvertedDate'] >= start_date]

# Ajouter une colonne pour l'année et la semaine
df['YearWeek'] = df['ConvertedDate'].dt.strftime('%Y-%U')

#Ajouter une colonne pour le mois
df['YearMonth'] = df['ConvertedDate'].dt.strftime('%Y-%m')

# Sauvegarder dans un fichier Excel
df.to_excel('~/work/Scrapping_tweets/Scrapping_tweets/dates_converties.xlsx', index=False)

