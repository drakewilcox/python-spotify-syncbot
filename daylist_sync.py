from log_config import configure_logging 
from utils import formatted_date
from envs import *
from spotify_session import SpotifySession 

app_logger = configure_logging()
sp = SpotifySession(logger=app_logger)

daylist_url = "https://open.spotify.com/playlist/37i9dQZF1EP6YuccBxUcC1?si=6c085d97b51e4ac1"

daylist = sp.playlist(playlist_id=daylist_url)

archive_name = f"{formatted_date()} DAYLIST ARCHIVE"
existing_archive = sp.search_playlists_by_name(query=archive_name)

if existing_archive:
  sp.transfer_songs_to_archive(from_playlist=daylist, to_playlist=existing_archive)
else:
  new_archive = sp.user_playlist_create(user=sp.current_user_id, name=archive_name, public=False, is_daylist=True)
  sp.transfer_songs_to_archive(from_playlist=daylist, to_playlist=new_archive, is_new_archive=True, is_daylist=True)
