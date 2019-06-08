import picamera
import datetime
import os
import glob

camera = picamera.PiCamera()
camera.resolution = (640, 480)

all_videos = glob.glob("./videos/*.h246")

while True:
    file_name = str(datetime.datetime.now()) + '.h264'
    camera.start_recording('./videos/' + file_name)
    camera.wait_recording(60)
    camera.stop_recording()
    print(file_name)
    all_videos.append(file_name)

    if len(all_videos) > 1440:
        os.remove('./videos/' + all_videos[0])
        del all_videos[0]
