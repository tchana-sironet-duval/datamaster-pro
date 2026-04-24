import streamlit as st
import sqlite3
from datetime import datetime
import os

# ================= CONFIG =================
st.set_page_config(page_title="DataMaster Pro", layout="wide", page_icon="🛡️")

# ================= STYLE PRO =================
st.markdown("""
<style>
body {background-color:#0e1117;color:white;}
h1, h2, h3 {color:#00c6ff;}
.stButton>button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border:none;
    border-radius:10px;
    height:3em;
    font-weight:bold;
}
.card {
    padding:20px;
    border-radius:12px;
    background:#161b22;
    margin:10px 0;
    box-shadow:0 4px 10px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ================= DB =================
def connect_db():
    # Utilisation d'un chemin relatif pour SQLite sur Render
    return sqlite3.connect("datamaster.db", check_same_thread=False)

def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        contact TEXT,
        secteur TEXT,
        note TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

# Initialisation au lancement
init_db()

# ================= DASHBOARD =================
def dashboard():
    st.title("📊 Tableau de bord professionnel")
    
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM data")
    total = c.fetchone()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total des fiches", total)
    col2.metric("Statut système", "En ligne")
    col3.metric("Mode", "Hébergé")

    st.markdown("---")
    st.subheader("📌 Dernières données")

    c.execute("SELECT * FROM data ORDER BY id DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()

    for d in rows:
        st.markdown(f"""
        <div class='card'>
        <b>{d[1]}</b><br>
        📞 {d[2]} | 🏢 {d[3]}<br>
        <small>📅 {d[5]}</small>
        </div>
        """, unsafe_allow_html=True)

# ================= AJOUT =================
def add_data():
    st.title("📥 Ajouter une nouvelle fiche")

    with st.form("ajout"):
        nom = st.text_input("Nom")
        contact = st.text_input("Contact")
        secteur = st.selectbox("Secteur", ["Informatique","Finance","Éducation","Business"])
        note = st.text_area("Note")

        if st.form_submit_button("Enregistrer"):
            if nom and contact:
                conn = connect_db()
                c = conn.cursor()
                c.execute("INSERT INTO data(nom,contact,secteur,note,created_at) VALUES(?,?,?,?,?)",
                          (nom, contact, secteur, note, datetime.now().strftime("%d/%m/%Y %H:%M")))
                conn.commit()
                conn.close()
                st.success("✅ Donnée enregistrée avec succès")
            else:
                st.error("⚠️ Champs obligatoires manquants")

# ================= GESTION =================
def manage():
    st.title("⚙️ Centre de gestion")
    tab1, tab2, tab3 = st.tabs(["📄 Voir","✏️ Modifier","🗑️ Supprimer"])

    conn = connect_db()
    c = conn.cursor()

    with tab1:
        c.execute("SELECT * FROM data ORDER BY id DESC")
        rows = c.fetchall()
        for d in rows:
            st.markdown(f"""
            <div class='card'>
            <b>ID {d[0]} - {d[1]}</b><br>
            📞 {d[2]} | 🏢 {d[3]}<br>
            📝 {d[4]}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        idm = st.number_input("ID à modifier", min_value=1)
        new = st.text_input("Nouveau nom")
        if st.button("Mettre à jour"):
            if new:
                c.execute("UPDATE data SET nom=? WHERE id=?", (new, idm))
                conn.commit()
                st.success("✅ Mise à jour réussie")
            else:
                st.error("Champ vide")

    with tab3:
        idd = st.number_input("ID à supprimer", min_value=1)
        confirm = st.checkbox("Confirmer la suppression")
        if st.button("Supprimer définitivement"):
            if confirm:
                c.execute("DELETE FROM data WHERE id=?", (idd,))
                conn.commit()
                st.warning("🗑️ Donnée supprimée")
            else:
                st.error("Veuillez confirmer")
    conn.close()

# ================= MAIN =================
with st.sidebar:
    st.title("🚀 DataMaster Pro")
    menu = st.radio("Navigation", ["Dashboard","Ajouter","Gestion"])

if menu == "Dashboard":
    dashboard()
elif menu == "Ajouter":
    add_data()
elif menu == "Gestion":
    manage()
