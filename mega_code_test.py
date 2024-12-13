import os
from mega import Mega
import subprocess
import sys

# Mega login credentials from environment variables
keys = os.getenv("M_TOKEN")
keys = keys.split("_")

# Mega login
mega = Mega()
m = mega.login(keys[0], keys[1])

# Links to download the files
links = ['https://mega.co.nz/#!Q8xGFJID!Mf32ye8u-grUDIeNK7S8C3YyUO7nijKgaa_PX0sCGOc']

# Loop through the links and download the files
for link in links:
    try:
        # Download the file using Mega library
        file_name = m.download_url(link)
        print(f"File downloaded: {file_name}")

        # Run OCR processing using ocrmypdf
        # The downloaded file will be used for OCR processing
        output_file = "output.pdf"  # Specify the output file name
        print(f"Running OCR on {file_name}...")
        
        # Using subprocess to run the ocrmypdf command
        subprocess.run(['ocrmypdf', file_name, output_file])

        print(f"OCR processing complete. Output saved to {output_file}")
        file  = m.upload(output_file)
        print(m.get_upload_link(file))
   
    except Exception as e:
        print(f"Error processing link {link}: {e}")
