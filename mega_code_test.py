import time

from mega import Mega
from pymongo import MongoClient
import os
import re
import json

mega = Mega()

def login_part(mega):
    """Login to Mega using environment variables."""
    try:
        print("Logging in to Mega...")
        keys = os.getenv("M_TOKEN")
        if not keys:
            raise ValueError("Mega credentials are not set in environment variables.")
        
        keys = keys.split("_")
        if len(keys) != 2:
            raise ValueError("Mega credentials are incorrectly formatted in environment variables.")
        
        m = mega.login(keys[0], keys[1])
        print("Logged in to Mega successfully.")
        return m
    except Exception as e:
        print(f"Error during Mega login: {e}")
        return None

def download_file(m,file_links):
    try:
        
        if len(file_links) >1:
            print("stated..")
            print(m)
            file_name = m.download_url(file_links[0])
            audio_file_name = m.download_url(file_links[1])
            print("working..")
            print(os.listdir())
            return [file_name,audio_file_name]
        else:
            file_name = m.download_url(file_links[0])


    except Exception as e:
        print(f"Error downloading file : {e}")
        return None


def save_links_to_db(lst,collection_name):
    collection_name = f"{collection_name}_video_links"
    mongourl = os.getenv("MONGO_URL")
    client = MongoClient(mongourl)
    db = client['file_links']
    collection = db[collection_name]
    if lst:
        collection.insert_many(lst)
        print(f"Successfully inserted {len(lst)} documents into the collection.")

    else:
        print("No data to insert")
def process_links(m,mega, links_data, audio_file_name):
    """Process the links data."""

    video_files_data = []
    try:
        if not m:
            m = login_part(mega)

        o_path = ""
        for key, snippet in links_data.items():
            file_name = snippet.get("file_name", "No file_name found")
            link = snippet.get("sharable_link", "No link available")
            
            if link:
                link_lst = [link]
                pdf_file_name = download_file(m,link_lst)
            
            exten = file_name.split(".")[-1]
            output_path = file_name.split(".")[0]
            o_path  = output_path
            main_folder_name = output_path.split("_")[1] if "_" in output_path else "temp_folder"
            
            
            if exten == 'pdf' and "compress"  in output_path:
                video_file_data_obj = "testing"
                if video_file_data_obj: video_files_data.append(video_file_data_obj)

        save_links_to_db(video_files_data,o_path)
            
    except Exception as e:
        print(f"Error processing links: {e}")

def get_shrable_links_db():
    mongo_url = os.getenv("MONGO_URL")
    client = MongoClient(mongo_url)
    db = client["file_links"]
    coll = db['links_coll']

    json_file_link = coll.find_one({"novel_title":"jobless_links"})
    audio_file_link = coll.find_one({"file_name":"audio.mp3"})
    
    
    # Fetch sharable links for specific documents
    json_file_link = coll.find_one({"novel_title": "jobless_links"}, {"_id": 0, "sharable_link": 1})
    audio_file_link = coll.find_one({"file_name": "audio.mp3"}, {"_id": 0, "sharable_link": 1})

    # Extracting only the links
    json_sharable_link = json_file_link.get("sharable_link") if json_file_link else None
    audio_sharable_link = audio_file_link.get("sharable_link") if audio_file_link else None

    return [json_sharable_link,audio_sharable_link]

def main():
    """Main function to execute the workflow."""
    
    # Login to Mega
    file_links = get_shrable_links_db()
    print(file_links)
    m = login_part(mega)
    if not m:
        print("Failed to log in to Mega. Exiting.")
        return

    # Download required files
    downloaded_files_name = download_file(m,file_links)

    if not downloaded_files_name:
        print("Required files are missing. Exiting.")
        return

    # Load links data
    try:
        with open(downloaded_files_name[0], 'r', encoding='utf-8') as f:
            links_data = json.load(f)
        # Limit to a subset of data for testing
        links_data = {k: links_data[k] for k in list(links_data)[:3]}
    except Exception as e:
        print(f"Error reading links data: {e}")
        return

    # Process the links
    process_links(m,mega, links_data, downloaded_files_name[1])

if __name__ == "__main__":
    main()
