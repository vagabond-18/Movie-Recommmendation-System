import streamlit as st
from backend.model.recommender import recommend_movies

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.write("Get personalized movie recommendations based on user preferences.")

user_id = st.number_input(
    "Enter User ID",
    min_value=1,
    value=1,
    step=1
)

top_n = st.slider(
    "Number of recommendations",
    min_value=1,
    max_value=20,
    value=10
)

if st.button("Get Recommendations"):
    try:
        recommendations = recommend_movies(user_id, top_n)

        st.subheader("🍿 Recommended Movies")

        for i, movie in enumerate(recommendations, start=1):
            st.markdown(f"""
**{i}. 🎬 {movie['title']}**  
Genres: {movie['genres']}  
⭐ Predicted Rating: {round(float(movie['predicted_rating']), 2)}
""")
    except Exception as e:
        st.error(str(e))
