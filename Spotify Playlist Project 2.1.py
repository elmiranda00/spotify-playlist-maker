import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import youtube_dl
import json

scope = 'playlist-modify-public'
username = "ncurs1n6rkvtfd8trztast5f7"

CLIENT_ID = '00000A'
CLIENT_SECRET = "00000B"

token = SpotifyOAuth(client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=scope,
    redirect_uri="http://www.blankwebsite.com/",
    username=username)

spotifyObj = spotipy.Spotify(auth_manager= token)

urls = []
chat= open(r"C:\Users\Elrich Miranda\Documents\Elrich\Projects- Python\WhatsApp to Spotify playlist 3.0\input\chat_sid_20231028_merged.txt",mode="r",encoding="utf-8").read()
for line in re.findall("https://www.youtube.com/watch\S*|https://open\.spotify\.com/track/\S*|https://youtu\.be\S*",chat):
    if(re.search("youtube.com|youtu.be",line)):
        urls.append(["YouTube",line])
    elif(re.search("spotify.com",line)):
        urls.append(["Spotify",line])

unique_urls = [] 
[unique_urls.append(x) for x in urls if x not in unique_urls] 

spotifyObj.user_playlist_create(username, "202310_test1", False)
getPlaylist = spotifyObj.user_playlists(user= username)
playlist = getPlaylist['items'][0]['id']


for i in range(len(unique_urls)):
    source = unique_urls[i][0] 
    link = unique_urls[i][1]

    if(source=="YouTube"):
        #get YouTube song info
        try:
            video = youtube_dl.YoutubeDL({}).extract_info(link,download= False)
            try:
                song_name = video["track"]
                try:
                    artist = video["artist"]
                except:
                    song_name="Not Found"
                    artist = "Not Found"
            except:
                    song_name="Not Found"
                    artist = "Not Found"
        except:
            song_name="Not Found"
            artist = "Not Found"

        if(song_name != "Not Found" or artist != "Not Found"):
            result = spotifyObj.search(q=song_name+" "+artist)
            uri = result["tracks"]["items"][0]["uri"]
            url = "https://open.spotify.com/track/" + uri.rsplit(":",1)[-1]
            spotifyObj.user_playlist_add_tracks(user= username,playlist_id=playlist,tracks=[url])
           

    if(source=="Spotify"):
        spotifyObj.user_playlist_add_tracks(user= username,playlist_id=playlist,tracks=[link])