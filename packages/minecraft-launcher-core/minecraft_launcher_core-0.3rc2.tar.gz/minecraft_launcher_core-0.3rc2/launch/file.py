import requests
class File:
    def __init__(self,url,path):
        r = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'})
        with open(path, 'wb') as f:
            f.write(r.content)