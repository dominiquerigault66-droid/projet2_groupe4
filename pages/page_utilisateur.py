import streamlit as st
import pandas as pd 
import os
from streamlit_option_menu import option_menu


# pr charger le CSS

# ========== sidebar navigation ============
with st.sidebar:
    st.write(f"Bienvenue {st.session_state.get('name','')} 🎬")
    sel = option_menu(menu_title="Menu",
                      options=["Accueil","Catalogue","Profil"],
                      icons=["house","collection","person"],
                      default_index=2)
    if sel == "Accueil":
        st.switch_page("app.py")
    elif sel == "Catalogue":
        st.switch_page("pages/catalogue.py")
    # Profil selected: stay here

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


css_path = os.path.join("src", "assets", "style.css")
local_css(css_path)

st.title("⚙️ Réglages ")
st.button("Sauvegarder les modifications")
st.success("Ceci est un exemple de film pour tester ")

#recup données
PATH_DATA = "data/processed/movies_filtered.csv"

st.title("⚙️ Mon Espace Personnel")

# prefs user
st.header("Mes Réglages")
col1, col2 = st.columns(2)

with col1:
    langue = st.selectbox("Langue préférée", ["Français", "Anglais", "Espagnol"])
    age = st.slider("Ton âge", 5, 99, 25)

with col2:
    mode_sombre = st.toggle("Activer le mode nuit 🌙")
    notif = st.checkbox("Recevoir des alertes nouveaux films")

# section ac favoris
st.divider() # Une petite ligne pour séparer
st.header("❤️ Mes Films Favoris")

# exemple de favoris à remplacer par les vrais favoris de l'utilisateur later
mes_favoris = ["Toy Story", "Inception", "Le Roi Lion"]

if mes_favoris:
    for film in mes_favoris:
        st.write(f"✅ {film}")
else:
    st.info("Tu n'as pas encore de favoris. Va vite en choisir !")

# dahsboard 

st.divider()

#st.header("📊 Tes statistiques")
# On peut faire une page stat ac un fichier csv mais ça m'as l'air innutile 
#st.info("Bientôt : Un graphique montrant combien d'heures tu as passé devant des films !")