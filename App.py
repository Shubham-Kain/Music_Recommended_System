
import spotipy
import pickle
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "3c492ee711e041a4843d80aef6826eed"
client_secret = "673ef8374083419e8782ee61c67777fc"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    result= sp.search(q=search_query,type='track')

    if result and result["tracks"]["items"]:
        track = result["tracks"]["items"][0]
        album_cover_url = track["album"]['images'][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png"

def recommend(song):
    index = music[music["song"] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_music_name = []
    recommend_music_poster = []
    for i in distances[1:6]:
        artist =  music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommend_music_poster.append(get_song_album_cover_url(music.iloc[i[0]].song,artist))
        recommend_music_name.append(music.iloc[i[0]].song)

    return recommend_music_name, recommend_music_poster


st.header('Music Recommender System')
music = pickle.load(open('Music_recommender.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
music_list = music['song'].values
selected_music = st.selectbox("Type or Select a song from the dropdown",music_list)
if st.button("Show Recommendation"):
    recommend_music_name,recommend_music_poster = recommend(selected_music)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommend_music_name[0])
        st.image(recommend_music_poster[0])
    with col2:
        st.text(recommend_music_name[1])
        st.image(recommend_music_poster[1])
    with col3:
        st.text(recommend_music_name[2])
        st.image(recommend_music_poster[2])
    with col4:
        st.text(recommend_music_name[3])
        st.image(recommend_music_poster[3])
    with col5:
        st.text(recommend_music_name[4])
        st.image(recommend_music_poster[4])