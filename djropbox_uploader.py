import os


class DjropboxUploader:
    def __init__(self, host=None, username=None, password=None):
        """
        Initialise the uploader defaults. If username, password and host aren't
        specified grab them from the os environment
        """
        self.host = host if host else os.environ.get('DJROPBOX_HOST')
        self.username = username if username else os.environ.get('DJROPBOX_USERNAME')
        self.password = password if password else os.environ.get('DJROPBOX_PASSWORD')

    def upload(self, file_path):
        """Upload the file"""
        print('Uploading {}'.format(file_path))
        pass
