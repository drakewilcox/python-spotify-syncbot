import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from transfers import TRANSFERS

from envs import *

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logFile = 'sync_log.txt'
logHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
logHandler.setFormatter(log_formatter)
logHandler.setLevel(logging.INFO)

appLogger = logging.getLogger('root')
appLogger.setLevel(logging.INFO)
appLogger.addHandler(logHandler)

# SPOTIFY AUTH
spotify_auth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPES,
)

token = spotify_auth.refresh_access_token(REFRESH_TOKEN)
access_token = token["access_token"]
sp = spotipy.Spotify(auth=access_token)

current_date = datetime.now()
formatted_date = current_date.strftime("%m/%d/%Y")

def get_playlist_track_uris(playlist_id):

  results = sp.playlist_tracks(playlist_id=playlist_id, fields="items,next", limit=100)
  tracks = results["items"]

  print(results["next"])

  while results["next"]:
    results = sp.next(results)
    tracks.extend(results["items"])

  return [track["track"]["uri"] for track in tracks]

def batch_tracks(sp, playlist_id, track_uris, batch_size=100): 
  for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i+batch_size]
        sp.playlist_add_items(playlist_id=playlist_id, items=batch)



appLogger.info(f"Starting Playlist Sync for {len(TRANSFERS)} Playlists")

for transfer in TRANSFERS: 
  to_id = transfer["to_playlist_link"]
  from_id = transfer["from_playlist_link"]
  from_uris = get_playlist_track_uris(from_id)
  to_uris = get_playlist_track_uris(to_id)
  new_uris = [uri for uri in from_uris if uri not in set(to_uris)]
  
  if new_uris:
    batch_tracks(sp, to_id, new_uris)
    new_description=f"Automated Archive of the {transfer["from_playlist_name"]} playlist. Last Sync: {formatted_date}"
    sp.playlist_change_details(playlist_id=to_id, description=new_description)

    log_message = f"{formatted_date}: Synced {transfer['from_playlist_name']} to {transfer['to_playlist_name']}\n"

    appLogger.info(log_message)
