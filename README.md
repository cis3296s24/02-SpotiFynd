# SpotiFynd Data CLI
A command-line interface (CLI) using Typer for a user’s Spotify statistics. Given a command, the program will send a Spotify Web API request using the Spotipy library, which will return the requested information (such as an artist’s top N tracks, the most popular tracks in the US right now, tempo of a song, etc.)

There are many Spotify command-line apps (For instance, Spotify-cli), but most have more of a focus on being an interface (playback, creating playlists, etc.) than a data tool. Rather than being an alternative frontend/UI to the Spotify desktop app, this application focuses more on quickly and easily accessing song data (which isn’t available in the desktop app).

Proof of feasibility: https://github.com/tuo20482/spotify-data-cli

## Prerequisites
- Python 3.8 or higher
- A Spotify Developer account and your own Client ID and Client Secret for accessing the Spotify Web API

## Installation
1. Clone this repository to your local machine.
2. Navigate to the cloned directory.
3. It is recommended to create a virtual environment for this project:
```
python -m venv venv
```
4. Activate the virtual environment:
- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```
5. Install the required dependencies:
```
pip install spotipy typer
```

## Configuration
Before running the application, you need to set up your Spotify API credentials. Set your Client ID and Client Secret as environment variables:
- On Windows:
```
set SPOTIPY_CLIENT_ID=your_client_id_here
set SPOTIPY_CLIENT_SECRET=your_client_secret_here
```
- On macOS and Linux:
```
export SPOTIPY_CLIENT_ID=your_client_id_here
export SPOTIPY_CLIENT_SECRET=your_client_secret_here
```
*** To get a client ID and client secret, you must sign up for Spotipy's web API. Follow below instructions to do so. ***
1. Browse to https://developer.spotify.com/dashboard/applications.

2. Log in with your Spotify account.

3. Click on ‘Create an app’.

4. Pick an ‘App name’ and ‘App description’ of your choice and mark the checkboxes. For your URI you can use http://localhost/.

5. After creation, you see your ‘Client Id’ and you can click on ‘Show client secret` to unhide your ’Client secret’.

6. Use your ‘Client id’ and ‘Client secret’ to retrieve a token from the Spotify API.

## Running the Application
To run the application, use the following command:
```
python main.py "artist name"
```


# Authors
- Gabriel Carvalho
- Addison Migash
- Animish Tenneti
- Matthew Christofas
- Justin Means
- Dennis Yeom
