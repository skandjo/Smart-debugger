import json
from pathlib import Path

def read_file(path: str | Path) -> str | None:
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            return fp.read()
    except Exception as e:
        print(f"[ERREUR] Impossible de lire {path} : {e}")
        return None



def print_result(result):
    """Affiche le résultat JSON généré par le modèle."""
    if not result:
        print("[ERREUR] Aucun résultat à afficher.")
        return

    print("\n" + "=" * 60)
    print("ANALYSE DU CODE (GROQ)")
    print("=" * 60)

    erreurs = result.get("erreurs", [])

    if erreurs:
        print("\n❌ ERREURS DÉTECTÉES :")
        for err in erreurs:
            print("-" * 60)
            print(f"📌 Ligne : {err.get('ligne', 'N/A')}")
            print(f"❌ À supprimer : {err.get('a_supprimer', 'N/A')}")
            print(f"🔧 Correction  : {err.get('remplacement', 'N/A')}")
            print(f"ℹ️ Explication : {err.get('explication', 'N/A')}")
    else:
        print("\n✅ Aucune erreur détectée")
        return
    print("\n🔧 CODE ENTIER CORRIGÉ :")
    print("-" * 60)
    print(result.get("code_corrige", "N/A"))
    print("-" * 60)



if __name__ == "__main__":
    
    content = read_file("context.txt")
    if content:
        print("Contenu du fichier context.txt :")
        print(content)
    