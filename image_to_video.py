# import os
# from PIL import Image
 
# filename = os.listdir("d:/2/")
# base_dir = "d:/2/"
# new_dir  = "d:/1/"
# size_m = 1366
# size_n = 768
 
# for img in filename:
#     image = Image.open(base_dir + img)
#     image_size = image.resize((size_m, size_n),Image.ANTIALIAS)
#     image_size.save(new_dir+ img)

# from PIL import Image
  
# def blend_two_images():
#     img1 = Image.open( "bridge.png ")
#     img1 = img1.convert('RGBA')
 
#     img2 = Image.open( "birds.png ")
#     img2 = img2.convert('RGBA')
    
#     img = Image.blend(img1, img2, 0.3)
#     img.show()
#     img.save( "blend.png")
 
#     return


# from PIL import Image
# import os.path
# import glob
# def convertjpg(jpgfile,outdir,width=1366,height=768):
#     img=Image.open(jpgfile)
#     try:
#         new_img=img.resize((width,height),Image.BILINEAR)   
#         new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
#     except Exception as e:
#         print(e)
        
# for jpgfile in glob.glob("d:/2/*.jpg"):
#     convertjpg(jpgfile,"d:/1/")

from PIL import Image
import os.path
import glob

def make_square(img, min_size=1366, fill_color=(0, 0, 0, 0)):
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
        
for jpgfile in glob.glob("d:/2/*.jpg"):
    convertjpg(jpgfile, "d:/1/")



# def make_square(im, min_size=1366, fill_color=(0, 0, 0, 0)):
#     x, y = im.size
#     size = max(min_size, x, y)
#     new_im = Image.new('RGBA', (size, size), fill_color)
#     new_im.paste(im, ((size - x) / 2, (size - y) / 2))
#     return new_im
    

import os
import glob
from natsort import natsorted
from moviepy.editor import *
from moviepy.audio.fx import all

base_dir = os.path.realpath("d:/1/")
print(base_dir)

fps = 24

file_list = glob.glob('d:/1/*.jpg')  # Get all the pngs in the current directory
file_list_sorted = natsorted(file_list, reverse=False)  # Sort the images

clips = [ImageClip(m).set_duration(3)
         for m in file_list_sorted]

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("d:/1/test.mp4", fps=fps, audio="d:/1/1.mp3")


# import cv2
# import os

# image_folder = 'd:/1/'
# video_name = 'd:/1/video.avi'

# images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
# frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape

# video = cv2.VideoWriter(video_name, 0, 1, (width,height), 24)
# video.set(cv2.CAP_PROP_POS_AVI_RATIO, 10)

# for image in images:
#     print(image)
#     video.write(cv2.imread(os.path.join(image_folder, image)))

# cv2.destroyAllWindows()
# video.release()


# import os
# import cv2

# dir_path = "d:/1/"
# ext = '.jpg'
# output = 'video.avi'
# shape = 960, 720
# fps = 1

# images = [f for f in os.listdir(dir_path) if f.endswith(ext)]

# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# video = cv2.VideoWriter(output, fourcc, fps, shape)

# for image in images:
#     image_path = os.path.join(dir_path, image)
#     image = cv2.imread(image_path)
#     resized=cv2.resize(image,shape) 
#     video.write(resized)

# video.release()
