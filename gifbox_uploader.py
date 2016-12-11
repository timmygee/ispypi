#!/usr/bin/env python3
import os
import requests
import json


def normalise_endpoint(endpoint):
    """
    Nice little method to ensure the right amount of slashes are in every endpoint string
    """
    return '/{}/'.format('/'.join([crumb for crumb in endpoint.split('/') if crumb]))


class GifBoxUploader:
    def __init__(self, host=None, username=None, password=None):
        """
        Initialise the uploader defaults. If username, password and host aren't
        specified grab them from the os environment
        """
        self.host = host if host else os.environ.get('GIFBOX_HOST')
        self.username = username if username else os.environ.get('GIFBOX_USERNAME')
        self.password = password if password else os.environ.get('GIFBOX_PASSWORD')
        self.auth_token = None

    def gen_headers(self):
        headers = {}
        if self.auth_token:
            headers['Authorization'] = 'Token {}'.format(self.auth_token)
        return headers

    def post(self, endpoint, data={}, is_json=True, **kwargs):
        """
        Post the data to the endpoint
        """
        url = '{}{}'.format(self.host, normalise_endpoint(endpoint))
        headers = self.gen_headers()

        if is_json:
            headers['Content-Type'] = 'application/json'
            post_data = json.dumps(data)
        else:
            post_data = data

        return requests.post(url, data=post_data, headers=headers, **kwargs)

    def authenticate(self):
        response = self.post('/obtain-auth-token/', data={
            'username': self.username,
            'password': self.password,
        })
        assert response.status_code == requests.codes.ok
        self.auth_token = response.json()['token']

    def upload(self, file_path):
        """Upload the file"""
        if not self.auth_token:
            # No auth token. Attempt to authenticate
            self.authenticate()

        print('Uploading {}'.format(file_path))

        with open(file_path, 'rb') as file_data:
            response = self.post(
                '/api/images/', is_json=False,
                files={'image': (os.path.basename(file_path), file_data)}
            )
            response.raise_for_status()


if __name__ == '__main__':
    uploader = GifBoxUploader()
    uploader.upload('/some/file/path')
