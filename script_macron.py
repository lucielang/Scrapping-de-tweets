from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://x.com/i/flow/login')
time.sleep(10)

# Connexion
username_input = driver.find_element('name', 'text')
username_input.send_keys('philipa.seilles@ensae.fr')
username_input.send_keys(Keys.RETURN)
time.sleep(5)

webdriver.ActionChains(driver).send_keys('car_pelet').perform()
webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()
time.sleep(5)

password_input = driver.find_element('name', 'password')
password_input.send_keys('w7a4731O')
password_input.send_keys(Keys.RETURN)
time.sleep(5)

# Naviguer vers la recherche
explore_button = driver.find_element(By.XPATH, "//a[@href='/explore']")
explore_button.click()
time.sleep(5)

search_bar = driver.find_element(By.XPATH, "//input[@aria-label='Search query']")
search_bar.send_keys("(leaving OR leave OR quitting) twitter musk until:2024-03-04 since:2024-01-01")
search_bar.send_keys(Keys.RETURN)
time.sleep(7)

link = driver.find_element(By.XPATH, "(//div[@class='css-175oi2r r-18u37iz r-16y2uox r-1wbh5a2 r-tzz3ar r-1pi2tsx r-buy8e9 r-mfh4gg r-2eszeu r-10m9thr r-lltvgl']//a)[2]")
link.click()
time.sleep(6)

# Listes pour stocker les données des tweets
usernames = []
dates = []
contents = []
comments = []
repost = []
likes = []
views = []

# Ensemble pour vérifier l'unicité
tweets_seen = set()


# Fonction pour collecter des tweets
def collect_tweets():
    new_tweets_found = False  # Initialiser le drapeau pour détecter de nouveaux tweets
    tweet_elements = driver.find_elements(By.XPATH, "(//div[contains(@class, 'css-175oi2r r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l')])")
    for element in tweet_elements:
        try:
            username_recup = element.find_element(By.XPATH, ".//a[contains(@class, 'css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21')]").text
            date_recup = element.find_element(By.XPATH, ".//div[contains(@class, 'css-175oi2r r-18u37iz r-1q142lx')]").text
            content_recup = element.find_element(By.XPATH, ".//div[contains(@class, 'css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim')]").text
            stats_recup = element.find_elements(By.XPATH, ".//div[contains(@class, 'css-175oi2r r-xoduu5 r-1udh08x')]")
            comments_recup = stats_recup[0].text
            repost_recup = stats_recup[1].text
            likes_recup = stats_recup[2].text
            views_recup = stats_recup[3].text
            tweet_tuple = (username_recup, date_recup, content_recup)
            
            # Vérifier si le tweet a déjà été vu
            if tweet_tuple not in tweets_seen:
                tweets_seen.add(tweet_tuple) 
                usernames.append(username_recup)
                dates.append(date_recup)
                contents.append(content_recup)
                comments.append(comments_recup)
                repost.append(repost_recup)
                likes.append(likes_recup)
                views.append(views_recup)
                new_tweets_found = True  # Détecter un nouveau tweet

        except Exception as e:
            continue
    return new_tweets_found  # Retourne True si de nouveaux tweets ont été ajoutés


# Boucle pour défiler et collecter jusqu'à obtenir 10 000 tweets
max_no_new_tweets = 5  # Nombre maximal de tentatives sans nouveaux tweets avant de s'arrêter
no_new_tweets_count = 0  # Compteur pour les tentatives sans nouveaux tweets

while len(usernames) < 10000 and no_new_tweets_count < max_no_new_tweets:
    if collect_tweets():  # Si de nouveaux tweets sont collectés
        no_new_tweets_count = 0  # Réinitialiser le compteur si des tweets ont été collectés
    else:
        no_new_tweets_count += 1  # Si aucun tweet n'est collecté, incrémenter le compteur

    # Scrolling pour charger davantage de tweets si aucun nouveau tweet n'est trouvé
    for _ in range(5):  # Défiler 5 fois
        driver.execute_script("window.scrollBy(0, window.innerHeight);")  # Défiler de la hauteur de la fenêtre
        time.sleep(1)  # Attendre le chargement des nouveaux tweets        
        # Récupérer des nouveaux tweets après chaque défilement
        if collect_tweets():  # Si de nouveaux tweets sont trouvés après le défilement
            no_new_tweets_count = 0  # Réinitialiser le compteur
            break  # Sort de la boucle si de nouveaux tweets sont trouvés

    if no_new_tweets_count >= max_no_new_tweets:  # Si le nombre de tentatives sans nouveaux tweets est trop élevé
        print("Aucun nouveau tweet trouvé après plusieurs tentatives, arrêt.")
        break

print(f"Total des tweets récupérés : {len(usernames)}")
driver.quit()

# Créer un DataFrame et enregistrer les données dans un fichier Excel
data = {
    'Username': usernames,
    'Date': dates,
    'Content': contents,
    'Comments': comments,
    'Repost': repost,
    'Likes': likes,
    'Views': views
}

df = pd.DataFrame(data)
df.to_excel("tweets_leave_9.xlsx", index=False)
print("Fichier tweets_leave_9.xlsx créé avec succès.")
