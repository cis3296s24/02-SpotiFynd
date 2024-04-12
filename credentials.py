class Credentials():
    def __init__(self):
        client_id = input("Provide Client ID: ")
        client_secret = input("Provide Client SECRET: ")
        username = input("Provide Username: ")

        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.redirect_uri = "http://localhost:3000"
        self.scope = "user-library-read"

cred = Credentials()