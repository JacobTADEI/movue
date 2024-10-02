from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

API_KEY = 'f2207c3fad17258662926c56f23cc37e'
DATA_FILE = 'seen_media.json'

# Exemple de mapping des genres
genre_mapping = {
    28: 'Action',
    12: 'Aventure',
    16: 'Animation',
    35: 'Comédie',
    80: 'Crime',
    99: 'Documentaire',
    18: 'Drame',
    10751: 'Famille',
    14: 'Fantastique',
    36: 'Histoire',
    27: 'Horreur',
    10402: 'Musique',
    9648: 'Mystery',
    10749: 'Romance',
    878: 'Science-Fiction',
    10770: 'Téléfilm',
    53: 'Thriller',
    10752: 'Guerre',
    37: 'Western'
}

def load_seen_media():
    try:
        with open(DATA_FILE, 'r') as file:
            data = file.read().strip()
            return json.loads(data) if data else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_seen_media(seen_media):
    with open(DATA_FILE, 'w') as file:
        json.dump(seen_media, file, indent=4)

@app.route('/')
def index():
    seen_media = load_seen_media()
    return render_template('index.html', seen_media=seen_media)

@app.route('/search', methods=['POST'])
def search():
    title = request.form['title']
    if not title:
        return jsonify({'error': 'Le titre de recherche ne peut pas être vide'}), 400

    url = f'https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={title}&language=fr'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        media_list = data.get('results', [])

        if not media_list:
            return jsonify({'error': 'Aucun résultat trouvé pour le titre donné'}), 404

        # Process each media item to include genre names
        for media in media_list:
            genre_ids = media.get('genre_ids', [])
            genres = [genre_mapping.get(genre_id, 'Inconnu') for genre_id in genre_ids]
            media['genres'] = ', '.join(genres)

        return jsonify(media_list)

    except requests.RequestException as e:
        return jsonify({'error': f'Erreur lors de la recherche : {str(e)}'}), 500

@app.route('/add', methods=['POST'])
def add():
    media = request.json
    seen_media = load_seen_media()
    seen_media.append(media)
    save_seen_media(seen_media)
    return jsonify({'status': 'success'})

@app.route('/remove', methods=['POST'])
def remove():
    media_id = request.json.get('id')
    seen_media = load_seen_media()
    seen_media = [media for media in seen_media if media['id'] != media_id]
    save_seen_media(seen_media)
    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
