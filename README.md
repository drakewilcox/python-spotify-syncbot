# Spotify Playlist SyncBot

The goal of this project was to build a tool for keeping an running archive of playlists that change on a regular basis. For instance, this program can be used to make sure that all of the songs from a Discover Weekly playlist (which is updated every week), is stored in another playlist that acts as an archive.

### Features and Technologies:

1. Takes in an array of “transfers” that will be done each time the script is ran.
   1. Each transfer object includes the “from_playlist”, and a “to_playlist.
   2. During a transfer, all the songs contained within the “from_playlist”, will be moved to the “to_playlist.”
   3. Any songs that already exist in the to_playlist will be skipped.
   4. If songs are added, then the description of the to_playlist will be changed to display the last updated date, and the source of the content.
2. The SpotiPy Python Library is used for SpotifyOAuth, and interaction with the Spotify Web API.
3. Songs are retrieved from and added to playlists in batches, to prevent limit errors from the Spotify API. This means that over 100 songs can be added to a playlist during one transfer.
4. The main.js Python Script is ran as a cron job with Github Actions, and is currently set to run once a day.
5. After the `main.js` script is run, the `sync_log.txt` file is updated to include records of which playlists where updated during the job. The github actions have also been configured so that these changes are committed and saved when the script is ran through the github action workflow.

### Usage

1. Fork this repo
2. Clone and spin up local environment (Mac OS):

```python
git clone {repository-url}
cd python-spotify-syncbot
python3 -m venv venv
source venv/bin/activate # activates virtual python environment
pip install -r requirements.txt # Installs required dependencies

cp .env-example .env # Duplicates .env-example and creates .env file to add your own variables
rm sync_log.txt # Removes the log, which will be recreated once main.js is ran successfully.
```

1. Go to the Spotify Developer Dashboard and log in with your Spotify account.
2. Click on the "Create an App" button and fill out the necessary information.
3. From the app dashboard, you'll find your client ID, client secret and Redirect URL. Copy this and paste it your `.env` file.
4. After the .env file is updated, run the script `get_refresh_token.py` to get refresh token. Follow the instruction in this script. Copy the refresh token into the `.env` file.
5. Before running the main.js script, update the `transfers.py` file:

   1. _THE TRANSFER WILL ONLY WORK IF YOU THE AUTHENTICATED USER IS THE OWNER OF THE TO_PLAYLIST._
   2. The from_playlist_name, and to_playlist_name will not impact the functionality if they are off, but they are used in the activity log to keep track of transfers.
   3. To get the link for a playlist in spotify, click on the ellipses, go to share, and click on “Copy Link to Playlist.”
   4. Example:

```python
  TRANSFERS = [
    {
      "from_playlist_name": {name_of_source_playlist},
      "from_playlist_link": {link_of_source_playlist},
      "to_playlist_name": {playlist_name_to_store_archive},
      "to_playlist_link": {playlist_link_to_store_archive},
 	  }
  ]
```

6. Run the `main.js` script for local testing.
7. To set up github actions for this project so that the main.js script is ran on a cron job:
   1. Add all env variables as a github repository secret.
   2. To change the frequency of how often the script is ran, update the `cron: '0 2 * * *’` on line 5 of the `actions.yml`
   3. Look at [Cron Generator](https://crontab.guru/) for help with this syntax.
   4. NOTE: this file has been updated so that the actions are compatible with the newest version of github actions, which now runs on Node 20.

### Resources:

[Spotipy Documentation](https://github.com/spotipy-dev/spotipy/tree/master)

[Python Git Action Template for Reference](https://github.com/patrickloeber/python-github-action-template)

[Spotify for Developers](https://developer.spotify.com/)
