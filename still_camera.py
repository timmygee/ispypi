#!/usr/bin/env python3
# A simple class that takes a still image from the pi camera based on some
# default settings
import picamera
import time


class StillCamera:
    led_status = True
    resolution = (2592, 1944)
    default_file_path = 'still_image.jpg'

    def __init__(self, **kwargs):
        for kwarg in ['led_status', 'resolution', 'default_file_path']:
            if kwarg in kwargs and kwargs[kwarg]:
                setattr(self, kwarg, kwargs[kwarg])

    def shoot(self, file_path=None):
        """Take the photo and save it to default_file_path"""
        with picamera.PiCamera() as camera:
            camera.resolution = self.resolution
            # camera.led = self.led_status
            camera.start_preview()
            time.sleep(2)
            camera.capture(file_path if file_path else self.default_file_path)


if __name__ == '__main__':
    still_camera = StillCamera()
    still_camera.shoot()
