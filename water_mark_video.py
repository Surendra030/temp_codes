from mega import Mega
import moviepy.editor as mp
import random
from PIL import Image
import os


keys = os.getenv("M_TOKEN")
keys = keys.split("_")
mega = Mega()


def add_moving_logo(inputfile, outputname, logoimage):
    inputfile = str(inputfile)

    try:
        # Load the video
        video = mp.VideoFileClip(inputfile)
    except Exception as e:
        print(f"Error loading video file {inputfile}: {e}")
        return False

    try:
        # Get video dimensions
        video_width, video_height = video.size
        size = int(video_width * (5 / 100) + video_height * (10 / 100))
        print(f"Logo size: {size}")

        # Define initial position and velocity of the logo
        logo_width, logo_height = size, size  # Approximate dimensions of the logo
        x, y = random.randint(0, video_width - logo_width), random.randint(0, video_height - logo_height)
        vx, vy = 200, 150  # Velocity in pixels per second

        # Define a function to calculate the logo's position
        def moving_position(t):
            nonlocal x, y, vx, vy
            # Calculate new position
            new_x = x + vx * t
            new_y = y + vy * t

            # Check for boundaries and reset or bounce
            if new_x < 0 or new_x + logo_width > video_width:
                new_x = random.randint(0, video_width - logo_width)
                new_y = random.randint(0, video_height - logo_height)
            if new_y < 0 or new_y + logo_height > video_height:
                new_x = random.randint(0, video_width - logo_width)
                new_y = random.randint(0, video_height - logo_height)

            return (new_x % video_width, new_y % video_height)

        # Create the logo clip
        logo = (mp.ImageClip(logoimage)
                .set_duration(video.duration)  # Match video duration
                .resize(height=150, resample=Image.Resampling.LANCZOS)  # Use LANCZOS for resizing
                .set_position(moving_position))  # Dynamic position

        # Add the logo to the video
        final = mp.CompositeVideoClip([video, logo])

        # Save the video with the moving and bouncing logo
        final.write_videofile(outputname)
        
        if os.path.exists(outputname):
            return True
        else:
            print(f"Error: Output file {outputname} not created.")
            return False
    except Exception as e:
        print(f"Error while adding logo to video: {e}")
        return False

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

def upload_to_mega(keys, file_name):
    try:
        mega = Mega()
        m = mega.login(keys[0], keys[1])
        folder = m.find('Mushoku', exclude_deleted=True)
        folder_handle = folder['h']

        try:
            m.delete(file_name)
        except Exception as e:
            print(f"Error deleting file {file_name}: {e}")

        file_obj = m.upload(file_name, folder_handle)
        file_link = m.get_upload_link(file_obj)
        if file_link:
            print(f"file uploded sucessfully.")
            return True
        else:
            print(f"Error: File upload failed for {file_name}")
            return False
    except Exception as e:
        print(f"Error uploading file {file_name} to Mega: {e}")
        return False

def main():
    try:
        mega = Mega()
        m = mega.login(keys[0], keys[1])

        # Fetch all files from Mega
        all_files = m.get_files()

        # Fetch video links
        video_lst = fetch_video_file_links(keys, m, all_files)
        video_lst = video_lst[:2]
        for index,video_obj in enumerate(video_lst):
            print(f"{index} : started processing.")
            f_name = video_obj['file_name']
            link = video_obj['link']
            
            # Download the video
            f_name = mega_download_url(link)

            if f_name:
                print(f"{f_name} : downloded sucessfully.")
                output_file = f"temp.mp4"
                
                # Add moving logo to the video
                result_flag = add_moving_logo(f_name, output_file, 'img.png')

                if result_flag:
                    print(f"Water Mark sucessfully added to video")
                    # Remove original and temporary files
                    os.remove(f_name)
                    os.remove(output_file)
                    
                    # Upload the video to Mega
                    u_flag = upload_to_mega(keys, f_name)
                    if u_flag: os.remove(f_name)
                else:
                    print(f"Error processing video {f_name} with moving logo.")
            else:
                print(f"Failed to download video {f_name} from link {link}")

    except Exception as e:
        print(f"Error in main process: {e}")

main()
