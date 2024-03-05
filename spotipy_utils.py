def get_playlist_track_uris(sp, playlist_id):
  # TEST THAT THIS IS WORKING WHEN HITTING NEXT MORE THAN ONCE

  results = sp.playlist_tracks(playlist_id=playlist_id, fields="items,next", limit=100)
  tracks = results["items"]

  while results["next"]:
    results = sp.next(results)
    tracks.extend(results["items"])

  return [track["track"]["uri"] for track in tracks]

def batch_tracks(sp, playlist_id, track_uris, batch_size=100): 
  for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i+batch_size]
        sp.playlist_add_items(playlist_id=playlist_id, items=batch)

def get_user_playlists(sp):   
  current_user = sp.current_user()
  user_id = current_user['id']
  results = sp.user_playlists(user=user_id, limit=50)

  playlists = results["items"]

  while results["next"]:
    results = sp.next(results)
    playlists.extend(results["items"])
  
  return playlists


def search_playlists_by_name(sp, query):
  playlists = get_user_playlists(sp)

  names = [playlist["name"] for playlist in playlists]
  print(names)
  for playlist in playlists: 
      if playlist['name'] == query:
        return playlist
  return None
   

def get_user_id(sp):
  current_user = sp.current_user()
  return current_user['id']

def get_playlist_details(sp):
   pass