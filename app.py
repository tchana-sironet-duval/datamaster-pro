import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataMaster Pro", layout="wide")

# ===================== TITLE =====================
st.title("📊 DataMaster Pro - Système de collecte & analyse")
st.markdown("Application intelligente de collecte et d'analyse de données")

# ===================== INIT DATA =====================
if "data" not in st.session_state:
    st.session_state.data = []

# ===================== FORM =====================
st.subheader("📝 Formulaire de collecte")

col1, col2, col3 = st.columns(3)

with st.form("form"):
    with col1:
        nom = st.text_input("👤 Nom complet")
        age = st.number_input("🎂 Âge", min_value=0, max_value=120)

    with col2:
        sexe = st.selectbox("⚧ Sexe", ["Homme", "Femme", "Autre"])
        ville = st.text_input("🏙️ Ville")

    with col3:
        niveau = st.selectbox("🎓 Niveau d'étude", [
            "Primaire", "Secondaire", "Université", "Autre"
        ])
        profession = st.text_input("💼 Profession")

    submit = st.form_submit_button("🚀 Envoyer les données")

# ===================== SAVE =====================
if submit:
    st.session_state.data.append({
        "Nom": nom,
        "Âge": age,
        "Sexe": sexe,
        "Ville": ville,
        "Niveau": niveau,
        "Profession": profession
    })
    st.success("✅ Données enregistrées avec succès !")

# ===================== DATAFRAME =====================
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    st.divider()
    st.subheader("📋 Données collectées")

    st.dataframe(df, use_container_width=True)

    # ===================== METRICS =====================
    st.subheader("📊 Indicateurs clés")

    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Total participants", len(df))
    col2.metric("🎂 Âge moyen", round(df["Âge"].mean(), 1))
    col3.metric("🏙️ Villes uniques", df["Ville"].nunique())

    # ===================== GRAPHS =====================
    st.subheader("📈 Analyse graphique")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Répartition par sexe")
        st.bar_chart(df["Sexe"].value_counts())

    with col2:
        st.markdown("### 🎓 Niveau d'étude")
        st.bar_chart(df["Niveau"].value_counts())

    st.markdown("### 🎂 Distribution des âges")
    st.bar_chart(df["Âge"])

    # ===================== DOWNLOAD =====================
    st.subheader("📥 Export des données")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Télécharger en CSV",
        csv,
        "donnees.csv",
        "text/csv"
    )

else:
    st.info("ℹ️ Aucune donnée pour le moment. Remplis le formulaire 👆")
