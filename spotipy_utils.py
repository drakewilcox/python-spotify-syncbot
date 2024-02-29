def get_playlist_track_uris(sp, playlist_id):

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