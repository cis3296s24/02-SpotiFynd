import spotipy  
from spotipy import Spotify  
  
sp = Spotify(auth_manager=sp_oauth)  
  
# Create a playlist  
playlist_name = "My new playlist"  
sp.user_playlist_create("USERNAME", playlist_name)  
  
#Add tracks to the playlist  
track_ids = ['4uLU6hMCjMI75M1A2tKUQC', '1301WleyT98MSxVHPZCA6M']  
sp.user_playlist_add_tracks("USERNAME", playlist_id, track_ids)  
  
# Retrieve all the playlists of a user  
playlists = sp.user_playlists("USERNAME")  