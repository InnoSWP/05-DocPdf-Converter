from os import makedirs, path
from pathlib import Path
from zipfile import ZipFile
from sys import platform
import subprocess
from os.path import basename
from shutil import copyfileobj
from django.http import HttpResponse
from mimetypes import MimeTypes


# Allocate new directory for the files and save them there.
def save_files(files: [str], last_id: int):
    # File path to saving files.
    file_path = f'{path.dirname(__file__)}/files/{last_id}/'
    # Allocate new directory if it doesn't exist.
    makedirs(file_path, exist_ok=True)
    # Save each file to file_path directory.
    for file in files:
        filename = f'{file_path}{file.name}'
        with open(filename, 'wb') as out_file:
            copyfileobj(file, out_file)
    return file_path


# Zip all files in given directory.
def zip_files_in_dir(filepath: str, files: [str], zip_file_name: str):
    with ZipFile(f'{filepath}{zip_file_name}', 'w') as zipObj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zipObj.write(file_full_name, basename(file_full_name))


# Form the file response for files in given directory and return it.
def get_file_response(converted_file_path: str, file_name: str):
    with open(f'{converted_file_path}{file_name}', 'rb') as file:
        response = HttpResponse(file, content_type=f'{MimeTypes().guess_type(file_name)}')
    response['files'] = f'attachment; filename={file_name}'
    return response


# Conversion operator that determines the OS, calls suitable
# conversion algorithm, and returns path to them.
def convert(filepath: str, files: [str], index):
    if platform == "linux" or platform == "linux2":
        return convert_linux(filepath, files, index)
    elif platform == "win32":
        return convert_windows(filepath, files, index)


# Conversion algorithm for Windows OS.
def convert_windows(filepath: str, files: [str], index: int):
    from docx2pdf import resolve_paths
    if not len(files):
        return []
    converted_file_path = f'{path.dirname(__file__)}/converted_files/{index}/'
    makedirs(converted_file_path, exist_ok=True)
    paths = resolve_paths(filepath, converted_file_path)
    windows(paths)
    return converted_file_path


# Windows conversion docx part.
def windows_convert_docx(word, docx_filepath: Path, pdf_filepath: Path, pdf_format: int):
    doc = word.Documents.Open(str(docx_filepath))
    doc.SaveAs(str(pdf_filepath), FileFormat=pdf_format)
    doc.Close(0)


# Windows conversion core.
def windows(paths):
    import win32com.client as w32c
    from servicemanager import CoInitializeEx
    CoInitializeEx(0)
    # Open word application for conversion.
    word = w32c.Dispatch("Word.Application")
    # Format of PDF file.
    wd_format_pdf = 17
    if paths["batch"]:
        # Convert each file via word application.
        for docx_filepath in Path(paths["input"]).glob("*.docx"):
            pdf_filepath = Path(paths["output"]) / f'{docx_filepath.stem}.pdf'
            windows_convert_docx(word, docx_filepath, pdf_filepath, wd_format_pdf)
    else:
        docx_filepath = Path(paths["input"]).resolve()
        pdf_filepath = Path(paths["output"]).resolve()
        # Convert file via word application.
        windows_convert_docx(word, docx_filepath, pdf_filepath, wd_format_pdf)
    # Close word application.
    word.Quit()


# Conversion algorithm for Linux-like OS.
def convert_linux(filepath: str, files: [str], index: int):
    if not len(files):
        return []
    # Path to converted files.
    converted_file_path = f'{path.dirname(__file__)}/converted_files/{index}/'
    cmd = f'cd {filepath}'
    # Make this directory if it doesn't exist.
    makedirs(converted_file_path, exist_ok=True)
    # For all files call lowriter for conversion (LibreOffice).
    for file in files:
        cmd += f' && lowriter --convert-to pdf {file} --outdir {converted_file_path}'
    # Execute all console commands.
    subprocess.call(cmd, shell=True)
    return converted_file_path
