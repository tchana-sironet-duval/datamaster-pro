import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataMaster Pro", layout="wide")

# ===================== SAFE INIT =====================
if "data" not in st.session_state:
    st.session_state["data"] = []

data = st.session_state["data"]

# ===================== TITLE =====================
st.title("📊 DataMaster Pro - Système de collecte & analyse")
st.markdown("Application intelligente de collecte et d'analyse de données")

# ===================== FORM =====================
st.subheader("📝 Formulaire de collecte")

with st.form("form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        nom = st.text_input("👤 Nom complet")

    with col2:
        age = st.number_input("🎂 Âge", min_value=0, max_value=120, value=18)

    with col3:
        sexe = st.selectbox("⚧ Sexe", ["Homme", "Femme", "Autre"])

    col4, col5 = st.columns(2)

    with col4:
        ville = st.text_input("🏙️ Ville")

    with col5:
        niveau = st.selectbox("🎓 Niveau d'étude", [
            "Primaire", "Secondaire", "Université", "Autre"
        ])

    profession = st.text_input("💼 Profession")

    submit = st.form_submit_button("🚀 Envoyer les données")

# ===================== SAVE SAFE =====================
if submit:
    if nom.strip() == "":
        st.error("❌ Le nom est obligatoire")
    else:
        data.append({
            "Nom": nom,
            "Âge": age,
            "Sexe": sexe,
            "Ville": ville,
            "Niveau": niveau,
            "Profession": profession
        })
        st.success("✅ Données enregistrées !")

# ===================== DATA ANALYSIS =====================
if len(data) > 0:
    df = pd.DataFrame(data)

    st.divider()
    st.subheader("📋 Données collectées")

    st.dataframe(df, use_container_width=True)

    # ===================== METRICS SAFE =====================
    st.subheader("📊 Indicateurs clés")

    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Total participants", len(df))
    col2.metric("🎂 Âge moyen", round(df["Âge"].mean(), 1) if len(df) > 0 else 0)
    col3.metric("🏙️ Villes uniques", df["Ville"].nunique())

    # ===================== GRAPHS =====================
    st.subheader("📈 Analyse graphique")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Sexe")
        st.bar_chart(df["Sexe"].value_counts())

    with col2:
        st.markdown("### 🎓 Niveau")
        st.bar_chart(df["Niveau"].value_counts())

    st.markdown("### 🎂 Âge")
    st.bar_chart(df["Âge"])

    # ===================== DOWNLOAD =====================
    st.subheader("📥 Export")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Télécharger CSV",
        csv,
        "donnees.csv",
        "text/csv"
    )

else:
    st.info("ℹ️ Aucune donnée enregistrée pour le moment.")
