import os
from mega import Mega

keys = os.getenv("M_TOKEN")
keys = keys.split("_")
mega = Mega()

def fetch_video_file_links(keys, m, all_files):
    lst = []
    try:
        for key, snippet in all_files.items():
            file_name = snippet['a']['n']
            if 'compress.mp4' in file_name:
                link = m.export(file_name)
                lst.append({
                    "file_name": file_name,
                    "link": link
                })
    except Exception as e:
        print(f"Error fetching video file links: {e}")
    return lst

def mega_download_url(link):
    try:
        mega = Mega()
        m = mega.login(keys[0], keys[1])
        file_name = m.download_url(link)
        if os.path.exists(file_name):
            return file_name
    except Exception as e:
        print(f"Error downloading URL {link}: {e}")
        return False

def main():
    try:
        mega = Mega()
        m = mega.login(keys[0], keys[1])

        # Fetch all files from Mega
        all_files = m.get_files()

        # Fetch video links
        video_lst = fetch_video_file_links(keys, m, all_files)
        video_lst = video_lst[:2]  # Limit to first 2 for demo, can change this

        downloaded_files = []

        for video_obj in video_lst:
            f_name = video_obj['file_name']
            link = video_obj['link']

            # Download the video
            f_name = mega_download_url(link)
            if f_name:
                print(f"{f_name} : downloaded successfully.")
                downloaded_files.append(f_name)
            else:
                print(f"Failed to download video {f_name} from link {link}")

        # Upload downloaded files as artifacts
        if downloaded_files:
            print(f"Uploading downloaded files as artifacts: {downloaded_files}")
            # You can use GitHub Actions 'upload-artifact' action to save them
            return downloaded_files
        else:
            print("No files to upload as artifacts.")
            return []
    except Exception as e:
        print(f"Error in main process: {e}")

main()
