from api_setup import logger_setup, set_env_variables
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
from pprint import pprint 
import re

def delete_playlists():
    logger_setup()
    set_env_variables()

    scope='playlist-modify-private'
    sp_personal = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    response_playlists: list = []

    still_responding: bool = True
    offset_i: int = 0

    while still_responding is True:
        offset = offset_i * 50
        response = sp_personal.current_user_playlists(offset=offset)
        response_playlists = response_playlists + response['items']
        
        if len(response['items']) < 50:
            still_responding == False
            break
        offset_i += 1

    playlist_id_to_delete: list = []
    regex_to_delete: str = '^My Playlist'

    for playlists in response_playlists:
        # if re.match(regex_to_delete, playlists['name']):
        pprint(playlists['name'])
        pprint(playlists['id'])
        playlist_id_to_delete.append(playlists['id'])

    pprint(len(playlist_id_to_delete))

    # for playlist_id in playlist_id_to_delete:
    #     sp_personal.current_user_unfollow_playlist(playlist_id)


if __name__ == "__main__":
    delete_playlists()