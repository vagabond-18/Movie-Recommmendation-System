import sys
import os

sys.path.append(os.path.abspath("."))
import sys
import os
sys.path.append(os.path.abspath("."))

import streamlit as st
from backend.model.recommender import recommend_movies

st.set_page_config(page_title="Movie Recommendation System")

st.title("🎬 Movie Recommendation System")

user_id = st.number_input("Enter User ID", min_value=1, step=1)
top_n = st.slider("Number of recommendations", 1, 20, 10)

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            movies = recommend_movies(user_id, top_n)

            if not movies:
                st.warning("No recommendations found.")
            else:
                st.subheader("Recommended Movies")
                for i, movie in enumerate(movies, 1):
                    st.write(f"{i}. 🎥 {movie}")

        except Exception as e:
            st.error(f"Error: {e}")
