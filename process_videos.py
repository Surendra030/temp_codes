import os
import random
import moviepy.editor as mp

def add_moving_logo(inputfile, outputname, logoimage):
    inputfile = str(inputfile)
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

def main():
    try:
        input_path = './downloaded-files'
        output_path = './processed-files'

        # Ensure output folder exists
        os.makedirs(output_path, exist_ok=True)

        files = os.listdir(input_path)

        for file_name in files:
            input_file = os.path.join(input_path, file_name)
            output_file = os.path.join(output_path, file_name)

            # Add moving logo to the video
            result = add_moving_logo(input_file, output_file, 'img.png')

            if result:
                print(f"Processed and saved: {output_file}")
            else:
                print(f"Failed to process: {input_file}")

    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == "__main__":
    main()
