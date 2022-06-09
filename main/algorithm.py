from os import makedirs, path
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
        return convert_linux(filepath, files, index)
    elif platform == "win32":
        pass


def convert_linux(filepath: str, files: [str], index: int):
    if not len(files):
        return []
    else:
        converted_file_path = f'{path.dirname(__file__)}/converted_files/{index}/'
        cmd = f'cd {filepath}'
        makedirs(converted_file_path, exist_ok=True)
        for file in files:
            cmd += f' && lowriter --convert-to pdf {file} --outdir {converted_file_path}'
        subprocess.call(cmd, shell=True)
    return converted_file_path
