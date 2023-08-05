import requests
class File:
    def __init__(self,url,path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)