import sys
import os
sys.path.append(os.path.abspath("."))

import streamlit as st
import requests
import sys
import os
import re

# ===============================
# Backend import path
# ===============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "model"))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from recommender import recommend_movies, explain_recommendation
from recommender import movies

# ===============================
# TMDB SETTINGS
# ===============================
TMDB_API_KEY = "8b0644659ee439925802f841961e552a"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
DEFAULT_POSTER = "https://via.placeholder.com/300x450?text=No+Poster"

# ===============================
# Extract Title + Year
# ===============================
def extract_title_year(title):
    match = re.search(r"(.*)\((\d{4})\)", title)
    if match:
        return match.group(1).strip(), match.group(2)
    return title, None

# ===============================
# Poster Fetch
# ===============================
@st.cache_data(show_spinner=False)
def get_movie_poster(title: str) -> str:
    clean_title, year = extract_title_year(title)
    try:
        response = requests.get(
            TMDB_SEARCH_URL,
            params={"api_key": TMDB_API_KEY, "query": clean_title},
            timeout=6
        )
        if response.status_code != 200:
            return DEFAULT_POSTER
        results = response.json().get("results", [])
        if not results:
            return DEFAULT_POSTER
        if year:
            for movie in results:
                if movie.get("release_date", "").startswith(year):
                    if movie.get("poster_path"):
                        return TMDB_IMAGE_BASE + movie["poster_path"]
        for movie in results:
            if movie.get("poster_path"):
                return TMDB_IMAGE_BASE + movie["poster_path"]
        return DEFAULT_POSTER
    except:
        return DEFAULT_POSTER

# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="🎬 ReelSense", layout="wide")

# ===============================
# CSS Styling - Multiple Harmonious Warm Colors
# ===============================
st.markdown("""
<style>
/* App Background */
.stApp { 
    background: linear-gradient(135deg,#fff8e1,#ffe0b2);
    font-family: 'Arial', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#ffd54f,#ffb74d);
    color:white;
}

/* User Card */
.user-card {
    background: linear-gradient(135deg, #ffe082, #ffcc80);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
    backdrop-filter: blur(5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    transition: transform 0.3s, box-shadow 0.3s;
    color: white;
}
.user-card:hover {
    transform: translateY(-5px) scale(1.03);
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
}
.user-card .avatar {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    margin-bottom: 15px;
    border: 3px solid rgba(255,255,255,0.6);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* Name & Subtitle */
.user-card h3 { font-size: 20px; font-weight: 700; }
.user-card p { font-size: 14px; margin: 0; color: #ffffffcc; }

/* Slider & Multiselect */
.stSlider > div > div:nth-child(2) { background: linear-gradient(90deg, #ffb74d, #ffcc80); }
.stMultiSelect > div > div > div { background: rgba(255,255,255,0.1); border-radius: 10px; padding: 5px; }

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#ff8f00,#ffb74d);
    color:white;
    font-weight:700;
    border-radius:12px;
    padding:8px 12px;
    transition:0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

/* Header */
.header-container {
    background: linear-gradient(90deg,#ffb74d,#ff9800);
    padding:25px;
    border-radius:15px;
    margin-bottom:25px;
    color:white;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    text-align: center;
}

/* Recommendation Count Bar */
.recommend-count {
    background: linear-gradient(90deg,#ffe0b2,#ffcc80);
    padding:15px;
    border-radius:12px;
    font-weight:600;
    margin-bottom:20px;
    color:#e65100;
}

/* Movie Cards */
.movie-card {
    background: #fff;
    border-radius:18px;
    padding:15px;
    text-align:center;
    transition:0.3s;
    height:100%;
    box-shadow:0 5px 15px rgba(0,0,0,0.1);
}
.movie-card:hover {
    transform:translateY(-10px) scale(1.03);
    box-shadow:0 15px 40px rgba(255, 167, 38, 0.3); /* yellow-orange glow on hover */
    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
}

/* Movie Info */
.movie-title { font-size:18px; font-weight:700; color:#e65100; margin-top:10px; }
.movie-genres { font-size:13px; font-weight:600; color:#ef6c00; background:#fff3e0; padding:6px 12px; border-radius:10px; display:inline-block; margin-top:5px; }
.movie-rating { font-size:14px; font-weight:600; color:#f57c00; margin-top:5px; }

/* Empty State */
.empty-state {
    text-align:center;
    padding:70px;
    background:#fff9e5;
    border-radius:20px;
    color:#e65100;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# Header
# ===============================
st.markdown("""
<div class="header-container">
<h1>🎬 ReelSense</h1>
<p style="font-weight:600;">Personalized Movie Recommendations</p>
</div>
""", unsafe_allow_html=True)

# ===============================
# Sidebar
# ===============================
with st.sidebar:
    st.markdown(f"""
    <div class="user-card">
        <img class="avatar" src="https://images.unsplash.com/photo-1607082342195-1a0d1b1c7c4c?crop=entropy&cs=tinysrgb&fit=crop&h=80&w=80" alt="Gentle Movie Illustration"/>
        <h3>🎬 Welcome Viewer</h3>
        <p>Discover movies tailored for you</p>
    </div>
    """, unsafe_allow_html=True)

    user_id = st.number_input("👤 User ID", min_value=1, step=1)
    top_n = st.slider("🎯 Number of Recommendations", 5, 20, 10)

    # Genre selection
    all_genres = set()
    for g in movies["genres"]:
        all_genres.update(g.split())

    selected_genres = st.multiselect("🎭 Preferred Genres", sorted(list(all_genres)))

    recommend_button = st.button("✨ Recommend Movies")

# ===============================
# Fetch Recommendations
# ===============================
if recommend_button:
    with st.spinner("Finding best movies for you... 🍿"):
        try:
            recommendations = recommend_movies(
                user_id,
                top_n,
                preferred_genres=selected_genres if selected_genres else None
            )
            st.session_state["recommendations"] = recommendations
            st.session_state["user_id"] = user_id
        except ValueError as e:
            st.error(str(e))

# ===============================
# Empty State UI
# ===============================
if "recommendations" not in st.session_state:
    st.markdown("""
    <div class="empty-state">
        <h2>🍿 Ready for Movie Magic?</h2>
        <p style="font-size:18px;">
        Enter your User ID and click Recommend to get personalized movie picks.
        </p>
        <div style="font-size:70px;">🎞️</div>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# Display Recommendations
# ===============================
if "recommendations" in st.session_state:
    recs = st.session_state["recommendations"]

    st.markdown(f"""
    <div class="recommend-count">
    🔥 Showing {len(recs)} personalized recommendations
    </div>
    """, unsafe_allow_html=True)

    cols_per_row = 4

    for i in range(0, len(recs), cols_per_row):
        row_movies = recs[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for col, movie in zip(cols, row_movies):
            with col:
                poster_url = get_movie_poster(movie["title"])
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                st.image(poster_url, width=200)
                st.markdown(f"<div class='movie-title'>{movie['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='movie-genres'>{movie['genres']}</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='movie-rating'>⭐ Predicted Rating: {movie.get('predicted_rating','N/A')}/5</div>",
                    unsafe_allow_html=True
                )
                if st.button("Why this movie? 🤔", key=f"why_{movie['movieId']}"):
                    explanation = explain_recommendation(
                        st.session_state["user_id"],
                        movie["movieId"]
                    )
                    st.session_state[f"explain_{movie['movieId']}"] = explanation
                if f"explain_{movie['movieId']}" in st.session_state:
                    st.info(st.session_state[f"explain_{movie['movieId']}"])
                st.markdown("</div>", unsafe_allow_html=True)



import streamlit as st
import requests
import re
