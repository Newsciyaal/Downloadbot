import requests
import json

def search_movies(query):
    """Searches for movies and returns a list of search results."""

    url = f"https://api.themoviedb.org/3/search/movie?api_key=YOUR_API_KEY&query={query}"
    response = requests.get(url)
    results = json.loads(response.content)["results"]

    return results

def get_movie(id):
    """Gets the details of a movie."""

    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=YOUR_API_KEY"
    response = requests.get(url)
    movie = json.loads(response.content)

    return movie

def get_movie_poster_url(movie_id):
    """Gets the URL of the movie poster."""

    movie = get_movie(movie_id)
    poster_path = movie["poster_path"]

    if poster_path is not None:
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        poster_url = None

    return poster_url

def get_movie_download_links(movie_id):
    """Gets the download links for the movie."""

    movie = get_movie(movie_id)

    download_links = {}
    for provider in movie["providers"]:
        download_links[provider["name"]] = provider["link"]

    return download_links
