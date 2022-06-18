from os import makedirs, path
from pathlib import Path
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
        convert_windows(filepath, files, index)


def windows(paths):
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    wd_format_pdf = 17

    if paths["batch"]:
        for docx_filepath in sorted(Path(paths["input"]).glob("*.docx")):
            pdf_filepath = Path(paths["output"]) / (str(docx_filepath.stem) + ".pdf")
            doc = word.Documents.Open(str(docx_filepath))
            doc.SaveAs(str(pdf_filepath), FileFormat=wd_format_pdf)
            doc.Close(0)
    else:
        docx_filepath = Path(paths["input"]).resolve()
        pdf_filepath = Path(paths["output"]).resolve()
        doc = word.Documents.Open(str(docx_filepath))
        doc.SaveAs(str(pdf_filepath), FileFormat=wd_format_pdf)
        doc.Close(0)


def convert_windows(filepath: str, files: [str], index: int):
    from docx2pdf import resolve_paths
    if not len(files):
        return []
    converted_file_path = f'{path.dirname(__file__)}/converted_files/{index}/'
    makedirs(converted_file_path, exist_ok=True)
    paths = resolve_paths(filepath, converted_file_path)
    windows(paths)


def convert_linux(filepath: str, files: [str], index: int):
    if not len(files):
        return []
    converted_file_path = f'{path.dirname(__file__)}/converted_files/{index}/'
    
    # Added installing the needed package(if not installed yet) or checking for and installing updates(if avaiable))

    cmd = f'cd {filepath} && sudo apt-get install unoconv'
    makedirs(converted_file_path, exist_ok=True)
    for file in files:
        #cmd += f' && lowriter --convert-to pdf {file} --outdir {converted_file_path}'

        #changed the convertion way

        cmd += f' && doc2pdf {file}'
        subprocess.call(cmd, shell=True)
    return converted_file_path
