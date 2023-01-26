import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image



movies = pickle.load(open("movie.pkl", 'rb'))
snake = pickle.load(open("similarity.pkl", 'rb'))

m_list = movies['title'].values


def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{"
                            "}?api_key=b241488de441b6137b80562ec762b4ca&language=en-US".format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(name):
    movie_index = movies[movies['title'] == name].index[0]
    distance = snake[movie_index]

    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:7]

    temp = []
    movie_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        temp.append(movies.iloc[i[0]].title)
        # fetch poster
        movie_poster.append(fetch_poster(movie_id))

    return temp, movie_poster

#POSTER
poster = Image.open('poster.png')
st.image(poster)

abhiram = f'<a  href="https://github.com/Abhiram-Laha">Developed by Abhiram Laha </a>'
st.markdown(abhiram, unsafe_allow_html=True)



st.header('Discover Movies You Like')
st.write('#')

selected_movie = st.selectbox(
    'Select the Movie : ', m_list
)

if st.button('Show Recommendation'):
    names, poster = recommend(selected_movie)

    st.write('#')



    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(poster[0])
        st.text(names[0])
    with col2:
        st.image(poster[1])
        st.text(names[1])
    with col3:
        st.image(poster[2])
        st.text(names[2])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(poster[3])
        st.text(names[3])
    with col2:
        st.image(poster[4])
        st.text(names[4])
    with col3:
        st.image(poster[5])
        st.text(names[5])




hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




