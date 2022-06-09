from zipfile import ZipFile
from os.path import basename


def zip_files_in_dir(filepath: str, files: [str], zip_file_name: str):
    with ZipFile(f'{filepath}{zip_file_name}', 'w') as zipObj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zipObj.write(file_full_name, basename(file_full_name))


def convert(files):
    return files
