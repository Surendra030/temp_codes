import os
from mega import Mega

def upload_to_mega(keys, file_path):
    file_name = os.path.basename(file_path)
    try:
        # Initialize Mega
        mega = Mega()
        m = mega.login(keys[0], keys[1])

        # Find the folder
        folder = m.find('Mushoku', exclude_deleted=True)
        print(f"Find folder output: {folder}")
        if folder and isinstance(folder, tuple):
            folder = folder[1]  # Extract the first element if tuple
        folder_handle = folder['h'] if folder else None

        if not folder_handle:
            raise ValueError("Folder 'Mushoku' not found in Mega account.")

        # Get file name and process name
        process_file_name = file_name.replace(".", "_process.")

        # Rename file locally if necessary
        os.rename(file_path, process_file_name)

        # Upload file to Mega
        file_obj = m.upload(process_file_name, folder_handle)
        file_link = m.get_upload_link(file_obj)

        if file_link:
            print(f"Uploaded {process_file_name}: {file_link}")
            # Optionally delete file from Mega
            try:
                m.delete(file_name)  # Delete by handle
            except Exception as e:
                print(f"Error deleting file {file_name} from Mega: {e}")
        else:
            print("Failed to generate file link after upload.")

        # Rename back to the original name (optional)
        os.rename(process_file_name, file_path)

        return file_link if file_link else False

    except Exception as e:
        print(f"Error uploading file {file_name} to Mega: {e}")
        return False



def main():
    try:
        # Load credentials
        keys = os.getenv("M_TOKEN", "").split("_")
        if len(keys) != 2:
            raise ValueError("Invalid M_TOKEN format. Expected 'email_password'.")

        # Input directory
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
