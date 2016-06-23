from requests.auth import HTTPBasicAuth

def gitcreds():
    auth = HTTPBasicAuth('YOURUSERNAMEHERE', 'YOURPASSWORDHERE')
    return auth