import streamlit as st
import pandas as pd
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

#trying to fix the error that appears when I load the catalogue page


if "name" not in st.session_state:
    st.session_state["name"] = ""


st.set_page_config(page_title="Catalogue de Films",
                   page_icon="🎬",
                   initial_sidebar_state="collapsed",
                   layout="wide")

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
                            options=["Accueil", "Catalogue", "Profil"],
                            icons=["house", "collection", "person"],
                            default_index=1)

    # navigate when user clicks
    if selection == "Accueil":
        st.switch_page("app.py")  # return to main script
    elif selection == "Profil":
        st.switch_page("pages/page_utilisateur.py")
    # if Catalogue is clicked we are already here so nothing happens

df = pd.read_parquet('data/catalogue.parquet')

# ===============================
# INITIALISATION SESSION
# ===============================
if "results" not in st.session_state:
    st.session_state.results = None

# ===============================
# FILTRES
# ===============================
st.title("🎬 CATALOGUE")

liste_genres = ['Action','Adventure','Animation','Biography','Comedy','Crime',
                'Documentary','Drama','Family','Fantasy','History','Music',
                'Musical','Mystery','News','Romance','Sci-Fi','Sport',
                'Thriller','War','Western']

liste_époques = ["1985 - 1989","1990 - 1994","1995 - 1999","2000 - 2004","2005 - 2009",
                 "2010 - 2014","2015 - 2019","2020 - 2024","2025 - 2029"]

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    selected_genres = st.multiselect("Genre", liste_genres)
with col2:
    selected_époques = st.multiselect("Epoque", liste_époques)
with col3:
    duree_min = st.number_input("Durée mini", 0, 480, 0)
with col4:
    duree_max = st.number_input("Durée maxi", 0, 480, 480)
with col5:
    note_min = st.number_input("Note mini", 0.0, 10.0, 0.0, step=0.1)
with col6:
    note_max = st.number_input("Note maxi", 0.0, 10.0, 10.0, step=0.1)

if st.button("Afficher les résultats"):

    result = df.copy()

    if selected_genres:
        result = result[result['genres'].apply(
            lambda x: all(g in x.split(",") for g in selected_genres)
        )]

    if selected_époques:
        def is_in_epoch(year):
            for epoch in selected_époques:
                start, end = epoch.split(" - ")
                if int(start) <= int(year) <= int(end):
                    return True
            return False

        result = result[result['startYear'].apply(is_in_epoch)]

    result = result[(result['runtimeMinutes'] >= duree_min) &
                    (result['runtimeMinutes'] <= duree_max) &
                    (result['averageRating'] >= note_min) &
                    (result['averageRating'] <= note_max)]

    result = result.sort_values(by=['averageRating','startYear'],
                                ascending=[False,False])

    st.session_state.results = result


# ===============================
# AFFICHAGE DES RESULTATS
# ===============================

base_url = "http://image.tmdb.org/t/p/"
size = "w154"

if st.session_state.results is not None:

    result = st.session_state.results
    st.write(f"**{len(result)} films trouvés**")

    if len(result) == 0:
        st.warning("Aucun film trouvé.")
    else:
        top_9 = result.head(9)
        cols = st.columns(3)

        for i, (_, row) in enumerate(top_9.iterrows()):
            with cols[i % 3]:

                url = base_url + size + row.poster_path if row.poster_path else ""

                st.markdown("""
                <div style="
                    border:1px solid #ddd;
                    border-radius:8px;
                    padding:10px;
                    margin-bottom:15px;
                    background-color:#f9f9f9;">
                """, unsafe_allow_html=True)

                # Sous-colonnes dans la carte
                subcol1, subcol2 = st.columns([1,2])
                with subcol1:
                    if url:
                        st.image(url, use_container_width=True)

                with subcol2:
                    st.write(f"**{row.primaryTitle} ({row.startYear})**")
                    st.write(f"Note : {row.averageRating}")
                    st.write(f"Durée : {row.runtimeMinutes} min")
                    st.write(f"Genres : {row.genres}")

                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("Détails", key=f"details_{i}"):

                    st.session_state.selected_movie = {
                        "titre": row['primaryTitle'],
                        "annee": row['startYear']
                    }

                    st.switch_page("pages/details.py")