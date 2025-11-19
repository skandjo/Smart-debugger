import json
from groq import Groq
from utils import read_file, print_result
from config import CONTEXT_FILE, PROMPT_FILE, MODEL_NAME, GROQ_API_KEY
import subprocess
import sys


def load_prompt_and_context(code: str, erreur: str) -> tuple[str, str]:
    """Charge le contexte et remplace le placeholder dans le prompt."""
    context = read_file(CONTEXT_FILE)
    prompt_template = read_file(PROMPT_FILE)

    if not context or not prompt_template:
        raise ValueError("Impossible de charger context.txt ou prompt.txt")

    prompt = prompt_template.replace("{{CODE_A_ANALYSER}}", code)
    prompt = prompt.replace("{{ERREUR}}", erreur)
    return context, prompt


def analyze_code(code: str, erreur: str) -> dict | None:
    """Appelle l'API GROQ pour analyser le code Python."""
    if not GROQ_API_KEY:
        print("[ERREUR] GROQ_API_KEY n'est pas défini.")
        return None

    context, prompt = load_prompt_and_context(code, erreur)

    client = Groq(api_key=GROQ_API_KEY)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        raw_content = response.choices[0].message.content

        try:
            return json.loads(raw_content)
        except json.JSONDecodeError:
            print("[ERREUR] Réponse GROQ non JSON :")
            print(raw_content)
            return None

    except Exception as e:
        print(f"[ERREUR] Appel API GROQ : {e}")
        return None

if __name__ == "__main__":
    """ test sur le ficheir script_secondaire.py"""
    code_file = "script_secondaire.py"
    # Exécuter le script en capturant stdout et stderr
    resultat = subprocess.run(
            [sys.executable, code_file],
            capture_output=True,
            text=True,
            check=False
        )

    code_content = read_file(code_file)
    erreur = resultat.stderr.strip() if resultat.stderr else "Aucune erreur détectée"
    if not code_content:
        sys.exit(1)

    result = analyze_code(code_content, erreur)
    print_result(result)
