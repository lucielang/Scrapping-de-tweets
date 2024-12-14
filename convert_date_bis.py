import pandas as pd
from datetime import datetime, timedelta

# Fonction 1 : Nettoyer les données numériques
def convertir_en_nombre(valeur):
    """
    Convertit les chaînes de caractères (ex: '1.2K') en nombres.
    Remplace NaN par 0.
    """
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

# Fonction 2 : Conversion des dates
def convert_date(value, previous_date):
    """
    Convertit les valeurs de date relative ou absolue en objets datetime.
    """
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

# Fonction 3 : Nettoyer et transformer un fichier
def process_file(file_path):
    """
    Nettoie et transforme un fichier Excel, en ajoutant des colonnes converties
    et en générant deux fichiers de sortie :
    1. Toutes les données transformées.
    2. Données filtrées avant une date spécifique.
    """
    print(f"Traitement du fichier : {file_path}")
    # Charger les données
    df = pd.read_excel(file_path)
    
    # Nettoyer les colonnes numériques
    colonnes_a_nettoyer = ['Comments', 'Repost', 'Likes', 'Views']
    for colonne in colonnes_a_nettoyer:
        if colonne in df.columns:
            df[colonne] = df[colonne].apply(convertir_en_nombre)
    
    # Convertir les dates
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
    
    # Ajouter les colonnes converties
    df['ConvertedDate'] = converted_dates
    df['YearWeek'] = df['ConvertedDate'].dt.strftime('%Y-%U')
    df['YearMonth'] = df['ConvertedDate'].dt.strftime('%Y-%m')
    

    # Filtrer les données pour garder uniquement les dates avant le 1er décembre 2024
    cutoff_date = datetime(2024, 12, 1)
    df_filtered = df[df['ConvertedDate'] < cutoff_date]
    
    # Sauvegarder les données filtrées
    output_file_filtered = file_path.replace('.xlsx', '_nettoye.xlsx')
    df_filtered.to_excel(output_file_filtered, index=False)
    print(f"Fichier avec les données filtrées sauvegardé : {output_file_filtered}")

# Liste des fichiers Excel à traiter
files = ['tweets_group_leave.xlsx', 'tweets_group_stay.xlsx']

# Boucle principale pour traiter chaque fichier
for file in files:
    process_file(file)
