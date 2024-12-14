import os
from mega import Mega

def upload_to_mega(keys, file_path):
    try:
        mega = Mega()
        m = mega.login(keys[0], keys[1])
        folder = m.find('Mushoku', exclude_deleted=True)
        folder_handle = folder['h']
        
        file_path = str(file_path).split("/")[-1]
        
        file_name = os.path.basename(file_path)
        process_file_name = file_name.split(".")
        
        
        process_file_name = f"{process_file_name[0]}_process.{process_file_name[-1]}"
        
        file_obj = m.upload(process_file_name, folder_handle)
        file_link = m.get_upload_link(file_obj)
        if file_link:
            try:
                m.delete(file_name)
            except Exception as e:
                print(f"Error deleting file {file_name}: {e}")
        else:
            print("No file link found.")
        return file_link if file_link else False

    except Exception as e:
        print(f"Error uploading file {process_file_name} to Mega: {e}")
        return False

def main():
    try:
        keys = os.getenv("M_TOKEN").split("_")
        input_path = './processed-files'

        files = os.listdir(input_path)

        for file_name in files:
            file_path = os.path.join(input_path, file_name)

            # Upload to Mega
            link = upload_to_mega(keys, file_path)

            if link:
                print(f"Uploaded {file_name}: {link}")
                os.remove(file_path)  # Clean up after successful upload
            else:
                print(f"Failed to upload: {file_name}")

    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
