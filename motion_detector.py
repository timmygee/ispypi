#!/usr/bin/env python3

# Change the above python3 to python if you wish to use this code with python 2

# Based on the very good work found here
# https://github.com/pageauc/pi-motion-lite/blob/master/pi-motion-lite.py

# This code attempts to encapsulate and streamline motion detection using a raspberry pi camera.
# The MotionDectector class can simply be instantiated and then subsequent calls to its
# motion_detected method will indicate whether motion has been detected based on the parameters the
# MotionDectector class is initialised with.

# Example usage at bottom of file

import picamera
import picamera.array
import time
from fractions import Fraction


MICROSECONDS_IN_A_SECOND = 1000000


class MotionDetector:
    pix_threshold = 10         # How much a pixel has to change
    max_pix_changes = 200      # How many pixels need to change for motion detection
    night_shutter_speed = 5.5  # Do not exceed 6 since camera may lock up

    night_iso = 800

    detection_image_width = 128
    detection_image_height = 80

    night_awb_timeout = 10

    def __init__(self, is_daytime=True):
        """
        Initialise the motion detector object.
        """
        self.night_shutter_speed_micro = int(self.night_shutter_speed * MICROSECONDS_IN_A_SECOND)

        self.set_is_daytime(is_daytime)

        # last_glance is what the camera saw the last time it had a look at what was in front of it
        self.last_glance = self._have_a_look()

    def set_is_daytime(self, is_daytime):
        self.is_daytime = is_daytime

    def motion_detected(self):
        """
        This method will return True or False indicating whether motion was detected.

        It does this by comparing what it sees in front of it right now with what it saw last time
        and decides whether enough has changed to indicate that motion was detected.
        """
        new_glance = self._have_a_look()

        test_pixel_color = 1  # red=0 green=1 blue=2
        num_changes = 0

        for width in range(self.detection_image_width):
            for height in range(self.detection_image_height):
                # get the delta of the pixel. Conversion to int
                # is required to avoid unsigned short overflow.
                pixel_delta = abs(
                    int(self.last_glance[height][width][test_pixel_color]) -
                    int(new_glance[height][width][test_pixel_color])
                )

                if pixel_delta > self.pix_threshold:
                    num_changes += 1

                    if num_changes > self.max_pix_changes:
                        self.last_glance = new_glance
                        return True

        self.last_glance = new_glance
        return False

    def _have_a_look(self):
        """
        This method uses the camera to take a quick look of what is in front of it and returns
        an rgb array containing the image data
        """
        detection_image_resolution = (self.detection_image_width, self.detection_image_height)

        with picamera.PiCamera(resolution=detection_image_resolution) as camera:
            camera.start_preview()
            time.sleep(2)  # Let camera warm up

            if self.is_daytime:
                camera.exposure_mode = 'auto'
                camera.awb_mode = 'auto'
            else:  # It's night time so take a low-light image
                camera.framerate = Fraction(1, 6)
                camera.shutter_speed = self.night_shutter_speed_micro
                camera.exposure_mode = 'off'
                camera.iso = self.night_iso
                # Give the camera a good long time to measure AWB
                # (you may wish to use fixed AWB instead)
                time.sleep(self.night_awb_timeout)

            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='rgb')

                return stream.array


if __name__ == '__main__':
    detector = MotionDetector()

    print('Checking for motion...')

    while True:
        if detector.motion_detected():
            print('!! MOTION DETECTED !!')
