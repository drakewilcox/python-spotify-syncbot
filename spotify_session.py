import spotipy 
from spotipy.oauth2 import SpotifyOAuth 
import html
from utils import formatted_time, remove_a_tags, formatted_date, formatted_previous_date, formatted_24_time
from envs import *

class SpotifySession(spotipy.Spotify):
  def __init__(self, logger=None):
    self.spotify_auth = SpotifyOAuth(
      client_id=CLIENT_ID,
      client_secret=CLIENT_SECRET,
      redirect_uri=REDIRECT_URI,
      scope=SCOPES,
    )
    self.refresh_token = REFRESH_TOKEN
    self.access_token = self.spotify_auth.refresh_access_token(REFRESH_TOKEN)["access_token"]
    super().__init__(auth=self.access_token)
    self.current_user_id = self._get_user_id()
    self.logger = logger
  
  def _get_user_id(self):
    current_user = self.current_user()
    return current_user['id']

  def get_playlist_track_uris(self, playlist_id):
    results = self.playlist_tracks(playlist_id=playlist_id, fields="items,next", limit=100)
    tracks = results["items"]

    while results["next"]:
      results = self.next(results)
      tracks.extend(results["items"])

    return [track["track"]["uri"] for track in tracks]
  
  def add_tracks(self, playlist_id, track_uris, batch_size=100):
    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i+batch_size]
        self.playlist_add_items(playlist_id=playlist_id, items=batch)
  
  def get_current_user_playlists(self):
    results = self.user_playlists(user=self.current_user_id, limit=50)
    playlists = results["items"]

    while results["next"]:
      results = self.next(results)
      playlists.extend(results["items"])
    
    return playlists 

  def search_playlists_by_name(self, query):
    playlists = self.get_current_user_playlists()
    for playlist in playlists: 
      if playlist['name'] == query:
        return playlist
    return None
  
  def prev_day_archive_uris(self): 
    prev_day_archive_name = f"{formatted_previous_date()} DAYLIST ARCHIVE"
    prev_day_archive = self.search_playlists_by_name(query=prev_day_archive_name)

    if prev_day_archive:
      prev_day_uris = self.get_playlist_track_uris(playlist_id=prev_day_archive["uri"])
      return prev_day_uris
    else: 
      return []

  def transfer_songs_to_archive(self, from_playlist, to_playlist, is_new_archive=False, is_daylist=False):
    to_uris = self.get_playlist_track_uris(playlist_id=to_playlist["uri"])
    from_uris = self.get_playlist_track_uris(playlist_id=from_playlist["uri"])
    excluded_uris = set(to_uris) 

    # Prevents a Daylist from being transferred to two Archive Days. 
    if len(to_uris) <= 50:
      prev_day_uris = self.prev_day_archive_uris()
      excluded_uris = set(to_uris) | set(prev_day_uris)

    new_uris = [uri for uri in from_uris if uri not in excluded_uris] # prevents duplicates

    description = html.unescape(to_playlist["description"]) # removes dates converted by Spotify to html
    from_name = from_playlist["name"].replace("daylist • ", "") 

    if new_uris: 
      self.add_tracks(playlist_id=to_playlist["uri"], track_uris=new_uris)
      if is_daylist:
        # Concats descriptions for each daylist made in one day.
        new_description = f"{description + ' | ' if description else ''}{formatted_24_time()} - {len(new_uris)} Songs - {from_name}"
      else:
        new_description = f"Automated Archive of the {from_playlist['name']} playlist. Last Sync: {formatted_date()}"
      # Prevents Description from being > 300 chars to avoid error  
      limit_desc = f"{new_description[:297]}..." if len(new_description) > 300 else new_description
      final_desc = description if len(description) == 300 else limit_desc

      self.playlist_change_details(playlist_id=to_playlist["uri"], description=final_desc)

      log_message = (
        f"{'Daylist ' if is_daylist else ''}Transfer Performed \n"
        f"\tLOCAL TIME: {formatted_time()} \n"
        f"\tFROM PLAYLIST NAME: {from_playlist['name']} \n"
        f"\tFROM PLAYLIST DESCRIPTION: {remove_a_tags(from_playlist['description'])} \n"
        f"\tTOTAL SONGS TRANSFERED: {len(new_uris)}\n"
        f"\tNEW ARCHIVE CREATED: {is_new_archive}\n"
        f"\tTO PLAYLIST NAME: {to_playlist['name']}\n"
        f"\tTO PLAYLIST URL: {to_playlist['external_urls']['spotify']}\n"
        + (f"\tFROM PLAYLIST URL: {from_playlist['external_urls']['spotify']}\n" if not is_daylist else "")
      ) 
      if self.logger: 
        self.logger.info(log_message)

    

  