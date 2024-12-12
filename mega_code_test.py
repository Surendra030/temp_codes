
import os
from mega import Mega

mega  = Mega()

keys = os.getenv("M_TOKEN")
keys = keys.split("_")

m = mega.login(keys[0],keys[1])
links = ['https://mega.co.nz/#!c5RSnYxb!Cd2nQuZyoFVQhs-ZVhAQG6d5_ZtxmOaAk-bFyMzinGs',
         'https://mega.nz/file/1oo3mBKT#ZJYcXjEA8HvW4XfJq5Bo1Tjd-Yvs1YvZM9N-1bQpoEc']


for link in links:
    try:
        file = m.download_url(link)
        print(f"File downloaded: {file}")
    except Exception as e:
        print(f"Error processing link {link}: {e}")
