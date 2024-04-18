#testing the credentials.py file. Dependent that credentials have been input somewhere
import pytest
import os
import json
from credentials import Credentials

def test_credentials():
    #Create a Credentials object
    credentials = Credentials()

    #Check that the attributes are set correctly
    assert hasattr(credentials, 'client_id')
    assert hasattr(credentials, 'client_secret')
    assert hasattr(credentials, 'username')
    assert hasattr(credentials, 'redirect_uri')
    assert hasattr(credentials, 'scope')

    #Check that the credentials are stored in a file
    assert os.path.exists('credentials.json')

    #Check that the file contains the correct data
    with open('credentials.json', 'r') as file:
        stored_credentials = json.load(file)
        assert stored_credentials['client_id'] == credentials.client_id
        assert stored_credentials['client_secret'] == credentials.client_secret
        assert stored_credentials['username'] == credentials.username