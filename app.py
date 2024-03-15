import streamlit as st
import requests
import pandas as pd
import random
import pickle
from requests.exceptions import ConnectionError, HTTPError


similarity_dataframe=pickle.load(open('similarity_dataframe.pkl', 'rb'))

def fetch_poster(movie_id, retries=3):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                # Use a placeholder image if poster_path is None or empty
                full_path = "https://placehold.co/500x750"  # 500x750 is an example size
            return full_path
        except (ConnectionError, HTTPError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt == retries:
                # Return a placeholder image after the final attempt
                return "https://placehold.co/500x750"


def recommend(movie_title):
    # Find the id of the movie with the given title
    movie_id = similarity_dataframe[similarity_dataframe['title'] == movie_title]['id'].iloc[0]
    
    # Find similar movies based on the movie_id
    similar_movie_ids = similarity_dataframe[similarity_dataframe['id'] == movie_id]['similar'].iloc[0]
    random.shuffle(similar_movie_ids)
    
    related_movies = []

    for id in similar_movie_ids:
        related_movies.append({'title':similarity_dataframe[similarity_dataframe['id']==id]['title'].iloc[0], 'ratings':similarity_dataframe[similarity_dataframe['id']==id]['vote_average'].iloc[0], 'poster':fetch_poster(id)})
    
    return related_movies


st.title('Recommendation System Testing')
st.write("Content based recommendation system for DeFlix")
movie_name=st.selectbox("Find Similar Movies for", similarity_dataframe['title'].values)

if st.button('Recommend'):
        recommendations = recommend(movie_name)

        st.subheader("Movies related to {}".format(movie_name))
        
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.image(recommendations[0]['poster'])
            st.write(recommendations[0]['title'])
            st.text(recommendations[0]['ratings'])

        with col2:
            st.image(recommendations[1]['poster'])
            st.write(recommendations[1]['title'])
            st.text(recommendations[1]['ratings'])

        with col3:
            st.image(recommendations[2]['poster'])
            st.write(recommendations[2]['title'])
            st.text(recommendations[2]['ratings'])
        
        with col4:
            st.image(recommendations[3]['poster'])
            st.write(recommendations[3]['title'])
            st.text(recommendations[3]['ratings'])
        
        with col5:
            st.image(recommendations[4]['poster'])
            st.write(recommendations[4]['title'])
            st.text(recommendations[4]['ratings'])

        
        col6, col7, col8, col9, col10 = st.columns(5)

        with col6:
            st.image(recommendations[5]['poster'])
            st.write(recommendations[5]['title'])
            st.text(recommendations[5]['ratings'])

        with col7:
            st.image(recommendations[6]['poster'])
            st.write(recommendations[6]['title'])
            st.text(recommendations[6]['ratings'])    
        
        with col8:
            st.image(recommendations[7]['poster'])
            st.write(recommendations[7]['title'])
            st.text(recommendations[7]['ratings'])

        with col9:
            st.image(recommendations[8]['poster'])
            st.write(recommendations[8]['title'])
            st.text(recommendations[8]['ratings'])
        
        with col10:
            st.image(recommendations[9]['poster'])
            st.write(recommendations[9]['title'])
            st.text(recommendations[9]['ratings'])