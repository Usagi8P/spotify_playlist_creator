import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from api_setup import logger_setup, set_env_variables


def get_playlists() -> list[str]:
    # Reads playlist codes from the secrets folder and loads them into a list
    playlists: list[str] = []

    with open('secrets/playlists.txt','r') as f:
        lines = f.readlines() 

        for line in lines:
            playlist_id = line[line.find('=')+1:-1]
            if playlist_id:
                playlists.append(playlist_id)
    
    return playlists


def get_songs_in_playlist(sp,pl_id):
    offset = 0

    response = sp.playlist_items(pl_id,
                                offset=offset,
                                fields='items.track.id,total',
                                additional_types=['track'])

    return response


def create_total_track_list(sp) -> list[str]:
    playlists: list[str] = get_playlists()

    track_ids: list[str] = []
    for playlist in playlists:
        response = get_songs_in_playlist(sp,playlist)

        for item in response['items']:
            track_ids.append(item['track']['id'])

    return track_ids


def create_new_playlist(sp_personal) -> str:
    with open('secrets/username.txt','r') as f:
        username = f.readline()

    new_playlist = sp_personal.user_playlist_create(username,'Full Playlist')
    
    with open('secrets/playlist_id.txt','w') as f:
        f.write(new_playlist['id'])

    return new_playlist['id']


def get_new_playlist_id(sp_personal) -> str:
    try:
        with open('secrets/playlist_id.txt','r') as f:
            playlist_id = f.readline()

            if playlist_id:
                return playlist_id

            if not playlist_id:
                return create_new_playlist(sp_personal)

    except:
        return create_new_playlist(sp_personal)


def main():
    logger_setup()
    set_env_variables()
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope='playlist-modify-public'
    sp_personal = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    tracklist = (create_total_track_list(sp))
    set_tracklist = set(tracklist)

    new_playlist_id = get_new_playlist_id(sp_personal)

    final_tracklist = list(set_tracklist)
    n_tracks = len(final_tracklist)
    
    if n_tracks <= 100:
        sp_personal.playlist_replace_items(new_playlist_id,final_tracklist)
    else:
        uploaded_tracks: int = 0
        sp_personal.playlist_replace_items(new_playlist_id,final_tracklist[uploaded_tracks:uploaded_tracks+99])
        uploaded_tracks += 99

        while uploaded_tracks + 99 <= n_tracks - 1:
            sp_personal.playlist_add_items(new_playlist_id,final_tracklist[uploaded_tracks:uploaded_tracks+99])
            uploaded_tracks += 99
        
        if uploaded_tracks < n_tracks - 1:
            sp_personal.playlist_add_items(new_playlist_id,final_tracklist[uploaded_tracks:n_tracks-1])



if __name__ == "__main__":
    main()
