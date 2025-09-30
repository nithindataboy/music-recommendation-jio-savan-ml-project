# recommendation_engine.py
"""
Backend logic for mood-based music recommendation.
"""

import random
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'data', 'new_balanced_songs1.csv')
if os.path.exists(DATASET_PATH):
    df = pd.read_csv(DATASET_PATH)
else:
    df = None

def recommend_music(mood: str, num_songs: int = 5):
    print(f"DEBUG: Requested mood: '{mood}'")
    print(f"DEBUG: Available moods in dataset: {df['mood'].unique() if df is not None else 'None'}")
    # ...existing code...
    """
    Recommend Telugu music tracks based on labeled mood from songs_with_mood.csv.
    """
    if df is None:
        return []
    mood = mood.strip().lower()
    # Clean all columns for whitespace and encoding issues
    df_clean = df.copy()
    for col in df_clean.columns:
        if df_clean[col].dtype == object:
            df_clean[col] = df_clean[col].astype(str).str.strip()
    df_clean['mood'] = df_clean['mood'].str.lower()
    telugu_tracks = df_clean[df_clean['mood'] == mood]
    print(f"DEBUG: Found {len(telugu_tracks)} songs for mood '{mood}'")
    if telugu_tracks.empty:
        # Advanced fallback: fuzzy matching for similar moods
        from difflib import get_close_matches
        moods_available = df_clean['mood'].unique().tolist()
        close = get_close_matches(mood, moods_available, n=1, cutoff=0.6)
        if close:
            telugu_tracks = df_clean[df_clean['mood'] == close[0]]
            print(f"DEBUG: Fuzzy match used: '{close[0]}'")
        else:
            print("DEBUG: No fuzzy match found.")
    if telugu_tracks.empty:
        return []
    
    # Drop duplicates to avoid key errors in Streamlit
    telugu_tracks.drop_duplicates(subset=['url'], inplace=True)

    sample = telugu_tracks.sample(n=min(num_songs, len(telugu_tracks)))
    return [
        {
            'track_name': row['title'],
            'artist_name': row['artist'],
            'album_name': row['album'],
            'year': row['year'],
            'artwork_url': row['image'],
            'track_url': row['url'],
            'duration': row['duration'],
            'mood': row['mood']
        }
        for _, row in sample.iterrows()
    ]


    # ...function replaced above...

if __name__ == "__main__":
    import streamlit as st

    st.title("Mood-based Music Recommendation")
    mood_input = st.text_input("Enter your mood:")
    num_songs_input = st.slider("Number of songs:", 1, 10, 3)

    if st.button("Get Recommendations"):
        recommendations = recommend_music(mood_input, num_songs_input)
        st.write("Recommended songs:")
        for song in recommendations:
            st.write(f"- {song}")
