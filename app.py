from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fonction pour scraper les conjugaisons
def scrape_conjugations(verb):
    url = f"http://www.les-verbes.com/conjuguer.php?verbe={verb}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Dictionnaire pour stocker les conjugaisons par mode et temps
    verb_conjugations = {}

    # Trouver tous les modes de conjugaison (par ex., "Indicatif", "Subjonctif", etc.)
    modes = soup.find_all("div", class_="verbetitle")
    for mode in modes:
        mode_name = mode.find("h2").text.strip()  # Le nom du mode (par ex., "Indicatif")
        verb_conjugations[mode_name] = {}

        # Trouver tous les temps pour ce mode (par ex., "Présent", "Passé composé")
        tenses = mode.find_next_siblings("div", class_="verbebox")
        for tense in tenses:
            tense_name = tense.find("a").text.strip()  # Le nom du temps (par ex., "Présent")
            conjugations = tense.p.get_text().strip().split("\n")
            conjugations = [conj.strip() for conj in conjugations if conj.strip()]  # Nettoyer les données

            # Ajouter le temps et ses conjugaisons dans la structure
            verb_conjugations[mode_name][tense_name] = conjugations

    return verb_conjugations

# Route pour afficher les conjugaisons en HTML
@app.route('/conjugaison', methods=['GET'])
def conjugate():
    verb = request.args.get('verbe')  # Obtenir le verbe du paramètre de requête
    if not verb:
        return "Aucun verbe fourni", 400  # Gérer les erreurs si aucun verbe n'est fourni
    
    # Scraper les conjugaisons du verbe donné
    conjugations = scrape_conjugations(verb)

    # Générer du HTML dynamique pour afficher les conjugaisons
    html_content = f"<h1>Conjugaison du verbe {verb}</h1>"

    for mode, tenses in conjugations.items():
        html_content += f"<h2>{mode}</h2>"

        for tense, conjugation in tenses.items():
            html_content += f"<h3>{tense}</h3><ul>"
            for line in conjugation:
                html_content += f"<li>{line}</li>"
            html_content += "</ul>"

    return html_content

# Exécuter l'application sur l'host 0.0.0.0 et le port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
