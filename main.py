import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from transfers import TRANSFERS

from envs import *
from spotipy_utils import get_playlist_track_uris, batch_tracks
from log_config import configure_logging

# CONFIGURE LOGGING:
appLogger = configure_logging()

# SPOTIFY OAUTH: 
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

# TRANSFER LOGIC

# appLogger.info(f"Starting Playlist Sync for {len(TRANSFERS)} Playlists")

for transfer in TRANSFERS: 
  to_id = transfer["to_playlist_link"]
  from_id = transfer["from_playlist_link"]
  from_uris = get_playlist_track_uris(sp, from_id)
  to_uris = get_playlist_track_uris(sp, to_id)
  new_uris = [uri for uri in from_uris if uri not in set(to_uris)]



  if new_uris:
    batch_tracks(sp, to_id, new_uris)
    new_description = f"Automated Archive of the {transfer['from_playlist_name']} playlist. Last Sync: {formatted_date}"
    sp.playlist_change_details(playlist_id=to_id, description=new_description)

    log_message = f"{formatted_date}: Synced {transfer['from_playlist_name']} to {transfer['to_playlist_name']}\n"

    appLogger.info(log_message)
