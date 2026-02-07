import streamlit as st
from backend.model.recommender import recommend_movies, explain_recommendation

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="centered"
)

st.title("🎬 Movie Recommendation System")
st.write("Get personalized movie recommendations based on user preferences.")

# ======================
# User Inputs
# ======================
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

# ======================
# Recommendation Button
# ======================
if st.button("🎯 Get Recommendations"):
    with st.spinner("Finding the best movies for you..."):
        try:
            movies = recommend_movies(user_id, top_n)

            st.subheader("🍿 Recommended Movies")

            for i, movie in enumerate(movies, 1):
                st.markdown(
                    f"""
                    **{i}. 🎬 {movie['title']}**  
                    *Genres:* {movie['genres']}  
                    ⭐ **Predicted Rating:** {float(movie['predicted_rating']):.2f}
                    """
                )

                if st.button(f"Why recommended? ({movie['movieId']})"):
                    explanation = explain_recommendation(
                        user_id,
                        movie["movieId"]
                    )
                    st.info(explanation)

        except Exception as e:
            st.error(str(e))
