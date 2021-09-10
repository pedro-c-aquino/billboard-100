from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = # Put your client id
CLIENT_SECRET = # Put yout client secret
REDIRECT_URI = # Put your redirect URL

year = input("Which year do you want to? Type a year from 2006 onwards: \n")

response = requests.get(f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs")

soup = BeautifulSoup(response.text, "html.parser")

song_tags = soup.find_all(name="div", class_="ye-chart-item__title")

artist_tags = soup.find_all(name="div", class_="ye-chart-item__artist")

artists = [tag.get_text() for tag in artist_tags]

artists_edited = []
for artist in artists:
    artists_edited.append(artist.replace("\n", ""))

print(artists_edited)

songs = [tag.get_text() for tag in song_tags]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path= # Put your token file
    )
)

user_id = sp.current_user()["id"]
song_uris = []

for i in range(len(songs)):
    result = sp.search(q=f"track:{songs[i]} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{songs[i]} doesn't exist in Spotify. Skipped.")


playlist_id = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)["id"]
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_uris)

