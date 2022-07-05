import time
from mimetypes import MimeTypes

import requests as requests
from rest_framework import status


def main():
    url = "http://127.0.0.1:8000/convert/"
    filess = ["1.doc", "2.docx", "3.docx", "4.docx"]
    files = []
    for file in filess:
        files.append(
            (
                "files",
                (
                    file,
                    open(f"{file}", "rb"),
                    MimeTypes().guess_type(file),
                ),
            )
        )
    resp = requests.request(
        "POST",
        url,
        files=files,
        stream=True,
    )
    print(resp.json())
    if resp.status_code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        print(resp.text)
        return


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
