from create_playlist import create_playlist, get_playlists_info, add_to_playlist

#Test playlist creation
def test_create_playlist():
    #Create playlist with test-playlist name
    playlist_id = create_playlist(name="test-playlist", is_public=True)

    # Check that the playlist was created by reading user's playlists
    playlists = get_playlists_info()
    assert playlist_id in playlists["playlist_id"].values

#Testing songs added to playlist run manually by physically checking the playlist