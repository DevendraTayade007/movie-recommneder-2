import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# 🔹 Helper: download file if missing
def download_file(file_id, output):
    if not os.path.exists(output):
        with st.spinner(f"Downloading {output} ..."):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# 🔹 Download required files
download_file("1_Ku5FTHIldn4CRS9-46ijfhOqWh8l5_M", "similarity.pkl")
download_file("YOUR_MOVIE_DICT_FILE_ID", "movie_dict.pkl")

# 🔹 Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔹 Fetch poster from OMDb
def fetch_poster(movie_title):
    api_key = "a98f5a39"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
    return None

# 🔹 Recommend movies
def recommend(movie, num_recommendations=5):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# ============ STREAMLIT UI ============ #
# 🎨 Page setup
st.set_page_config(page_title="Movie Recommender 🎬", page_icon="🎥", layout="wide")

# 🎬 Title
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>
        🎬 Movie Recommender System
    </h1>
    <p style='text-align: center; color: #AAAAAA;'>
        Discover movies similar to your favorites 📽️🍿
    </p>
    """,
    unsafe_allow_html=True
)

# 🎥 Movie selection
selected_movie_name = st.selectbox("🔍 Choose a Movie", movies['title'].values)

# 📌 Dropdown for recommendations
num_recs = st.selectbox("✨ Number of recommendations", list(range(1, 11)), index=4)

# 🔘 Button
if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie_name, num_recs)

    st.markdown("---")
    st.subheader("🎯 Top Recommendations")

    # 🎨 Card-like layout
    cols = st.columns(3)
    for idx, movie in enumerate(recommendations):
        poster = fetch_poster(movie)
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style='
                    background-color: #222;
                    border-radius: 15px;
                    padding: 15px;
                    text-align: center;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
                    margin-bottom: 20px;
                '>
                    <img src="{poster if poster else 'https://via.placeholder.com/200x300?text=No+Poster'}" 
                         style='width: 180px; border-radius: 10px; margin-bottom: 10px;'>
                    <h4 style='color: #FFDD00;'>{movie}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )
