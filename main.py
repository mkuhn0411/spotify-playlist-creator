import requests
from datetime import date
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_playlist(sp, user_id, song_uris, date):
    playlist = sp.user_playlist_create(user=user_id, name=f"Top Hits from {date}", public=False, collaborative=False, description='Udemy Course')
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


def find_songs(songs, sp):
    song_uris = []

    for song, artist in songs.items():
        try:
            result = sp.search(q=f"track:{song} artist:{artist}", type="track")
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except:
            pass

    return song_uris


def authenticate_spotify(songs, date_chosen):
    CLIENT_ID_SPOTIFY = "xxx"
    CLIENT_SECRET_SPOTIFY = "xxx"
    URL_REDIRECT = "http://example.com"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID_SPOTIFY,
                                                   client_secret=CLIENT_SECRET_SPOTIFY,
                                                   redirect_uri=URL_REDIRECT,
                                                   scope="playlist-modify-private",
                                                   cache_path="token.txt"))
    user_id = sp.current_user()["id"]
    song_uris = find_songs(songs, sp)
    create_playlist(sp, user_id, song_uris, date_chosen)


def get_song_data(date_chosen):
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_chosen}")
    webpage = response.text
    soup = BeautifulSoup(webpage, "html.parser")

    song_elements = [element for element in soup.select(".o-chart-results-list__item") if len(element.select("h3")) > 0 and len(element.select(".u-max-width-330")) > 0]
    song_data = {song.select_one("#title-of-a-story").getText().strip(): song.select_one("span.u-max-width-330").getText().strip() for song in song_elements}
    authenticate_spotify(song_data, date_chosen)


def validate_date(arrival_date):
    is_valid = True

    try:
        date(*map(int, arrival_date.split("-")))
    except ValueError:
        is_valid = False

    return is_valid


def get_date():
    user_date = input("Which year do you want to travel to? Type in this format YYYY-MM-DD: ")

    if validate_date(user_date):
        get_song_data(user_date)
    else:
        print("Please enter a valid date")
        get_date()


def run():
    get_date()


run()