import os
from mega import Mega

def upload_to_mega(keys, file_path):
    try:
        mega = Mega()
        m = mega.login(keys[0], keys[1])
        folder = m.find('Mushoku', exclude_deleted=True)
        folder_handle = folder['h']

        file_name = os.path.basename(file_path)

        try:
            m.delete(file_name)
        except Exception as e:
            print(f"Error deleting file {file_name}: {e}")

        file_obj = m.upload(file_path, folder_handle)
        file_link = m.get_upload_link(file_obj)
        return file_link if file_link else False

    except Exception as e:
        print(f"Error uploading file {file_path} to Mega: {e}")
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