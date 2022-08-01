import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import logging
import sys
from pprint import pprint


def logger_setup() -> None:
    logging.basicConfig(filename='logfile.log', encoding='utf-8',level=logging.DEBUG)


def read_secrets() -> dict[str,str]: # Returns a dict of all secrets?
    secrets: dict[str,str] = {}

    with open('secrets/secrets.txt','r') as f:
        lines = f.readlines() 

    for line in lines:
        secrets[line[:line.find('=')]]=line[line.find('=')+1:-1]

    return secrets


# Set environment variables using secrets file
def set_env_variables() -> None:
    secrets: dict[str,str] = read_secrets()

    if 'SPOTIPY_CLIENT_ID' in os.environ:
        logging.info('SPOTIPY_CLIENT_ID already set')
    if 'SPOTIPY_CLIENT_ID' not in os.environ:
        os.environ['SPOTIPY_CLIENT_ID']=secrets['SPOTIPY_CLIENT_ID']
        logging.info('Set SPOTIPY_CLIENT_ID')

    if 'SPOTIPY_CLIENT_SECRET' in os.environ:
        logging.info('SPOTIPY_CLIENT_SECRET alreay set')
    if 'SPOTIPY_CLIENT_SECRET' not in os.environ:
        os.environ['SPOTIPY_CLIENT_SECRET']=secrets['SPOTIPY_CLIENT_SECRET']
        logging.info('Set SPOTIPY_CLIENT_SECRET')

    if 'SPOTIPY_REDIRECT_URI' in os.environ:
        logging.info('SPOTIPY_REDIRECT_URI already set')
    if 'SPOTIPY_REDIRECT_URI' not in os.environ:
        os.environ['SPOTIPY_REDIRECT_URI']=secrets['SPOTIPY_REDIRECT_URI']
        logging.info('Set SPOTIPY_REDIRECT_URI')


def get_playlists() -> list[str]:
    # Reads playlist codes from the secrets folder and loads them into a list
    playlists: list[str] = []

    with open('secrets/playlists.txt','r') as f:
        lines = f.readlines() 

        for line in lines:
            playlists.append(line[line.find('=')+1:-1])
    
    return playlists


def get_songs_in_playlist(sp,pl_id):
    offset = 0

    response = sp.playlist_items(pl_id,
                                offset=offset,
                                fields='items.track.id,total',
                                additional_types=['track'])

    return response


def create_total_track_list(sp):
    playlists: list[str] = get_playlists()

    track_ids: list[str] = []
    for playlist in playlists:
        print(playlist)
        response = get_songs_in_playlist(sp,playlist)
        pprint(response['items'])

        for item in response['items']:
            track_ids.append(item['track']['id'])

    return track_ids


def main():
    logger_setup()
    set_env_variables()
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    pprint(create_total_track_list(sp))


if __name__ == "__main__":
    main()
