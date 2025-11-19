import streamlit as st
import tempfile
import subprocess
import sys
import os
from pathlib import Path

# Import backend functions
from utils import read_file, print_result
from agent import analyze_code


st.set_page_config(
    page_title="Debug Assistant – Python",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 Assistant Debug Python (GROQ)")
st.write("Analyse, exécution et correction automatique de vos scripts Python.")


# ----------------------------------------------
# UPLOAD DE FICHIERS
# ----------------------------------------------
uploaded_files = st.file_uploader(
    "📂 Importez un ou plusieurs fichiers Python",
    type=["py"],
    accept_multiple_files=True
)

temp_dir = tempfile.mkdtemp()

file_paths = []

if uploaded_files:
    st.success(f"{len(uploaded_files)} fichier(s) importé(s).")

    for file in uploaded_files:
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.read())
        file_paths.append(temp_path)

    st.write("📄 Fichiers détectés :")
    st.code("\n".join([Path(p).name for p in file_paths]))


# ----------------------------------------------
# CHOIX DU FICHIER A EXECUTER
# ----------------------------------------------
target_file = None

if file_paths:
    target_file = st.selectbox(
        "Choisissez le fichier principal à exécuter :",
        file_paths
    )

# ----------------------------------------------
# AFFICHAGE CODE ORIGINAL
# ----------------------------------------------
if target_file:
    st.subheader("📜 Code source")
    st.code(read_file(target_file))


# ----------------------------------------------
# EXECUTION DU SCRIPT
# ----------------------------------------------
if target_file and st.button("▶️ Exécuter le script"):

    st.info("Exécution en cours...")

    result = subprocess.run(
        [sys.executable, target_file],
        capture_output=True,
        text=True,
        check=False
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Sortie (stdout)")
        st.code(result.stdout if result.stdout else "[vide]")

    with col2:
        st.subheader("🔴 Erreurs (stderr)")
        st.code(result.stderr if result.stderr else "Aucune erreur détectée")


# ----------------------------------------------
# ANALYSE GROQ DU CODE
# ----------------------------------------------
if target_file and st.button("🔍 Analyser le code avec GROQ"):

    st.info("Analyse en cours, veuillez patienter...")

    code = read_file(target_file)

    # Re-exécute pour capturer stderr
    exec_out = subprocess.run(
        [sys.executable, target_file],
        capture_output=True,
        text=True,
        check=False
    )

    erreur = exec_out.stderr.strip() if exec_out.stderr else "Aucune erreur détectée"

    result = analyze_code(code, erreur)

    if not result:
        st.error("❌ Analyse impossible. Vérifiez l'API KEY GROQ.")
        st.stop()

    erreurs = result.get("erreurs", [])
    code_corrige = result.get("code_corrige", "")

    # Affichage des erreurs détectées
    if erreurs:
        st.subheader("❌ Erreurs détectées")

        for err in erreurs:
            st.markdown(f"""
                ---
                **📌 Ligne :** {err.get('ligne')}  
                **❌ À remplacer :** `{err.get('a_supprimer')}`  
                **🔧 Correction :** `{err.get('remplacement')}`  
                **ℹ️ Explication :** {err.get('explication')}
            """)

        st.subheader("🔧 Code corrigé proposé par l'IA")
        st.code(code_corrige)

    else:
        st.success("✅ Aucune erreur détectée")
        st.stop()

    st.session_state["analysis_result"] = result
    st.session_state["target_file"] = target_file
    st.session_state["corrected_code"] = code_corrige


# ----------------------------------------------
# APPLICATION DES CORRECTIONS
# ----------------------------------------------
if "analysis_result" in st.session_state:

    if st.button("💾 Générer le fichier corrigé à télécharger"):

        result = st.session_state["analysis_result"]
        original_code = read_file(st.session_state["target_file"]).split("\n")
        erreurs = result.get("erreurs", [])

        corrected_lines = original_code.copy()

        # Applique les corrections dans une copie mémoire
        for err in erreurs:
            a_supprimer = err["a_supprimer"]
            remplacement = err["remplacement"]

            try:
                index = corrected_lines.index(a_supprimer)
                corrected_lines[index] = remplacement
            except ValueError:
                st.warning(f"⚠️ Ligne introuvable : {a_supprimer}")

        corrected_code_str = "\n".join(corrected_lines)

        st.subheader("📄 Code corrigé à télécharger")
        st.code(corrected_code_str)

        # Bouton de téléchargement
        st.download_button(
            label="⬇️ Télécharger le fichier corrigé",
            data=corrected_code_str,
            file_name="script_corrige.py",
            mime="text/x-python"
        )

