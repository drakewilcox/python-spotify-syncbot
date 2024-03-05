from transfers import TRANSFERS
from spotify_session import SpotifySession 
from log_config import configure_logging

app_logger = configure_logging()

sp = SpotifySession(logger=app_logger)

for transfer in TRANSFERS: 
  from_playlist = sp.playlist(playlist_id=transfer["from_playlist_link"])
  to_playlist = sp.playlist(playlist_id=transfer["to_playlist_link"])

  sp.transfer_songs_to_archive(from_playlist=from_playlist, to_playlist=to_playlist)

