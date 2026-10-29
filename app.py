import streamlit as st
import pandas as pd
import pickle
import requests

# --- CONFIGURATION & API KEY ---
# Replace with your actual TMDB API key to enable movie posters
TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"


import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def main():
    # Page configuration
    st.set_page_config(
        page_title="Movie Recommender",
        page_icon="🎬",
        layout="wide"
    )

    # Styling for a cleaner look
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #ff4b4b;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🎬 Movie Recommender System")
    st.markdown("Get personalized movie suggestions based on your favorite films.")

    # Load pre-computed pickle files
    try:
        movie_list = pickle.load(open('movie_list.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
    except FileNotFoundError:
        st.error("Critical Error: 'movie_list.pkl' or 'similarity.pkl' not found in the project folder.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        st.stop()

    # User Interface
    st.subheader("Search for a movie")
    movie_titles = movie_list['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_titles)

    if st.button("Show Recommendation"):
        # Get index of selected movie
        movie_index = movie_list[movie_list['title'] == selected_movie].index[0]

        # Get similarity scores
        distances = similarity[movie_index]

        # Sort and get top 5 similar movies (excluding itself)
        movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        st.markdown("---")
        st.subheader("Recommended for you:")

        # Create 5 columns for the posters
        cols = st.columns(5)

        for i, (idx, dist) in enumerate(movie_indices):
            movie_id = movie_list.iloc[idx].movie_id
            title = movie_list.iloc[idx].title
            poster = fetch_poster(movie_id)

            with cols[i]:
                st.image(poster)
                st.markdown(f"**{title}**")

if __name__ == "__main__":
    main()
