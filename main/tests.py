import os
import requests as requests
import io
import zipfile

url = 'http://127.0.0.1:8000/convert/'
files = ["A1.docx", "A2.docx"]
payload = {}
files = [
    ('files', (file, open(f'{os.path.dirname(__file__)}/{file}', 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')) for file in files
]
headers = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
}
resp = requests.request("POST", url, headers=headers, data=payload, files=files, stream=True)
resp.raise_for_status()
zfile = zipfile.ZipFile(io.BytesIO(resp.content))
zfile.extractall(path=os.path.dirname(__file__))
