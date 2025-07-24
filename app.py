import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=bb776064268add4dc30badbb488892ee&language=en-US'
    response = requests.get(url)
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  # fallback image


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]

    recommend_movies = []

    recommend_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]]['movie_id']

        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

option = st.selectbox(
    "how would you like to learn more?",
    movies['title'].values)

if st.button('Recommend'):
     name, posters = recommend(option)

     col1, col2 , col3, col4, col5= st.columns(5)
     with col1:
         st.text(name[0])
         st.image(posters[0])
     with col2:
         st.text(name[1])
         st.image(posters[1])
     with col3:
         st.text(name[2])
         st.image(posters[2])
     with col4:
         st.text(name[3])
         st.image(posters[3])
     with col5:
         st.text(name[4])
         st.image(posters[4])

