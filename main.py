import sys
from utils import read_file, print_result
from agent import analyze_code
import subprocess

def apply_fixes_to_file(filepath, result):
    """Applique les corrections après validation de l'utilisateur."""

    erreurs = result.get("erreurs", [])
    if not erreurs:
        print("\n[INFO] Aucun correctif à appliquer au fichier.")
        return


    print("\n⚠️ Souhaites-tu appliquer les corrections au fichier ? (o/n)")
    choix = input("> ").strip().lower()
    if choix not in ("o", "oui", "y", "yes"):
        print("\n[INFO] Aucune modification n'a été appliquée.")
        return
    print("\n[INFO] Application des correctifs au fichier...")

    content = read_file(filepath).split("\n")

    # On applique les corrections par recherche exacte
    for err in erreurs:
        a_supprimer = err["a_supprimer"]
        remplacement = err["remplacement"]
        ligne = err["ligne"]
        # Remplacement simple : one-liner INSIDE the content
        try:
            index = content.index(a_supprimer)
            content[index] = remplacement
            print(f"  ✔ Correction appliquée à la ligne {ligne}: {a_supprimer} → {remplacement}")
        except ValueError:
            print(f"  ❌ Impossible de trouver la ligne exacte : {a_supprimer}")
            print("    (L’IA a mal compté ou modifié les espaces)\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print("\n[OK] Fichier corrigé et mis à jour avec succès !")



def run_debug_process():
    if len(sys.argv) < 2:
        print("Usage : python agent_debug.py <fichier.py>")
        sys.exit(1)

    python_file = sys.argv[1]
    code = read_file(python_file)
    # Exécuter le script en capturant stdout et stderr
    resultat = subprocess.run(
            [sys.executable, python_file],
            capture_output=True,
            text=True,
            check=False
        )
    
    erreur = resultat.stderr.strip() if resultat.stderr else "Aucune erreur détectée"

    if not code:
        print("[ERREUR] Impossible de lire le fichier.")
        sys.exit(1)

    print(f"[INFO] Analyse du fichier : {python_file}\n")

    result = analyze_code(code, erreur)

    print_result(result)
    if result:
        apply_fixes_to_file(python_file, result)




if __name__ == "__main__":
    run_debug_process()
