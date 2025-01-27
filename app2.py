import pickle
import gzip
import requests
import streamlit as st
from io import BytesIO

# GitHub raw file URL (replace with your URL)
COMPRESSED_FILE_URL = "https://raw.githubusercontent.com/Ayan-Mahato/movierecommendation/main/similarity.pkl.gz"

def fetch_and_load_compressed_file(url):
    # Fetch the compressed file
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Decompress the file and load with pickle
    with gzip.GzipFile(fileobj=BytesIO(response.content)) as f:
        data = pickle.load(f)
    return data

# Fetch similarity data
similarity = fetch_and_load_compressed_file(COMPRESSED_FILE_URL)

# Load movies.pkl
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Movie Recommender System Code
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3e04b1cc3dc39ceff4fbc47c4de177d6&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Streamlit Interface
st.header('Movie Recommender System')
st.subheader('Minor project by Ayan Mahato')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])