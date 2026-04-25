import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ================= CONFIG =================
st.set_page_config(page_title="DataStudy Pro", layout="wide", page_icon="📊")

# ================= STYLE =================
st.markdown("""
<style>
body {background-color:#0e1117;color:white;}
h1, h2 {color:#00c6ff;}
.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border:none;
    border-radius:10px;
    height:3em;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)


# ================= DB =================
def connect_db():
    return sqlite3.connect("datastudy.db", check_same_thread=False)

def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        age INTEGER,
        sexe TEXT,
        niveau TEXT,
        ville TEXT,
        profession TEXT,
        satisfaction INTEGER,
        commentaire TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= COLLECTE =================
def collect():
    st.title("📥 Collecte de données (Étude)")

    with st.form("form"):
        nom = st.text_input("Nom (optionnel)")
        age = st.number_input("Âge", min_value=10, max_value=100)
        sexe = st.selectbox("Sexe", ["Homme","Femme"])
        niveau = st.selectbox("Niveau d'étude", ["Secondaire","Licence","Master","Doctorat"])
        ville = st.text_input("Ville")
        profession = st.text_input("Profession")
        satisfaction = st.slider("Niveau de satisfaction", 1, 5)
        commentaire = st.text_area("Commentaire")

        if st.form_submit_button("Enregistrer"):
            conn = connect_db()
            c = conn.cursor()
            c.execute("""
            INSERT INTO data(nom,age,sexe,niveau,ville,profession,satisfaction,commentaire,created_at)
            VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                nom, age, sexe, niveau, ville, profession,
                satisfaction, commentaire,
                datetime.now().strftime("%d/%m/%Y %H:%M")
            ))
            conn.commit()
            conn.close()

            st.success("✅ Donnée enregistrée")

# ================= DASHBOARD =================
def dashboard():
    st.title("📊 Analyse statistique")

    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM data", conn)

    if df.empty:
        st.warning("Aucune donnée disponible")
        return

    # ===== METRICS =====
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", len(df))
    col2.metric("Âge moyen", round(df["age"].mean(), 1))
    col3.metric("Satisfaction moyenne", round(df["satisfaction"].mean(), 1))

    st.markdown("---")

    # ===== GRAPHIQUES =====
    st.subheader("Répartition par sexe")
    st.bar_chart(df["sexe"].value_counts())

    st.subheader("Niveau d'étude")
    st.bar_chart(df["niveau"].value_counts())

    st.subheader("Répartition par ville")
    st.bar_chart(df["ville"].value_counts())

    st.subheader("Satisfaction")
    st.bar_chart(df["satisfaction"].value_counts())

    # ===== TABLE =====
    st.subheader("Données collectées")
    st.dataframe(df)

    # ===== EXPORT =====
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger CSV", csv, "donnees.csv", "text/csv")

    df.to_excel("donnees.xlsx", index=False)
    with open("donnees.xlsx", "rb") as f:
        st.download_button("📥 Télécharger Excel", f, "donnees.xlsx")

    conn.close()

# ================= MAIN =================
if not st.session_state["auth"]:
    login()
else:
    with st.sidebar:
        st.title("📊 DataStudy Pro")
        menu = st.radio("Menu", ["Collecte","Analyse","Déconnexion"])

    if menu == "Collecte":
        collect()
    elif menu == "Analyse":
        dashboard()
    elif menu == "Déconnexion":
        st.session_state["auth"] = False
        st.experimental_rerun()
