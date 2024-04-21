#used to test track_info.py
from utility import get_track_info_and_features

def test_get_track_info_and_features():
    #Define known good track IDs for testing
    test_ids = ["3n3Ppam7vgaVa1iaRUc9Lp", "3twNvmDtFQtAd5gMKedhLD"]

    all_info = get_track_info_and_features(test_ids)

    #Check function returns correct data types
    assert isinstance(all_info, list)
    for info in all_info:
        assert isinstance(info, tuple)
        assert len(info) == 2
        track_info, features = info
        assert isinstance(track_info, dict)
        assert isinstance(features, dict)
        assert set(track_info.keys()) == {"Art", "Artists", "Song", "uri"}