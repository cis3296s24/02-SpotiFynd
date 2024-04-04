import json
import os
import spotipy
import typer
from spotipy.oauth2 import SpotifyClientCredentials
from dataframe import create_dataframe
from skip_auth import access_token

# Doesn't allow personal features such as playlist access, 
# but removes the need for username/password.
# Could be a launch option in the future?
spotify = spotipy.Spotify(auth=access_token())

#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
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

#Retrieves track information and features from the Spotify API
def get_track_info_and_features(ids: list):
    results = spotify.tracks(ids) #for artist, song, album
    features = spotify.audio_features(ids) #for tempo, pitch, etc
    all_info = [] #list of both track info and features

    for i in range(len(ids)):
        track_info = {
            "Art": results["tracks"][i]["album"]["images"][0]["url"],
            "Artist": results["tracks"][i]["artists"][0]["name"], 
            "Song": results["tracks"][i]["name"],
        }
        all_info.append((track_info, features[i])) #appends track info and features to all_info

    return all_info

@app.command()
#top_tracks passed arguments based on flags such as -a or -s
def top_tracks(artist: str = typer.Option(None, '-a', '--artist'),
               song: str = typer.Option(None, '-s', '--song'),
               pitch: str = typer.Option(None, '-p', '--pitch'),
               tempo: str = typer.Option(None, '-t', '--tempo'),
               danceabillity: str = typer.Option(None, '-d', '--dance'),
               save: bool = None,
               load: bool = None,
):

    if save is not None:
        saved_filters = {}
        if tempo is not None:
            saved_filters["tempo"] = tempo
        if pitch is not None:
            saved_filters["pitch"] = pitch
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(saved_filters, file, ensure_ascii=False, indent=4)
        return

    if load is not None:
        if not os.path.exists("data.json"):
            raise ValueError("No saved filter. Create one with --save")
        with open("data.json", "r") as file:
            data = json.load(file)
            pitch = data.get("pitch")
            tempo = data.get("tempo")


    print("\t   _________              __  .__  _____                  .___")
    print("\t  /   _____/_____   _____/  |_|__|/ ____\__.__. ____    __| _/")
    print("\t  \_____  \\____ \ /  _ \   __\  \   __<   |  |/    \  / __ | ")
    print("\t  /        \  |_> >  <_> )  | |  ||  |  \___  |   |  \/ /_/ | ")
    print("\t /_______  /   __/ \____/|__| |__||__|  / ____|___|  /\____ | ")
    print("\t         \/|__|                         \/         \/      \/ ")
    
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
    
    #corresponding to 0-11 value for -p search
    pitch_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    
    #track search
    if search_type == "track":
        all_info = get_track_info_and_features(ids)
        for track_info, features in all_info:
            #pitch flag was passed
            if pitch is not None and features["key"] == int(pitch):
                track_info["Pitch"] = pitch_names[features["key"]]
                track_data.append(track_info) #appends track info to track_data for df
            #tempo flag was passed
            if tempo is not None:
                min_tempo, max_tempo = map(float, tempo.split('-'))
                if min_tempo <= features["tempo"] <= max_tempo:
                    track_info["Tempo"] = features["tempo"]
                    track_data.append(track_info) #appends track info to track_data for df
            #danceability flag was passed
            if danceabillity is not None:
                min_dance, max_dance = map(float, danceabillity.split('-'))
                if min_dance < 0.0 or max_dance > 1.0:
                    raise ValueError(f"Danceability outside scope. Values must be between 0 and 1")
                if min_dance <= features["danceability"] <= max_dance:
                    track_info["Danceability"] = features["danceability"]
                    track_data.append(track_info)
            #no flags were passed
            if pitch is None and tempo is None and danceabillity is None:
                track_data.append(track_info)
    #Artist search
    else:
        for id in ids:
            results = spotify.artist_top_tracks(artist_id=id, country="US")
            track_ids = [track["id"] for track in results["tracks"]]
            if track_ids:
                all_info = get_track_info_and_features(track_ids) #gets track info and features
                #for all requested info
                for track_info, features in all_info:
                    #if pitch flag was passed
                    if pitch is not None and features["key"] == int(pitch):
                        track_info["Pitch"] = pitch_names[features["key"]]
                        track_data.append(track_info)
                    #if tempo flag was passed
                    if tempo is not None:
                        min_tempo, max_tempo = map(float, tempo.split('-')) #
                        if min_tempo <= features["tempo"] <= max_tempo:
                            track_info["Tempo"] = features["tempo"]
                            track_data.append(track_info)
                    #if danceability was passed
                    if danceabillity is not None:
                        min_dance, max_dance = map(float, danceabillity.split('-'))
                        if min_dance < 0.0 or max_dance > 1.0:
                            raise ValueError(f"Danceability outside scope. Values must be between 0 and 1")
                        if min_dance <= features["danceability"] <= max_dance:
                            track_info["Danceability"] = features["danceability"]
                            track_data.append(track_info)
                    #if no flags were passed
                    else:
                        track_data.append(track_info)       
    df = create_dataframe(track_data)
if __name__ == "__main__":
    app()