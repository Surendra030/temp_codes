from mega import Mega
import os

mega = Mega()

keys = os.getenv("M_TOKEN")
[email,password] = keys.split("_")
m = mega.login(email,password)
file_name = m.download_url("https://mega.co.nz/#!c5RSnYxb!Cd2nQuZyoFVQhs-ZVhAQG6d5_ZtxmOaAk-bFyMzinGs")
print(file_name)