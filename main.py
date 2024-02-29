import spotipy
import spotipy.util as util 
from spotipy.oauth2 import SpotifyOAuth
import datetime
from transfers import TRANSFERS
from dotenv import load_dotenv
import os 

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI= os.getenv('REDIRECT_URI')

token = util.prompt_for_user_token(
  scope="playlist-modify-public playlist-modify-private",
  redirect_uri=REDIRECT_URI,
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET
)

def get_playlist_track_uris(playlist_id):

  results = sp.playlist_tracks(playlist_id=playlist_id, fields="items,next", limit=100)
  tracks = results["items"]

  print(results["next"])

  while results["next"]:
    results = sp.next(results)
    tracks.extend(results["items"])

  return [track["track"]["uri"] for track in tracks]

sp = spotipy.Spotify(auth=token)
current_date = datetime.now()
formatted_date = current_date.strftime("%m/%d/%Y")

for transfer in TRANSFERS: 
  to_id = transfer["to_playlist_link"]
  from_id = transfer["from_playlist_link"]
  from_uris = get_playlist_track_uris(from_id)
  to_uris = get_playlist_track_uris(to_id)
  new_uris = [uri for uri in from_uris if uri not in set(to_uris)]
  if new_uris:
    sp.playlist_add_items(playlist_id=to_id, items=new_uris)
    new_description=f"Automated Archive of the {transfer["from_playlist_name"]} playlist. Last Sync: {formatted_date}"
    sp.playlist_change_details(playlist_id=to_id, description=new_description)
