import json
import os
from textblob import TextBlob
import random
import nltk

# Download required NLTK data
# Add this method to the __init__ method
def __init__(self):
    """Initialize the MoodMusicMatcher with the songs database."""
    # Ensure the database file exists with initial structure
    if not os.path.exists('songs_database.json'):
        initial_db = {
            "happy": [
                {"title": "Happy", "artist": "Pharrell Williams"},
                {"title": "Can't Stop the Feeling!", "artist": "Justin Timberlake"}
            ],
            "sad": [
                {"title": "Someone Like You", "artist": "Adele"},
                {"title": "Fix You", "artist": "Coldplay"}
            ],
            "relaxed": [
                {"title": "Banana Pancakes", "artist": "Jack Johnson"},
                {"title": "Weightless", "artist": "Marconi Union"}
            ],
            "energetic": [
                {"title": "Shake It Off", "artist": "Taylor Swift"},
                {"title": "Breathe Me", "artist": "Sia"}
            ]
        }
        with open('songs_database.json', 'w') as f:
            json.dump(initial_db, f, indent=4)
    
    self.load_database()
    self.mood_keywords = {
        'happy': ['happy', 'joy', 'excited', 'cheerful', 'great', 'wonderful', 'fantastic'],
        'sad': ['sad', 'down', 'depressed', 'gloomy', 'unhappy', 'miserable', 'blue'],
        'relaxed': ['relaxed', 'calm', 'peaceful', 'tranquil', 'serene', 'mellow', 'chill'],
        'energetic': ['energetic', 'pumped', 'active', 'lively', 'dynamic', 'vigorous', 'motivated']
    }

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading required NLTK data...")
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

class MoodMusicMatcher:
    def __init__(self):
        """Initialize the MoodMusicMatcher with the songs database."""
        self.load_database()
        self.mood_keywords = {
            'happy': ['happy', 'joy', 'excited', 'cheerful', 'great', 'wonderful', 'fantastic'],
            'sad': ['sad', 'down', 'depressed', 'gloomy', 'unhappy', 'miserable', 'blue'],
            'relaxed': ['relaxed', 'calm', 'peaceful', 'tranquil', 'serene', 'mellow', 'chill'],
            'energetic': ['energetic', 'pumped', 'active', 'lively', 'dynamic', 'vigorous', 'motivated']
        }

    def load_database(self):
        """Load the songs database from the JSON file."""
        try:
            with open('songs_database.json', 'r') as file:
                self.songs_db = json.load(file)
        except FileNotFoundError:
            print("Error: Songs database file not found!")
            self.songs_db = {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in database file!")
            self.songs_db = {}

    def save_database(self):
        """Save the current songs database to the JSON file."""
        try:
            with open('songs_database.json', 'w') as file:
                json.dump(self.songs_db, file, indent=4)
            print("Database updated successfully!")
        except Exception as e:
            print(f"Error saving database: {str(e)}")

    def analyze_mood(self, user_input):
        """
        Analyze the user's input to determine their mood.
        Uses simple keyword matching and sentiment analysis.
        """
        # Convert input to lowercase for better matching
        user_input = user_input.lower()
        
        # First try direct keyword matching
        for mood, keywords in self.mood_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                return mood
        
        # If no direct match, use sentiment analysis as a fallback
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity
        
        if sentiment > 0.3:
            return 'happy'
        elif sentiment < -0.3:
            return 'sad'
        elif 'energy' in user_input or 'active' in user_input:
            return 'energetic'
        else:
            return 'relaxed'

    def get_recommendations(self, mood):
        """Get song recommendations based on the detected mood."""
        if mood in self.songs_db:
            songs = self.songs_db[mood]
            return songs
        return []

    def add_song(self, title, artist, mood):
        """Add a new song to the database."""
        if mood not in self.songs_db:
            print(f"Invalid mood: {mood}")
    
            return False
        
        new_song = {"title": title, "artist": artist}
        self.songs_db[mood].append(new_song)
        self.save_database()
        return True

    def display_recommendations(self, songs):
        """Display the recommended songs in a formatted way."""
        if not songs:
            print("\nNo songs found for this mood.")
            return
        
        print("\nRecommended songs for your mood:")
        print("-" * 40)
        for i, song in enumerate(songs, 1):
            print(f"{i}. {song['title']} - {song['artist']}")

def main():
    """Main function to run the Mood Music Matcher program."""
    matcher = MoodMusicMatcher()
    
    while True:
        print("\n=== Mood Music Matcher ===")
        print("1. Get song recommendations")
        print("2. Add a new song")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            mood_input = input("\nHow are you feeling today? Describe your mood: ")
            try:
                detected_mood = matcher.analyze_mood(mood_input)
                print(f"\nDetected mood: {detected_mood.capitalize()}")
                recommendations = matcher.get_recommendations(detected_mood)
                matcher.display_recommendations(recommendations)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                
        elif choice == '2':
            title = input("Enter song title: ")
            artist = input("Enter artist name: ")
            print("\nAvailable moods:", ", ".join(matcher.mood_keywords.keys()))
            mood = input("Enter mood category: ").lower()
            
            if matcher.add_song(title, artist, mood):
                print("Song added successfully!")
            else:
                print("Failed to add song.")
                
        elif choice == '3':
            print("\nThank you for using Mood Music Matcher!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 