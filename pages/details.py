import numpy as np
import pandas as pd
import streamlit as st
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from streamlit_option_menu import option_menu


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=LINE+Seed+JP:wght@400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'LINE Seed JP', sans-serif !important;
    font-weight: 400 !important;
    font-size: 21px !important;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Détails du Film",
                   page_icon="🎬", 
                   initial_sidebar_state="collapsed")

# Masque du menu multi-page par défaut
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with st.sidebar:
    st.write(f"Bienvenue {st.session_state['name']} 🎬")

    selection = option_menu(menu_title="Menu",
                            options=["Accueil", "Catalogue"],
                            icons=["house", "collection"],
                            default_index=0)
    
# Vérifier si un film est sélectionné
if "selected_movie" not in st.session_state:
    st.error("Aucun film sélectionné.")
    st.stop()

titre = st.session_state.selected_movie["titre"]
annee = st.session_state.selected_movie["annee"]

st.title(f"Détails du film : {titre} ({annee})")

df = pd.read_parquet('data/catalogue.parquet')

movie_details = df[
    (df['primaryTitle'] == titre) &
    (df['startYear'] == annee)
].iloc[0]


# ===============================
# RECUPERER AFFICHE
# ===============================

base_url = "http://image.tmdb.org/t/p/"

backdrop_sizes = ["w300","w780","w1280","original"]
logo_sizes = ["w45","w92","w154","w185","w300","w500","original"]
poster_sizes = ["w92","w154","w185","w342","w500","w780","original"]
profile_sizes = ["w45","w185","h632","original"]
still_sizes = ["w92","w185","w300","original"]

size = "w154"

if movie_details['poster_path'] is None:
    url = ""
else:
    url = base_url + size + movie_details['poster_path']

# ===============================
# AFFICHER DETAILS
# ===============================

col1, col2 = st.columns([1, 1])

with col1:
    st.write(f"**Titre original :** {movie_details['originalTitle']}")
    st.write(f"**Année :** {movie_details['startYear']}")
    st.write(f"**Durée :** {movie_details['runtimeMinutes']} minutes")
    st.write(f"**Genres :** {movie_details['genres']}")
    st.write(f"**Note :** {movie_details['averageRating']} ({movie_details['numVotes']} votes)")

with col2:
    if url:
        st.image(url)


# ===============================
# RECOMMANDATIONS KNN
# ===============================
st.subheader("🎯 Films recommandés")

# Nettoyage des données

df_movie = df.loc[df['titleType'] =='movie']
df_movie = df_movie[df_movie["isAdult"] == 0].copy()

df_movie.drop(columns=['titleType'], inplace=True)
df_movie.drop(columns=['endYear'], inplace=True)
df_movie.drop(columns=['isAdult'], inplace=True)

df_movie = df_movie.loc[df['startYear'] !='\\N']
df_movie =  df_movie.loc[df['runtimeMinutes'] !='\\N']
df_movie =  df_movie.loc[df['genres'] != '\\N']

df_movie = df_movie.astype({'startYear' : 'int', 'runtimeMinutes':'int'} )

# Encodage des données

df_dummies = df_movie["genres"].str.get_dummies(sep=",").astype("int8")
df_feat = pd.concat([df_movie[["tconst", "primaryTitle", "startYear", "runtimeMinutes"]],
                     df_dummies],axis=1)
df_feat = df_feat.reset_index(drop=True)

X_num = df_feat[["startYear", "runtimeMinutes"]].copy()
X_gen = df_dummies.copy()

# Standardisation des données
scaler = StandardScaler()
X_num_scaled = scaler.fit_transform(X_num)

GENRE_WEIGHT = 2.0
NUM_WEIGHT   = 1.0

X_gen_weighted = X_gen.to_numpy(dtype=float) * GENRE_WEIGHT
X_num_weighted = X_num_scaled * NUM_WEIGHT

X_final = np.hstack([X_num_weighted, X_gen_weighted])

# Création et entraînement du modèle
@st.cache_resource
def build_knn_model(X):
    model = NearestNeighbors(n_neighbors=11, metric="cosine")
    model.fit(X)
    return model

knn = build_knn_model(X_final)

# Préparation de l'affichage des résultats
df_display = df_feat[["tconst", "primaryTitle", "startYear", "runtimeMinutes"]].copy()
df_display["genres"] = df_movie["genres"].reset_index(drop=True)

def recommend_movies(title : str,
                     model : NearestNeighbors,
                     k : int,
                     df : pd.DataFrame,
                     year : int | None = None) -> pd.DataFrame:

    # --- 1) Trouver le film cible (match exact sur le titre) ---
    candidates = df[df["primaryTitle"].str.lower() == titre.lower()]

    if candidates.empty:
        raise ValueError(f"Film introuvable : {title}")

    # Si plusieurs films portent le même titre (remake, etc.), l'année permet de choisir le bon
    if year is not None:
        candidates_year = candidates[candidates["startYear"] == annee]
        if not candidates_year.empty:
            candidates = candidates_year

    # Si plusieurs candidats restent, on prend le premier (en Streamlit on peut proposer une liste)
    idx = candidates.index[0]

    # --- 2) Calculer les voisins ---
    distances, indices = model.kneighbors(X_final[idx].reshape(1, -1),
                                          n_neighbors=k+1)

    # distances/indices sont des tableaux 2D -> on aplati
    distances = distances.flatten()
    indices = indices.flatten()

    # --- 3) Construire les recommandations ---
    recos = df.iloc[indices].copy()
    recos["distance"] = distances

    # Retirer le film de départ (souvent distance=0)
    recos = recos[recos.index != idx]

    # Trier : distance petite = film plus similaire
    recos = recos.sort_values("distance", ascending=True).reset_index(drop=True)

    # Garder k recommandations
    recos = recos.head(k).reset_index(drop=True)

    # Trier : distance petite = film plus similaire
    recos = recos.sort_values("distance", ascending=True).reset_index(drop=True)

    return recos

recos = recommend_movies(title = movie_details['primaryTitle'],
                 model = knn,
                 k = 6,
                 df = df_display,
                 year = movie_details['startYear'])

for _,row in recos.iterrows():
    st.markdown(f"""
    **🎬 {row['primaryTitle']} ({row['startYear']})**
    Durée : {row['runtimeMinutes']} min
    Genres : {row['genres']}
    Distance : {row['distance']:.3f}""")


# ===============================
# BOUTON RETOUR
# ===============================

if st.button("Retour au catalogue"):
    st.switch_page("pages/catalogue.py")