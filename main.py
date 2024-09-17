# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
import yt_dlp
import subprocess

def progress_hooks(d):
    if d['status'] == 'downloading':
        # Print progress
        print(f"Downloaded {d['_percent_str']} of {d['_total_bytes_str']}. Speed: {d['_speed_str']}. ETA: {d['_eta_str']}")
    elif d['status'] == 'finished':
        print('Download completed!')


def download_video(url):
    ydl_opts = {
        'format': 'best',  
        'outtmpl': '%(title)s.%(ext)s',  
        'noplaylist': True, 
        'progress_hooks': [progress_hooks],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from {url}...")
            info_dict = ydl.extract_info(url, download=True)
            print("Download completed!")
            file_name = ydl.prepare_filename(info_dict)
            return file_name
    except Exception as e:
        print(f"Error downloading video: {e}")



def trim_video(input_file, start_time, end_time, output_file):
    ffmpeg_command = [
        'ffmpeg', '-i', input_file,
        '-ss', start_time, '-to', end_time,
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', 
        '-c:a', 'aac', '-b:a', '192k',
        output_file
    ]
    subprocess.run(ffmpeg_command)


def download_video_with_section(url, start_time, end_time):
    try:
        file_name = download_video(url)
        trim_video(file_name, start_time, end_time, "trim_" + file_name)
    except Exception as e:
        print(f"Error downloading video: {e}")


def download_audio(url):
    ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from {url}...")
            ydl.download([url])
            print("Download completed!")
    except Exception as e:
        print(f"Error downloading video: {e}")

