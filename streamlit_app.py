import streamlit as st
from backend.model.recommender import recommend_movies

st.set_page_config(page_title="Movie Recommendation System")

st.title("🎬 Movie Recommendation System")

st.success("Streamlit is running successfully!")
st.info("Health check passed ✅")

st.divider()

# =====================
# User input
# =====================
user_id = st.number_input(
    "Enter User ID",
    min_value=1,
    step=1
)

top_n = st.slider(
    "Number of recommendations",
    min_value=1,
    max_value=20,
    value=10
)

# =====================
# Button
# =====================
if st.button("Get Recommendations"):
    try:
        recommendations = recommend_movies(user_id, top_n)

        st.subheader("🎥 Recommended Movies")
        for i, movie in enumerate(recommendations, start=1):
            st.write(f"{i}. {movie}")

    except Exception as e:
        st.error(str(e))
