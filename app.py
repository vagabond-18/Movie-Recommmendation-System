from fastapi import FastAPI, HTTPException
from backend.model.recommender import (
    recommend_movies,
    explain_recommendation
)

app = FastAPI(
    title="ReelSense Movie Recommendation API",
    description="Hybrid Movie Recommendation System",
    version="1.0"
)

# ===============================
# Health check
# ===============================
@app.get("/")
def health_check():
    return {"status": "API is running"}

# ===============================
# Recommendation endpoint
# ===============================
@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, top_n: int = 10):
    try:
        recommendations = recommend_movies(user_id, top_n)
        return {
            "user_id": user_id,
            "recommendations": recommendations
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ===============================
# Explanation endpoint
# ===============================
@app.get("/explain/{user_id}/{movie_id}")
def explain(user_id: int, movie_id: int):
    try:
        return explain_recommendation(user_id, movie_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))