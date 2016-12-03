import youtube_dl
import subprocess
# bach
# url='https://www.youtube.com/watch?v=DS89Vb07C-U'
# bach from playlist
# url='https://www.youtube.com/watch?v=bBbXOdZm3Jw&list=PLnmvUWZfw3kt3qp1L50dOkEdQ80kAWA7D'
url='https://www.youtube.com/watch?v=QrxjgC6ks0A'
file_path = '/Users/Frank/Documents/UCSC/TIM_209/project/test_youtube_dl/command_line/video.mkv'
ydl_opts = {'outtmpl': file_path, 'nooverwrites':False, 'noplaylist':True, 'extractaudio' : True, 'audioformat' : "mp3"}
# ydl=youtube_dl.YoutubeDL(ydl_opts)
# ydl.download([url])
command = "youtube-dl -x --audio-format wav --no-playlist -o "+file_path+' '+url
subprocess.call(command, shell=True)

# 