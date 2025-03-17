from flask import Flask, request, jsonify, render_template
from music import MoodMusicMatcher
import os

app = Flask(__name__)

matcher = MoodMusicMatcher()

@app.route('/')
def index():
    return render_template('musicmatcher.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    mood_input = data.get('mood')
    detected_mood = matcher.analyze_mood(mood_input)
    recommendations = matcher.get_recommendations(detected_mood)
    return jsonify(recommendations)

@app.route('/add_song', methods=['POST'])
def add_song():
    title = request.form['title']
    artist = request.form['artist']
    mood = request.form['mood']
    
    if matcher.add_song(title, artist, mood):
        return "Song added successfully!", 200
    else:
        return "Failed to add song.", 400

if __name__ == '__main__':
    # Ensure the database file exists
    if not os.path.exists('songs_database.json'):
        with open('songs_database.json', 'w') as f:
            f.write('{"happy": [], "sad": [], "relaxed": [], "energetic": []}')
    
    app.run(debug=True)