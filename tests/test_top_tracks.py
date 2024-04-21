import pytest
from main import top_tracks

def test_top_tracks():
    #Checks top tracks for The Wonder Years
    df = top_tracks('The Wonder Years')

