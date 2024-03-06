from transfers import TRANSFERS, DAYLIST
from spotify_session import SpotifySession 
from log_config import configure_logging
from utils import formatted_date

app_logger = configure_logging()
sp = SpotifySession(logger=app_logger)

# DAYLIST SYNC 
if DAYLIST["sync_on"]:
  daylist = sp.playlist(playlist_id=DAYLIST["link"])

  archive_name = f"{formatted_date()} DAYLIST ARCHIVE"
  existing_archive = sp.search_playlists_by_name(query=archive_name)

  if existing_archive:
    sp.transfer_songs_to_archive(from_playlist=daylist, to_playlist=existing_archive, is_daylist=True)
  else:
    new_archive = sp.user_playlist_create(user=sp.current_user_id, name=archive_name, public=False)
    sp.transfer_songs_to_archive(from_playlist=daylist, to_playlist=new_archive, is_new_archive=True, is_daylist=True)

# GENERAL TRANSFERS SYNC
for transfer in TRANSFERS: 
  from_playlist = sp.playlist(playlist_id=transfer["from_playlist_link"])
  to_playlist = sp.playlist(playlist_id=transfer["to_playlist_link"])

  sp.transfer_songs_to_archive(from_playlist=from_playlist, to_playlist=to_playlist)