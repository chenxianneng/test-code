from PIL import Image
import os.path
import glob

def make_square(img, fill_color=(0, 0, 0, 0)):
    screen_width = 1366
    screen_height = 768

    x, y = img.size
    new_x, new_y = 0, 0
    if (x / y) > (screen_width / screen_height):
        new_x = screen_width
        new_y = y * (screen_width / x)
    else:
        new_y = screen_height
        new_x = x * (screen_height / y)

    print(x, y, new_x, new_y)
    img = img.resize((int(new_x), int(new_y)),Image.BILINEAR)   
    new_im = Image.new('RGBA', (screen_width, screen_height), fill_color)
    pos_x, pos_y = (screen_width - new_x) / 2, (screen_height - new_y) / 2
    new_im.paste(img, (int(pos_x), int(pos_y)))
    return new_im

def convertjpg(jpgfile, outdir):
    img = Image.open(jpgfile)
    img.convert("RGBA")

    result = make_square(img)
    #result.show()
    result = result.convert('RGB')
    result.save(os.path.join(outdir, os.path.basename(jpgfile)))


import os
import glob
from natsort import natsorted
from moviepy.editor import *
from moviepy.audio.fx import all

def run(directory, back_ground_music, out_dir):
    base_dir = os.path.realpath(directory)
    print(base_dir)

    for jpgfile in glob.glob(base_dir + "*.jpg"):
        convertjpg(jpgfile, out_dir)
    
    fps = 24

    file_list = glob.glob(out_dir +  '*.jpg')  # Get all the pngs in the current directory
    file_list_sorted = natsorted(file_list, reverse=False)  # Sort the images

    clips = [ImageClip(m).set_duration(5)
             for m in file_list_sorted]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(out_dir + "output.mp4", fps=fps, audio=back_ground_music)

run('f:/test-code/youtube/input/', 'f:/test-code/youtube/back_ground.mp3', 'f:/test-code/youtube/output/')
