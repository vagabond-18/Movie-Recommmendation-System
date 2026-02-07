import requests
from streamlit import cache_data

TMDB_API_KEY = "8b0644659ee439925802f841961e552a"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# ===============================
# Cached TMDB poster fetch
# ===============================
@cache_data(show_spinner=False)
def get_movie_poster(title: str):
    """
    Fetch poster URL from TMDB using movie title.
    Uses Streamlit cache to avoid repeated API calls.

    Returns:
        str: Full poster URL or None if not found
    """
    try:
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title
        }

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        # Get first result
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return IMAGE_BASE_URL + poster_path

        return None  # No poster found

    except Exception as e:
        print(f"TMDB API error for '{title}': {e}")
        return None