from zipfile import ZipFile
from sys import platform
import subprocess
from os.path import basename


def zip_files_in_dir(filepath: str, files: [str], zip_file_name: str):
    with ZipFile(f'{filepath}{zip_file_name}', 'w') as zipObj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zipObj.write(file_full_name, basename(file_full_name))


def convert(filepath: str, files: [str], index):
    if platform == "linux" or platform == "linux2":
        convert_linux(filepath, files, index)

    elif platform == "win32":
        pass


def convert_linux(filepath: str, files: [str], index: int):
    if not len(files):
        return []
    else:
        cmd = f'cd {filepath}converted_files/{index}/'
        for file in files:
            cmd += f' && lowriter --convert-to pdf {file} && rm file_name'
        subprocess.call(cmd, shell=True)

