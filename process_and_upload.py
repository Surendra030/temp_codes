import os
import moviepy.editor as mp
from mega import Mega
import random

keys = os.getenv("M_TOKEN")
keys = keys.split("_")
mega = Mega()

def add_moving_logo(inputfile, outputname, logoimage):
    inputfile  = str(inputfile)
    try:
        # Load the video
        video = mp.VideoFileClip(inputfile)

        # Get video dimensions
        video_width, video_height = video.size
        size = int(video_width * (5 / 100) + video_height * (10 / 100))

        # Define initial position and velocity of the logo
        logo_width, logo_height = size, size  # Approximate dimensions of the logo
        x, y = random.randint(0, video_width - logo_width), random.randint(0, video_height - logo_height)
        vx, vy = 200, 150  # Velocity in pixels per second

        # Define a function to calculate the logo's position
        def moving_position(t):
            nonlocal x, y, vx, vy
            new_x = x + vx * t
            new_y = y + vy * t

            if new_x < 0 or new_x + logo_width > video_width:
                new_x = random.randint(0, video_width - logo_width)
                new_y = random.randint(0, video_height - logo_height)
            if new_y < 0 or new_y + logo_height > video_height:
                new_x = random.randint(0, video_width - logo_width)
                new_y = random.randint(0, video_height - logo_height)

            return (new_x % video_width, new_y % video_height)

        logo = (mp.ImageClip(logoimage)
                  .set_duration(video.duration)
                  .resize(height=150)
                  .set_position(moving_position))

        final = mp.CompositeVideoClip([video, logo])

        final.write_videofile(outputname)
        
        return True if os.path.exists(outputname) else False

    except Exception as e:
        print(f"Error while adding logo to video: {e}")
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
        return file_link if file_link else False

    except Exception as e:
        print(f"Error uploading file {file_name} to Mega: {e}")
        return False

def main():
    try:
        # Fetch downloaded files from artifacts
        artifact_path = './downloaded-files'  # Adjust the path to the downloaded files
        files = os.listdir(artifact_path)

        for file_name in files:
            input_file = os.path.join(artifact_path, file_name)
            output_file = f"processed_{file_name}"

            # Add moving logo to the video
            result = add_moving_logo(input_file, output_file, 'img.png')

            if result:
                # Upload the processed video back to Mega
                upload_to_mega(keys, output_file)

                # Clean up
                os.remove(input_file)
                os.remove(output_file)

    except Exception as e:
        print(f"Error in main process: {e}")

main()
