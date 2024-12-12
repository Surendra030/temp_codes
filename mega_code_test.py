
import os
from mega import Mega

mega  = Mega()

keys = os.getenv("M_TOKEN")
keys = keys.split("_")

m = mega.login(keys[0],keys[1])
all_files = m.get_files()

folder_handler = next(
            (folder for folder in all_files.values() if folder['a']['n'] == "audio.mp3" and folder['t'] == 0),
            None
        )

file_link = m.export('audio.mp3')
print(file_link,folder_handler)