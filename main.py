import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe
from filter_features import filter_pitch, filter_tempo, filter_danceability
from track_info import get_track_info_and_features, spotify
from save_load import save_filters, load_filters

#spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#spotipy_fix(spotify) #may need to resolve with track_info
app = typer.Typer()

def uri_from_search(name: str, search_type: str):
    #limit determines amount of results, artist and album are limited to 10 results via API
    results = spotify.search(q=f"{search_type}:" + name, type=search_type, limit=50)
    items = results[search_type + "s"]["items"]
    #prints the amount of results
    print(f"Number of results: {len(items)}")
    if len(items) > 0:
        return [item["id"] for item in items]
    else:
        raise ValueError(f"No {search_type}s found with the name {name}")

#Dictionary of filter handlers for filtering in top_tracks, this is used when filtering a song by feature
filter_handlers = {"pitch": filter_pitch, "tempo": filter_tempo, "danceabillity": filter_danceability}

@app.command()
#top_tracks passed arguments based on flags such as -a or -s
def top_tracks(artist: str = typer.Option(None, '-a', '--artist'),
               song: str = typer.Option(None, '-s', '--song'),
               pitch: str = typer.Option(None, '-p', '--pitch'),
               tempo: str = typer.Option(None, '-t', '--tempo'),
               danceabillity: str = typer.Option(None, '-d', '--dance'),
               help: str = typer.Option(None, '-h', '--help'),
               save: bool = None,
               load: bool = None,
):
    
    if save is not None:
        save_filters(tempo, pitch)
        return

    if load is not None:
        pitch, tempo = load_filters()
    
    print(r"     _________              __  .__  _____                  .___")
    print(r"    /   _____/_____   _____/  |_|__|/ ____\__.__. ____    __| _/")
    print(r"    \_____  \\____ \ /  _ \   __\  \   __<   |  |/    \  / __ | ")
    print(r"    /        \  |_> >  <_> )  | |  ||  |  \___  |   |  \/ /_/ | ")
    print(r"   /_______  /   __/ \____/|__| |__||__|  / ____|___|  /\____ | ")
    print(r"           \/|__|                         \/         \/      \/ ")
    
    
    if artist is None and song is None:
        
        print("Welcome to SpotiFynd! Please input the artist, song, pitch, tempo, or dance property" + 
          " you are interested in.\nFor example: $python main.py -a 'Drake'" +

          "\n\nThe specific flags are:\n'-a' or 'artist' for artist" +
          "\n'-s' or '--song' for song"   +
          "\n'-p' or '--pitch' for pitch" +
          "\n'-t' or '--tempo' for tempo" + 
          "\n'-d' or '--dance' for dance" +
          
          "\n or '-h' or '--help' to display this message again\nHAVE FUN!")  
    
    #Used to filter the search results
    flags = {"artist": artist, "song": song, "pitch": pitch, "tempo": tempo, "danceabillity": danceabillity}
    
    #artist flag passed limited to 10 results
    if artist:
        search_type = "artist"
        name = artist
    #song flag passed limited by limit= in uri_from_search
    elif song or tempo or pitch or danceabillity:
        search_type = "track"
        name = song
    else:
        raise ValueError("You must provide either an artist (-a) or a song (-s).")
    ids = uri_from_search(name, search_type)
    track_data = []
    
    #track search
    if search_type == "track":
        all_info = get_track_info_and_features(ids)
        for track_info, features in all_info:
            #Always append track_info to track_data
            track_data.append(track_info)
            #Apply filters, filter_handlers is a dictionary of filter functions that calls on the filtering functions
            for flag, handler in filter_handlers.items(): 
                if flags[flag] is not None:
                    #Update the last element of track_data with the filtered track_info
                    track_data[-1] = handler(track_info, features, flags[flag])
    #Artist search
    else:
        for id in ids:
            results = spotify.artist_top_tracks(artist_id=id, country="US")
            track_ids = [track["id"] for track in results["tracks"]]
            if track_ids:
                all_info = get_track_info_and_features(track_ids) #gets track info and features
                #for all requested info
                for track_info, features in all_info:
                    #Operation is always done
                    track_data.append(track_info)
                    #Apply filters
                    for flag, handler in filter_handlers.items():
                        if flags[flag] is not None:
                            track_data[-1] = handler(track_info, features, flags[flag])       
    df = create_dataframe(track_data)
if __name__ == "__main__":
    app()