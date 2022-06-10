import glob
import os
import requests as requests
import io
import zipfile
from rest_framework import status


def main():
    url = 'http://127.0.0.1:8000/convert/'
    files = [filename for filename in glob.glob('*.docx')]
    print(files)
    files = [
        ('files', (file, open(f'{os.path.dirname(__file__)}/{file}', 'rb'),
                   'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) for file in files
    ]
    headers = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    }
    resp = requests.request("POST", url, headers=headers, data={'files': files}, stream=True)
    if resp.status_code == status.HTTP_400_BAD_REQUEST or resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        print(resp.text)
        return
    zfile = zipfile.ZipFile(io.BytesIO(resp.content))
    zfile.extractall(path=os.path.dirname(__file__))


if __name__ == '__main__':
    main()