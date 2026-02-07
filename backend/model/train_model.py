import pandas as pd
import numpy as np
import pickle
from scipy.sparse.linalg import svds
import os

# ===============================
# Paths
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # backend/model
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")                # data folder

# ===============================
# Load Data
# ===============================
movies = pd.read_csv(os.path.join(DATA_DIR, "movies.csv"))
ratings = pd.read_csv(os.path.join(DATA_DIR, "ratings.csv"))
tags = pd.read_csv(os.path.join(DATA_DIR, "tags.csv"))

# ===============================
# Preprocessing
# ===============================
ratings["timestamp"] = pd.to_datetime(ratings["timestamp"], unit="s")
tags["timestamp"] = pd.to_datetime(tags["timestamp"], unit="s")

ratings.drop_duplicates(inplace=True)
movies.drop_duplicates(inplace=True)
tags.drop_duplicates(inplace=True)

movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)

tags["tag"] = (
    tags["tag"]
    .str.lower()
    .str.strip()
    .str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)
)

# keep common tags only
tag_counts = tags["tag"].value_counts()
common_tags = tag_counts[tag_counts >= 5].index
tags = tags[tags["tag"].isin(common_tags)]

movie_tags = tags.groupby("movieId")["tag"].apply(lambda x: " ".join(x)).reset_index()
movies = movies.merge(movie_tags, on="movieId", how="left")
movies["tag"] = movies["tag"].fillna("")
movies["content"] = movies["genres"] + " " + movies["tag"]

# ===============================
# Filter users & movies
# ===============================
user_counts = ratings["userId"].value_counts()
active_users = user_counts[user_counts >= 5].index
ratings = ratings[ratings["userId"].isin(active_users)]

movie_counts = ratings["movieId"].value_counts()
popular_movies = movie_counts[movie_counts >= 5].index
ratings = ratings[ratings["movieId"].isin(popular_movies)]

# ===============================
# Train / Test split (time-based)
# ===============================
ratings = ratings.sort_values("timestamp")
train = ratings.groupby("userId").head(-1)
test = ratings.groupby("userId").tail(1)

# ===============================
# Popularity model
# ===============================
popularity_model = (
    train.groupby("movieId")["rating"]
    .mean()
    .reset_index()
)

popularity_dict = dict(
    zip(popularity_model.movieId, popularity_model.rating)
)

# ===============================
# Collaborative Filtering (SVD)
# ===============================
user_movie_matrix = train.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
)

user_means = user_movie_matrix.mean(axis=1)
matrix = user_movie_matrix.sub(user_means, axis=0).fillna(0)

U, sigma, Vt = svds(matrix.values, k=50)
sigma = np.diag(sigma)

predicted_ratings = np.dot(np.dot(U, sigma), Vt)
predicted_ratings += user_means.values.reshape(-1, 1)

predicted_df = pd.DataFrame(
    predicted_ratings,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.columns
)

# ===============================
# Hybrid Model
# ===============================
hybrid_scores = predicted_df.copy()

for movie_id in hybrid_scores.columns:
    pop_score = popularity_dict.get(movie_id, 0)
    hybrid_scores[movie_id] = (
        0.7 * hybrid_scores[movie_id] + 0.3 * pop_score
    )

# ===============================
# Save artifacts
# ===============================
artifacts = {
    "predicted_df": predicted_df,
    "hybrid_scores": hybrid_scores,
    "movies": movies,
    "popularity_dict": popularity_dict
}

MODEL_PATH = os.path.join(BASE_DIR, "recommender.pkl")  # <- Save here directly

with open(MODEL_PATH, "wb") as f:
    pickle.dump(artifacts, f)

print("✅ Model training complete. Artifacts saved to:", MODEL_PATH)