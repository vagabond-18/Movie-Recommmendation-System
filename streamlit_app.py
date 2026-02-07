import streamlit as st
from backend.model.recommender import (
    recommend_movies,
    explain_recommendation
)

# ===============================
# Page config
# ===============================
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="centered"
)

# ===============================
# UI Header
# ===============================
st.title("🎬 Movie Recommendation System")
st.write("Get personalized movie recommendations based on user preferences.")

# ===============================
# User Inputs
# ===============================
user_id = st.number_input(
    "Enter User ID",
    min_value=1,
    step=1,
    value=1
)

top_n = st.slider(
    "Number of recommendations",
    min_value=1,
    max_value=20,
    value=10
)

# ===============================
# Recommendation Button
# ===============================
if st.button("🎯 Get Recommendations"):
    try:
        recommendations = recommend_movies(user_id, top_n)

        if not recommendations:
            st.warning("No recommendations found.")
        else:
            st.subheader("🍿 Recommended Movies")

            for idx, movie in enumerate(recommendations, start=1):
                st.markdown(
                    f"""
**{idx}. 🎬 {movie['title']}**  
Genres: *{movie['genres']}*  
⭐ Predicted Rating: **{round(float(movie['predicted_rating']), 2)}**
"""
                )

                with st.expander("Why was this recommended?"):
                    explanation = explain_recommendation(
                        user_id,
                        movie["movieId"]
                    )
                    st.write(explanation)

    except Exception as e:
        st.error(f"Error: {e}")
