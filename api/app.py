from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fonction pour scraper les conjugaisons
def scrape_conjugations(verb):
    url = f"http://www.les-verbes.com/conjuguer.php?verbe={verb}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Dictionnaire pour stocker les conjugaisons
    verb_conjugations = {
        "Indicatif": {},
        "Subjonctif": {},
        "Conditionnel": {},
        "Impératif": {},
        "Infinitif": {},
        "Participe": {}
    }

    # Récupérer les sections de titres des temps (Indicatif, Subjonctif, etc.)
    verb_tenses = soup.find_all("div", class_="verbetitle")
    verb_boxes = soup.find_all("div", class_="verbebox")

    # Remplir chaque catégorie avec ses conjugaisons respectives
    for i, tense in enumerate(verb_tenses):
        tense_name = tense.h2.text.strip()
        
        if i < len(verb_boxes):
            # Extraire les conjugaisons sous forme de liste
            conjugations = verb_boxes[i].p.get_text().strip().split("\n")
            
            # Affecter aux bons modes verbaux
            if "Indicatif" in tense_name:
                verb_conjugations["Indicatif"][tense_name] = conjugations
            elif "Subjonctif" in tense_name:
                verb_conjugations["Subjonctif"][tense_name] = conjugations
            elif "Conditionnel" in tense_name:
                verb_conjugations["Conditionnel"][tense_name] = conjugations
            elif "Impératif" in tense_name:
                verb_conjugations["Impératif"][tense_name] = conjugations
            elif "Infinitif" in tense_name:
                verb_conjugations["Infinitif"][tense_name] = conjugations
            elif "Participe" in tense_name:
                verb_conjugations["Participe"][tense_name] = conjugations

    # Renvoyer les conjugaisons collectées
    return verb_conjugations

# Route pour afficher les conjugaisons en JSON via paramètre de requête
@app.route('/conjugaison', methods=['GET'])
def conjugate():
    verb = request.args.get('verbe')  # Obtenir le verbe du paramètre de requête
    if not verb:
        return jsonify({"error": "Aucun verbe fourni"}), 400  # Gérer les erreurs si aucun verbe n'est fourni
    
    # Scraper les conjugaisons du verbe donné
    conjugations = scrape_conjugations(verb)
    
    # Renvoyer le résultat en JSON
    return jsonify(conjugations)

# Exécuter l'application sur l'host 0.0.0.0 et le port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
