import yt_dlp
import argparse
import os


def download(url, download_type='video', output_path='.'):
    """
    Downloads a video or audio from YouTube using yt-dlp

    Parameters:
    - url: The YouTube URL
    - download_type: 'video' for video download, 'music' for audio download
    - output_path: The directory where the downloaded file will be saved (default is current directory)
    """
    try:
        if download_type == 'music':
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'postprocessors': [],
            }
        elif download_type == 'video':
            ydl_opts = {
                'format': 'best',
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            }
        else:
            print("Invalid download type! Use 'video' or 'music'")
            return

        # get final file path
        downloaded_file_path = []

        def progress_hook(d):
            if d['status'] == 'finished':
                downloaded_file_path.append(d['filename'])

        ydl_opts['progress_hooks'] = [progress_hook]

        # download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if downloaded_file_path:
            file_path = downloaded_file_path[0]
            file_name = os.path.basename(file_path)
            print(f"Download complete! Your file: {file_name} saved in {os.path.abspath(output_path)}")
        else:
            print("No file downloaded. Something went wrong!")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos or music")

    parser.add_argument('url', help="The YouTube video URL to download")
    parser.add_argument('-m', '--music', action='store_true',
                        help="Download audio only (music)")
    parser.add_argument('-v', '--video', action='store_true',
                        help="Download video (default behavior if neither -m nor -v is provided)")
    parser.add_argument('-d', '--directory', default='.',
                        help="The directory where the downloaded file will be saved (default is current directory)")

    args = parser.parse_args()
    if args.music:
        download_type = 'music'
    else:
        download_type = 'video'

    download(args.url, download_type, args.directory)


if __name__ == "__main__":
    main()
