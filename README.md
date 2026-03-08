# 🎬 Application de Recommandation de Films - Cinéma Creuse

**Projet Data Analyst** : Une application Streamlit pour proposer des suggestions de films personnalisées aux spectateurs d'un cinéma en Creuse.

---

## 📌 Description
Cette application permet aux utilisateurs de :
- **S’authentifier** avec un compte personnalisé.
- **Explorer un catalogue de films** filtré par genre, époque, durée et note.
- **Consulter les détails d’un film** et obtenir des recommandations similaires (via un algorithme KNN).
- **Gérer un profil utilisateur** (préférences, favoris).

---

## 📂 Structure du Projet

PROJET2_GROUPE4/

│

├── data/

│   ├── comptes.csv                 # Données des comptes utilisateurs

│   ├── catalogue.parquet           # Catalogue des films (format Parquet)

│   ├── images.1.png                # Affiche 1 page d'accueil

│   ├── images.2.png                # Affiche 2 page d'accueil

│   └── images.3.png                # Affiche 3 page d'accueil

│

├── images/

│   ├── capture d'écran

│   ├── ...

│   └── capture d'écran

│

├── pages/

│   ├── catalogue.py                # Page de catalogue et filtres

│   ├── details.py                  # Détails d’un film + recommandations

│   └── page_utilisateur.py         # Profil utilisateur et préférences

│

├── src/

│   └── assets/

│       ├── style.css               # Styles CSS personnalisés

│       └── Tableau_de_bord.pbix    # Tableau de bord Power BI (optionnel)

│

├── app.py                          # Page d’accueil et authentification

└── requirements.txt                # Dépendances Python

---

## 🛠️ Prérequis

### 1. Environnement
- **Python 3.8+**
- **Streamlit** (pour exécuter l’application)
- **Pandas**, **NumPy**, **Scikit-learn** (pour le traitement des données et les recommandations)

### 2. Installation
1. Clonez ce dépôt :
   bash
   git clone https://github.com/dominiquerigault66-droid/projet2_groupe4.git


Installez les dépendances :
bash
pip install -r requirements.txt

Lancez l’application :
bash
streamlit run app.py


🚀 Fonctionnalités Clés
1. Authentification

Système de login sécurisé avec streamlit-authenticator.
Gestion des rôles (utilisateur/admin) via comptes.csv.

2. Catalogue de Films

Filtres avancés : Genre, époque, durée, note.
Affichage dynamique des films correspondants (9 résultats max par page).
Navigation intuitive entre les pages (Accueil, Catalogue, Profil).

3. Recommandations Personnalisées

Algorithme K-Nearest Neighbors (KNN) pour suggérer des films similaires.
Prise en compte des genres, de l’année de sortie et de la durée.
Affichage des recommandations avec leur score de similarité.

4. Profil Utilisateur

Préférences : Langue, âge, mode sombre.
Favoris : Liste des films préférés de l’utilisateur.
Statistiques : (Optionnel) Temps passé à regarder des films.

📊 Données Utilisées

Fichier catalogue.parquet:

Titre, année, durée, genres, note moyenne, nombre de votes, chemin de l’affiche.
Format optimisé pour une lecture rapide avec Pandas.
Ce catalogue a été préparé depuis les données téléchargées de imdb_title_basics, imdb_title_ratings et tmdb selon le processus suivant :
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)

Fichier comptes.csv :

Noms d’utilisateurs, mots de passe (hashés), emails, rôles.


🎨 Design et UX

Interface moderne avec la police LINE Seed JP.
Boutons personnalisés (style Netflix pour une expérience immersive).
Responsive : Adapté aux écrans larges et mobiles.

🔧 Configuration

Personnalisation des filtres : Modifiez les listes liste_genres et liste_époques dans catalogue.py.
Poids des recommandations : Ajustez GENRE_WEIGHT et NUM_WEIGHT dans details.py pour affiner l’algorithme KNN.
Ajout de films : Mettez à jour catalogue.parquet avec de nouvelles entrées.

👥 Contributeurs

Dominique Rigault
Féréol Nyounai
Samira Zeggai
Zina Tiar

📄 Licence
Ce projet est sous licence MIT. Voir LICENSE pour plus de détails.

🙏 Remerciements

Jeu de données : Sites IMDb et TMDb.
Inspiration : Projet réalisé dans le cadre du bootcamp data analyst de la WildCodeSchool (novembre 2025).
Outils : Streamlit, Pandas, Scikit-learn, et la communauté open-source !

📎 Captures d’Écran

Voir le dossier /images

🔗 Liens Utiles

Documentation Streamlit
Guide Pandas
Scikit-learn : KNN
