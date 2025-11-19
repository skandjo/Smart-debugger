# 🐍 Assistant Debug Python  
Analyse & Correction Automatique de Scripts Python (GROQ + Streamlit)

Ce projet est un assistant intelligent capable d’analyser un script Python, d’identifier ses erreurs et de proposer des corrections détaillées grâce à l’API **GROQ**.

Il fonctionne en deux modes :

- 🟦 **Mode CLI (Ligne de commande)**  
  → Analyse et corrige directement un fichier Python local.

- 🟩 **Mode Streamlit (Interface graphique)**  
  → Permet d’uploader un fichier Python, de visualiser l’analyse et de télécharger une version corrigée du fichier **sans modifier l’original**.

---

## 📦 Installation

### 1. Cloner le dépôt

```bash
git clone <ton_repo>
cd ton_repo
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer l’API GROQ (fichier `.env`)

Ce projet nécessite une clé API GROQ.

➡️ **IMPORTANT : le fichier `.env` n’est pas fourni** (sécurité)  
➡️ **Il ne doit jamais être envoyé sur GitHub**

Créer ton fichier `.env` :

```bash
touch .env
```

Avec le contenu :

```
GROQ_API_KEY=ta_clef_api_groq
MODEL_NAME=openai/gpt-oss-20b
```

> ⚠️ Le `.env` est déjà ignoré via `.gitignore`.

---

## 🛠 Mode CLI (Ligne de commande)

Ce mode permet de :

- Exécuter un fichier Python
- Lire et afficher les erreurs
- Envoyer le code + erreur à GROQ
- Recevoir des corrections détaillées
- **Appliquer automatiquement les correctifs au fichier original**

### ▶️ Lancer une analyse :

```bash
py .\main.py <fichier_avec_erreur.py>
```

### Exemple :

```bash
py .\main.py .\script_secondaire.py
```

---

## 🌐 Mode Streamlit (Interface graphique)

### ▶️ Lancer l'application

```bash
streamlit run app.py
```

### Fonctionnalités :

- 📂 Upload d’un ou plusieurs fichiers `.py`
- 🎯 Sélection du fichier principal
- ▶️ Exécution et affichage stdout/stderr
- 🔍 Analyse via GROQ
- ❌ Liste des erreurs détectées
- 🔧 Code complet corrigé
- ⬇️ **Téléchargement du fichier corrigé (`script_corrige.py`)**

⚠️ **En mode Streamlit, le fichier original n’est jamais modifié.**

---

## 📁 Arborescence du projet

```
├── agent.py
├── app.py
├── main.py
├── utils.py
├── config.py
├── context.txt
├── prompt.txt
├── requirements.txt
└── README.md
```

---

## 🧪 Exemple d’utilisation Streamlit

1. Upload d’un fichier `bug.py`
2. Exécution → affichage de l’erreur
3. Analyse → corrections proposées
4. Téléchargement → `script_corrige.py`

---

## 🤝 Contributions

Tu peux améliorer :

- L’analyse multi-fichiers
- Le diff visuel avant/après
- Un thème Streamlit custom
- Le déploiement en ligne

N’hésite pas à proposer des améliorations !

