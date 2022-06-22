import glob
import io
import os
import time
import zipfile
from mimetypes import MimeTypes

import requests as requests
from rest_framework import status


def main():
    url = "http://127.0.0.1:8000/convert/"
    start = time.time()
    for i in range(25):
        files = [filename for filename in glob.glob("*.docx")]
        files = [
            ("files", (file, open(f"{file}", "rb"), MimeTypes().guess_type(file)))
            for file in files
        ]
        headers = {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"}
        payload = {}
        resp = requests.request(
            "POST", url, headers=headers, data=payload, files=files, stream=True
        )
        if (
            resp.status_code == status.HTTP_400_BAD_REQUEST
            or resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        ):
            print(resp.text)
            return
        zfile = zipfile.ZipFile(io.BytesIO(resp.content))
        zfile.extractall(path=os.path.dirname(__file__))
    print(time.time() - start)


if __name__ == "__main__":
    main()
