import os
import logging

def logger_setup() -> None:
    """
    Set up fr logging files.
    """
    
    logging.basicConfig(filename='logfile.log', encoding='utf-8',level=logging.DEBUG)

def read_secrets() -> dict[str,str]:
    """
    Reads the Spotify credentials needed to interact with the API.
    """
    
    secrets: dict[str,str] = {}

    with open('secrets/secrets.txt','r') as f:
        lines = f.readlines() 

    for line in lines:
        secrets[line[:line.find('=')]]=line[line.find('=')+1:-1]

    return secrets

def set_env_variables() -> None:
    """
    Sets environent variables to the required Spotify credentials.
    This is only active for the session and must be run at the beginning of each session.
    """
    
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
