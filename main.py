#!/usr/bin/env python3

from motion_detector import MotionDetector
from still_camera import StillCamera
from gifbox_uploader import GifBoxUploader

IMAGE_FILE_PATH = 'capture.jpg'

detector = MotionDetector()
camera = StillCamera(default_file_path=IMAGE_FILE_PATH, resolution=(640, 480), rotation=180)
uploader = GifBoxUploader()

print('Checking for motion...')

while True:
    if detector.motion_detected():
        # Take a high res photo and save it
        camera.shoot()
        # Upload the file. You could do anything you want here with the
        # image file. I upload it to my custom online image repository
        uploader.upload(IMAGE_FILE_PATH)
