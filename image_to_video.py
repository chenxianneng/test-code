import os
import glob
from natsort import natsorted
from moviepy.editor import *

base_dir = os.path.realpath("d:/1/")
print(base_dir)

gif_name = 'pic'
fps = 24

file_list = glob.glob('d:/1/*.jpg')  # Get all the pngs in the current directory
file_list_sorted = natsorted(file_list,reverse=False)  # Sort the images

clips = [ImageClip(m).set_duration(2)
         for m in file_list_sorted]

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("d:/1/test.mp4", fps=fps, audio="d:/1/1.mp3")
