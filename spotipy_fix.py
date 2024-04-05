from requests import Session
from spotipy import Spotify


def spotipy_fix(spotify: Spotify) -> None:
    """
    Uses some Python magic to overwrite spotipy.Spotify's destructor method.
    Without this fix, there's an exception every time the program finishes.
    """
    def fixed_del(self):
        if isinstance(self._session, Session):
            self._session.close()
    spotify.__del__ = fixed_del.__get__(spotify, Spotify)
