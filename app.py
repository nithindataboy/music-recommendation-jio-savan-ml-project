import streamlit as st
from recommendation_engine import recommend_music
import pandas as pd
import os

st.set_page_config(page_title="Mood-Based Music Recommendation", layout="centered")

# Inject custom CSS for background image and glassmorphism
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
        min-height: 100vh;
    }
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(30, 30, 30, 0.35);
        z-index: 0;
    }
    .title-card {
        background: #fff;
        border-radius: 24px;
        padding: 18px 28px;
        margin: 40px auto;
        max-width: 720px;
        text-align: center;
        z-index: 1;
        position: relative;
    }
    .glass-card {
        position: relative;
        z-index: 1;
        background: #fff;
        border-radius: 24px;
        padding: 36px 28px;
        margin: 40px auto;
        max-width: 720px;
    }
    h1 {
        color: #000 !important;
    }
    h2, h3, h4, h5, h6 {
        color: #fff !important;
    }
    </style>
    <div class="overlay"></div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title-card"><h1>🎵 Mood Based Music Recommendation</h1></div>', unsafe_allow_html=True)

# Load data
dataset_path = os.path.join(os.path.dirname(__file__), 'data', 'new_balanced_songs1.csv')
if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)
    moods = sorted(df['mood'].dropna().unique())
else:
    st.error("Dataset not found. Please make sure 'new_balanced_songs1.csv' is in the 'data' directory.")
    st.stop()

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('''
    <span style='color:#222;font-size:1.1em;font-weight:bold;'>Select or type your mood and get personalized Telugu music suggestions!</span><br>
    <span style='color:#222;font-weight:bold;'>Select a mood or type your own. Choose how many recommendations you want.</span><br>
''', unsafe_allow_html=True)
mood = st.selectbox("Choose your mood:", moods)
custom_mood = st.text_input("Or type your mood:")
num_songs = st.slider("Number of recommendations:", 1, 10, 5)
recommend_button = st.button("Recommend Music")
st.markdown('</div>', unsafe_allow_html=True)


selected_mood = custom_mood if custom_mood else mood

if recommend_button:
    with st.spinner(f"Finding {selected_mood} songs..."):
        recommendations = recommend_music(selected_mood, num_songs)
        if recommendations:
            st.subheader(f"Recommended Telugu tracks for '{selected_mood.title()}':")
            for track in recommendations:
                st.markdown(f"<div style='background:#fff;border-radius:18px;padding:18px 16px;margin-bottom:18px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'>"
                            f"<span style='font-size:1.2em;font-weight:bold;color:#1976d2'>{track['track_name']}</span> <br>"
                            f"<span style='color:#000;font-weight:bold'>by <b style='color:#000'>{track['artist_name']}</b></span><br>"
                            f"<span style='color:#000;font-weight:bold'>Album:</span> <b style='color:#000'>{track['album_name']}</b> &nbsp;|&nbsp; <span style='color:#000;font-weight:bold'>Year:</span> <b style='color:#000'>{track['year']}</b> &nbsp;|&nbsp; <span style='color:#000;font-weight:bold'>Duration:</span> <b style='color:#000'>{track['duration']}s</b> &nbsp;|&nbsp; <span style='color:#000;font-weight:bold'>Mood:</span> <b style='color:#000'>{track['mood']}</b><br>"
                            f"</div>", unsafe_allow_html=True)
                st.image(track['artwork_url'], width=140)
                st.markdown(f"<a href='{track['track_url']}' target='_blank' style='color:#1976d2;font-weight:bold;background:#fff;padding:4px 8px;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,0.08);'>🎧 Listen</a>", unsafe_allow_html=True)
                st.button(f"👍 Like {track['track_name']}", key=track['track_url'])
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("No songs found for this mood in the dataset.")
