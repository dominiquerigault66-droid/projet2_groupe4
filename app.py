import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
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


st.set_page_config(page_title="Choix de votre film",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items={'Get Help': None,
                               'Report a Bug': None,
                               'About': None,})

# Masque du menu multi-page par défaut
hide_streamlit_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
/* Bouton principal (Afficher résultats) */
div.stButton > button {
    background-color: #E50914;
    color: white;
    font-weight: bold;
    border-radius: 8px;
}

/* Effet au survol */
div.stButton > button:hover {
    background-color: #B20710;
    color: white;
}

</style>
""", unsafe_allow_html=True)
# ===============================
# LECTURE DU CSV UTILISATEURS
# ===============================
df_users = pd.read_csv("data/comptes.csv", dtype=str)
df_users["password"] = df_users["password"].astype(str)

credentials = {"usernames": {}}

for _, row in df_users.iterrows():
    credentials["usernames"][row["name"]] = {
        "name": row["name"],
        "password": row["password"],
        "email": row["email"],
        # CSV column may be misspelled, correct key to avoid KeyError
        "failed_login_attempts": row.get("failed_login_attempts", row.get("failed_login_attemps", "")),
        "logged_in": row["logged_in"],
        "role": row["role"],
    }

# ===============================
# AUTHENTIFICATION
# ===============================
authenticator = Authenticate(
    credentials,
    "cookie_film",
    "cle_secrete_film",
    30
)

authenticator.login(key="login_form_film")

# ===============================
# SI CONNECTÉ
# ===============================
if st.session_state["authentication_status"]:

    # SIDEBAR
    with st.sidebar:
        st.write(f"Bienvenue {st.session_state['name']} 🎬")

        selection = option_menu(menu_title="Menu",
                                options=["Accueil", "Catalogue", "Profil"],
                                icons=["house", "collection", "person"],
                                default_index=0)

        authenticator.logout("Déconnexion")
    


    
    # PAGE ACCUEIL
    if selection == "Accueil":
        st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        🎥 Application de recommandation de films
    </h1>
    """, unsafe_allow_html=True)
        st.write("")
        st.write("")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("data/images.1.png", caption="Film 1")
        with col2:
            st.image("data/images.2.png", caption="Film 2")
        with col3:
            st.image("data/images.3.png", caption="Film 3")
    
    # PAGE CATALOGUE
    elif selection == "Catalogue":
        # explicitly specify path relative to main script
        st.switch_page("pages/catalogue.py")

    # PAGE PROFIL
    elif selection == "Profil":
        st.switch_page("pages/page_utilisateur.py")

    # PAGE CHOIX FILM (unlikely to appear in menu but kept)
    elif selection == "Choisir un film":
        st.title("🎬 Sélectionnez un film")


    

# ===============================
# ERREURS LOGIN
# ===============================
elif st.session_state["authentication_status"] is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("Veuillez entrer vos identifiants")


