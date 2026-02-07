# # import pickle
# # import os
# #
# # # ===============================
# # # Load artifacts
# # # ===============================
# # MODEL_PATH = os.path.join(os.path.dirname(__file__), "recommender.pkl")
# #
# # with open(MODEL_PATH, "rb") as f:
# #     artifacts = pickle.load(f)
# #
# # predicted_df = artifacts["predicted_df"]
# # hybrid_scores = artifacts["hybrid_scores"]
# # movies = artifacts["movies"]
# # popularity_dict = artifacts["popularity_dict"]
# #
# # print("✅ Recommender artifacts loaded successfully")
# #
# # # ===============================
# # # Recommendation function
# # # ===============================
# # def recommend_movies(user_id, top_n=10):
# #     """
# #     Returns top-N movie recommendations for a given user
# #     """
# #     if user_id not in hybrid_scores.index:
# #         raise ValueError("User ID not found")
# #
# #     user_scores = hybrid_scores.loc[user_id].sort_values(ascending=False)
# #     top_movies = user_scores.head(top_n).index.tolist()
# #
# #     recommendations = (
# #         movies[movies["movieId"].isin(top_movies)]
# #         [["movieId", "title", "genres"]]
# #         .head(top_n)
# #     )
# #
# #     return recommendations.to_dict(orient="records")
# #
# #
# # # ===============================
# # # Explain function (dummy example)
# # # ===============================
# # def explain_recommendation(user_id, movie_id):
# #     """
# #     Returns a simple explanation string for why the movie is recommended
# #     """
# #     movie_row = movies[movies["movieId"] == movie_id]
# #     genres = movie_row["genres"].values[0] if not movie_row.empty else ""
# #     return f"This movie is recommended based on your taste in genres: {genres}"
#
#
# import pickle
# import os
# import pandas as pd
#
# # ===============================
# # Load artifacts
# # ===============================
# MODEL_PATH = os.path.join(os.path.dirname(__file__), "recommender.pkl")
#
# with open(MODEL_PATH, "rb") as f:
#     artifacts = pickle.load(f)
#
# predicted_df = artifacts["predicted_df"]
# hybrid_scores = artifacts["hybrid_scores"]
# movies = artifacts["movies"]
# popularity_dict = artifacts["popularity_dict"]
#
# print("✅ Recommender artifacts loaded successfully")
#
# # ===============================
# # Recommendation function
# # ===============================
# def recommend_movies(user_id, top_n=10):
#     """
#     Returns top-N movie recommendations for a given user
#     """
#     if user_id not in hybrid_scores.index:
#         raise ValueError(f"User ID {user_id} not found")
#
#     user_scores = hybrid_scores.loc[user_id].sort_values(ascending=False)
#     top_movies = user_scores.head(top_n).index.tolist()
#
#     recommendations = []
#     for movie_id in top_movies:
#         movie_row = movies[movies["movieId"] == movie_id]
#         if movie_row.empty:
#             continue
#         movie_info = movie_row.iloc[0]
#         recommendations.append({
#             "movieId": movie_id,
#             "title": movie_info["title"],
#             "genres": movie_info["genres"],
#             "predicted_rating": round(user_scores[movie_id], 2)
#         })
#
#     return recommendations
#
# # ===============================
# # Explain function (dummy example)
# # ===============================
# def explain_recommendation(user_id, movie_id):
#     """
#     Returns a simple explanation string for why the movie is recommended
#     """
#     movie_row = movies[movies["movieId"] == movie_id]
#     genres = movie_row["genres"].values[0] if not movie_row.empty else ""
#     return f"This movie is recommended based on your taste in genres: {genres}"


import pickle
import os

# ===============================
# Load artifacts
# ===============================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "recommender.pkl")

with open(MODEL_PATH, "rb") as f:
    artifacts = pickle.load(f)

predicted_df = artifacts["predicted_df"]
hybrid_scores = artifacts["hybrid_scores"]
movies = artifacts["movies"]
popularity_dict = artifacts["popularity_dict"]

print("✅ Recommender artifacts loaded successfully")


# ===============================
# Recommendation function
# ===============================
def recommend_movies(user_id, top_n=10, preferred_genres=None):
    """
    Returns top-N movie recommendations for a given user.
    Optionally filters by preferred genres.
    """
    if user_id not in hybrid_scores.index:
        raise ValueError(f"User ID {user_id} not found")

    user_scores = hybrid_scores.loc[user_id].sort_values(ascending=False)
    top_movies = user_scores.index.tolist()

    recommendations = []
    for movie_id in top_movies:
        movie_row = movies[movies["movieId"] == movie_id]
        if movie_row.empty:
            continue
        movie_info = movie_row.iloc[0]

        # Filter by selected genres
        if preferred_genres:
            movie_genres = set(movie_info["genres"].split())
            if not movie_genres.intersection(set(preferred_genres)):
                continue

        recommendations.append({
            "movieId": movie_id,
            "title": movie_info["title"],
            "genres": movie_info["genres"],
            "predicted_rating": round(user_scores[movie_id], 2)
        })

        if len(recommendations) >= top_n:
            break

    return recommendations


# ===============================
# Explain function
# ===============================
def explain_recommendation(user_id, movie_id):
    """
    Returns explanation string for a recommended movie
    """
    movie_row = movies[movies["movieId"] == movie_id]
    genres = movie_row["genres"].values[0] if not movie_row.empty else ""
    rating = None
    if user_id in predicted_df.index and movie_id in predicted_df.columns:
        rating = round(predicted_df.loc[user_id, movie_id], 2)
    explanation = f"This movie is recommended based on your taste in genres: {genres}."
    if rating:
        explanation += f" Predicted rating for you: {rating}/5."
    return explanation