import pickle
import streamlit as st
import requests
import numpy as np


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=709a683f3a611b9db3d621bde969bca9&lenguage=en-US".format(movie_id)
    # print(movie_id);
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:19]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)

    for i in range(0, 18, 3):
        columns = st.columns(3)
        for j in range(3):
            if i + j < 18:
                columns[j].text(recommended_movie_names[i+j])
                columns[j].image(recommended_movie_posters[i+j])