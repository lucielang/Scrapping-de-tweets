# Etude de l'utilisation de Twitter par ses utilisateurs en 2024 :bird:

Bienvenue sur le Github présentant notre projet Python dans le cadre du cours Python pour la data science. 

L'objectif était, en récoltant par scraping les tweets contenant les mots clefs *Musk*, *Twitter* et des mots synonymes de *quit*, *leave* ou *stay*, d'obtenir une base de tweets avec les utilisateurs qui s'étaient exprimés sur la question de quitter ou non Twitter. Nous avons ainsi pu observer les tendances exprimées en 2024, puis fait de l'analyse textuelle en regardant les mots qui revenaient le plus souvent dans les tweets.
En passant par du NLP, nous avons classifié les tweets en 2 catégories et étudier corrélation entre positif nbr de likes toussa COMPLETER

Pour trouver notre notebook final, il suffit de cliquer sur celui qui s'intitule **0_RAPPORT.ipynb** 



### Récapitulatif des notebooks et des scripts présents sur notre Github : 

__0_RAPPORT.ipynb__ : Notebook final renvoyant aux autres notebooks

# __0_notebooks__ : dossier qui rassemble tous nos notebooks
- __1_Script_scraping.ipynb__ : Script **à ne pas exécuter** qui a permis de récolter les tweets avec le nombre de likes, retweets et les informations jugées nécessaires à la constitution de notre base de données 
- __2_nettoyage.ipynb__ : Nettoyage de la base de données, classement des tweets par date et suppression des bots
- __4_Statdesc.ipynb__ : Constitution de graphiques pour révéler les tendances des tweets en 2024
- __4.5_Statdesc_violent.ipynb__ : Statistiques descriptives à partir de l'analyse de sentiment issue du NLP
- __6_Analyse_textuelle.ipynb__ : Fait ressortir la fréquence et l'utilisation de certains mots dans les tweets en 2024
- __7_Modelisation.ipynb__ : 

# __1_scripts__ : dossier rassemblant les scripts 
- __3_NLP.py__ : Script pour créer le réseau de neurones et la tokenisation adaptée pour trier les tweets
- __3.5_Data_sorting.py__ : Script afin de traiter une base de données avec le modèle créé dans le script précédent. 

# Dossiers rassemblant les tableaux de données
- __data_fin__ : dossier avec les tableaux de données finales
- __data_processing__ : dossier contenant les sorties du scraping puis les tables intermédiaires lors du nettoyage des données
- __training_data__ :


├── 0_notebooks
    │   ├── 0_RAPPORT.ipynb
    │   ├── 0_rapport.ipynb
    │   ├── 1_Script_scraping.ipynb
    │   ├── 2_nettoyage.ipynb
    │   ├── 4.5_statdesc_violent.ipynb
    │   ├── 4_statdesc.ipynb
    │   ├── 6_analyse_textuelle.ipynb
    │   └── 7_modelisation.ipynb
    ├── 1_scripts
    │   ├── 3.5_Data_sorting.py
    │   └── 3_NLP.py
    ├── README.md
    ├── data_fin
    │   ├── bluesky_def.csv
    │   ├── bluesky_nettoye.xlsx
    │   ├── tweets_fusionnes.xlsx
    │   ├── tweets_fusionnes_def.csv
    │   └── tweets_fusionnes_def.xlsx
    ├── data_processing
    │   ├── bluesky_nettoye.xlsx
    │   ├── tweets_exode_1.xlsx
    │   ├── tweets_exode_1_date.xlsx
    │   ├── tweets_exode_2.xlsx
    │   ├── tweets_exode_2_date.xlsx
    │   ├── tweets_last.xlsx
    │   ├── tweets_last_2.xlsx
    │   ├── tweets_last_2_date.xlsx
    │   ├── tweets_last_3.xlsx
    │   ├── tweets_last_3_date.xlsx
    │   ├── tweets_last_4.xlsx
    │   ├── tweets_last_4_date.xlsx
    │   ├── tweets_last_5.xlsx
    │   ├── tweets_last_5_date.xlsx
    │   ├── tweets_last_6.xlsx
    │   ├── tweets_last_6_date.xlsx
    │   ├── tweets_last_date.xlsx
    │   ├── tweets_leave_p1.xlsx
    │   ├── tweets_leave_p1_date.xlsx
    │   ├── tweets_quit.xlsx
    │   ├── tweets_quit_date.xlsx
    │   ├── tweets_stay_1.xlsx
    │   └── tweets_stay_1_date.xlsx
    ├── structure.txt
    ├── test.py
    ├── training_data
    │   ├── saved_model_optimized_3.h5
    │   ├── tokenizer.pickle
    │   └── train.csv
    ├── tweets_fusionnes.csv
    └── tweets_fusionnes.xlsx
