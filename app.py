import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown
import tempfile

st.set_page_config(page_title="Movie Recommendation System")

API_KEY = "b241488de441b6137b80562ec762b4ca"


# Google Drive file ID for similarity.pkl
similarity_file_id = "1YE37mlwbvU0FU6d4XX98kOsI2Gk2OE-H"

# Function to download and load similarity.pkl from Google Drive
def load_similarity_from_drive(file_id):
    # Create a temporary directory for the download
    temp_dir = tempfile.mkdtemp()  # This will create a unique temporary directory
    temp_file_path = os.path.join(temp_dir, "similarity.pkl")

    # Clean up any leftover .part files from previous downloads
    if os.path.exists(f"{temp_file_path}.part"):
        os.remove(f"{temp_file_path}.part")

    # Download the file from Google Drive
    print("Downloading similarity.pkl from Google Drive...")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, temp_file_path, quiet=False)
    print("similarity.pkl downloaded successfully!")

    # Load the pickle file into memory
    with open(temp_file_path, 'rb') as file:
        similarity = pd.read_pickle(file)

    # Optionally, remove the temporary directory after loading
    os.remove(temp_file_path)
    os.rmdir(temp_dir)

    return similarity


# Load the similarity file from Google Drive
similarity = load_similarity_from_drive(similarity_file_id)


print("Movies and similarity data loaded successfully!")




movie_file_path = "movie.pkl"

with open(movie_file_path, 'rb') as file:
    movies = pd.read_pickle(file)
    
movie_list = movies['title'].values






def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b241488de441b6137b80562ec762b4ca&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return None


def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distance = similarity[movie_index]
    movielist = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:7]
    suggested_movies = []
    suggested_movies_posters = []
    for i in movielist:
        suggested_movies.append(movies.iloc[i[0]].title)
        id = movies.iloc[i[0]].id
        suggested_movies_posters.append(fetch_poster(id))
    return suggested_movies, suggested_movies_posters


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['results']
        return [(movie['title'], movie['id']) for movie in data[:6]]
    return []


# Trending and Popular Movies Section
st.header("Trending Movies")
trending_movies = fetch_trending_movies()

cols = st.columns(6)
for idx, (title, movie_id) in enumerate(trending_movies):
    with cols[idx % 6]:  # Arrange six posters per row
        st.image(fetch_poster(movie_id), use_column_width='auto')  # Adjust for mobile width


st.divider()

# Streamlit app
st.title('Movie Recommendation')

selected_movie = st.selectbox('Select Movie Name', movie_list)

if selected_movie:
    movie_id = movies[movies['title'] == selected_movie].id.values[0]
    movie_details = fetch_movie_details(movie_id)

    if movie_details:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(fetch_poster(movie_id), use_column_width=True)

        with col2:
            st.header(movie_details['title'])
            st.write(f"**Overview:** {movie_details['overview']}")
            st.write(f"**Release Date:** {movie_details['release_date']}")
            st.write(f"**Rating:** {movie_details['vote_average']}")
            st.write(f"**Genres:** {', '.join(genre['name'] for genre in movie_details['genres'])}")


        if st.button('Recommend'):
            names, posters = recommend(selected_movie)
            num_movies = len(names)

            # Display recommended movies with responsiveness
            for i in range(0, num_movies, 3):
                if num_movies <= 3:
                    cols = st.columns(2)  # For smaller screens, show 2 columns per row
                else:
                    cols = st.columns(3)  # For larger screens, show 3 columns per row
                
                for j in range(3):
                    if i + j < num_movies:
                        with cols[j]:
                            st.image(posters[i + j], use_column_width='auto')  # Adjust image size automatically
                            st.write(names[i + j])

