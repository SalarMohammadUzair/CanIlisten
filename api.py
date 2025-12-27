from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys

sys.path.append('./src')

from lyrics_fetch import get_lyrics
from gemini_analyser import analysis
from file_manager import save_lyrics, save_gemini_response

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')



@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/api/lyrics', methods=['POST'])
def fetch_lyrics():
    data=request.get_json()
    artist = data.get('artist')
    track = data.get('track')
    if not artist or not track:
        return jsonify({"error": "Missing artist or track"}), 400
    lyrics_result = get_lyrics(artist, track)
    if lyrics_result['source'] is None:
        return jsonify({"error": "Lyrics not found"}), 404
    return jsonify(lyrics_result)

@app.route('/api/prompt', methods=['GET'])
def get_prompt():
    try:
        with open('./src/prompt.txt', 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        return jsonify({"prompt": prompt_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/analyze', methods=['POST'])
def analyze_song():
    data = request.get_json()
    artist = data.get('artist')
    lyrics = data.get('lyrics')
    if not artist or not lyrics:
        return jsonify({"error": "Missing artist or lyrics"}), 400
    analysis_result = analysis(artist, lyrics)

    #save_lyrics(lyrics_result['artist'], lyrics_result['title'], lyrics_result)
    

    if analysis_result is None:
        return jsonify({"error": "Analysis failed"}), 500
    #save_gemini_response(artist, track, analysis_result)
    return jsonify(analysis_result)
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')
if __name__ == '__main__':
    app.run(debug=True, port=5000)
