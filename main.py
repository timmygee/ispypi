from .motion_detector import MotionDetector
from .still_camera import StillCamera
from .djropbox_uploader import DjropboxUploader

if __name__ == '__main__':
    image_file_path = 'capture.jpg'
    detector = MotionDetector()
    camera = StillCamera(default_file_path=image_file_path)
    uploader = DjropboxUploader()

    print('Checking for motion...')

    while True:
        if detector.motion_detected():
            # Take a high res photo and save it
            camera.shoot()
            # Upload the file. You could do anything you want here with the
            # image file. I upload it to my custom online image repository
            uploader.upload(image_file_path)
