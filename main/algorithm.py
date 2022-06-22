from os import makedirs, path, rename
from pathlib import Path
from zipfile import ZipFile
from sys import platform
import subprocess
from os.path import basename
from shutil import copyfileobj, copyfile
from django.http import HttpResponse
from mimetypes import MimeTypes


def save_files(files, last_id: int):
    """
    Allocate new directory for the files and save them there.

    :param files: file names
    :type files: list of files
    :param last_id: index for filepath
    :type last_id: int
    :return:
    """

    # File path to saving files.
    file_path = f'{path.dirname(__file__)}/files/{last_id}/'
    converted_file_path = get_converted_file_path(last_id)
    makedirs(converted_file_path, exist_ok=True)
    # Allocate new directory if it doesn't exist.
    makedirs(file_path, exist_ok=True)
    # Save each file to file_path directory.
    for file in files:
        if ".pdf" not in file.name:
            filename = f'{file_path}{file.name}'
        else:
            filename = f'{converted_file_path}{file.name}'
        with open(filename, 'wb') as out_file:
            copyfileobj(file, out_file)
    return file_path


def zip_files_in_dir(filepath: str, files: [str], zip_file_name: str):
    """
    Zip all files in given directory.

    :param filepath: path to input files
    :type filepath: str
    :param files: file names
    :type files: list of str
    :param zip_file_name: name of zip file
    :type zip_file_name: str
    :return file_format
    :rtype string
    """
    if len(files) == 1:
        rename(f'{filepath}{files[0].rsplit(".", 1)[0]}.pdf', f'{filepath}{zip_file_name}.pdf')
        return ".pdf"
    with ZipFile(f'{filepath}{zip_file_name}.zip', 'w') as zipObj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zipObj.write(file_full_name, basename(file_full_name))
    return ".zip"


def get_file_response(file_path: str, file_name: str):
    """
    Form the file response for files in given directory and return it.

    :param file_path: path to input files
    :type file_path: str
    :param file_name: name of file
    :type file_name: str
    :return: response object
    :rtype: :class:`django.http.response.HttpResponse`
    """

    with open(f'{file_path}{file_name}', 'rb') as file:
        response = HttpResponse(file, content_type=f'{MimeTypes().guess_type(file_name)}')
    response['files'] = f'attachment; filename={file_name}'
    return response


def sieve(file_names: [str], index: int):
    convert_files = []
    pdf_files = []
    for file in file_names:
        if ".pdf" not in file:
            convert_files.append(file)
        else:
            pdf_files.append(file)
    return convert_files


def convert(filepath: str, files: [str], index):
    """
    Conversion operator that determines the OS, calls suitable
    conversion algorithm, and returns path to them.

    :param filepath: path to input files
    :type filepath: str
    :param files: file names
    :type files: list of str
    :param index: index for filepath
    :type index: int
    :return: path to converted files
    :rtype: str
    """
    converted_file_path = get_converted_file_path(index)
    if platform == "linux" or platform == "linux2":
        convert_linux(filepath, files, converted_file_path)
    elif platform == "win32":
        convert_windows(filepath, files, converted_file_path)
    return converted_file_path


def convert_windows(filepath: str, files: [str], converted_file_path: str):
    """
    Windows conversion core.

    :param converted_file_path: path to output files
    :type converted_file_path: str
    :param filepath: path to input files
    :type filepath: str
    :param files: file names
    :type files: list of str
    :return: path to converted files
    :rtype: str
    """

    from docx2pdf import resolve_paths
    if not len(files):
        return []
    paths = resolve_paths(filepath, converted_file_path)
    windows(paths)


def windows_convert_docx(word, docx_filepath: Path, pdf_filepath: Path, pdf_format: int):
    """
    Windows conversion docx part.

    :param word: Word application
    :param docx_filepath: path to docx file
    :type docx_filepath: :class:`Path(PurePath)`
    :param pdf_filepath: path to future pdf file
    :type pdf_filepath: :class:`Path(PurePath)`
    :param pdf_format: pdf format code
    :type pdf_format: int
    """

    doc = word.Documents.Open(str(docx_filepath))
    doc.SaveAs(str(pdf_filepath), FileFormat=pdf_format)
    doc.Close(0)


def windows(paths):
    import win32com.client as w32c
    from servicemanager import CoInitializeEx
    """
    Conversion algorithm for Windows OS.

    :param paths: paths
    :type paths: dict[str, Union[bool, str, Path]]
    """

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


def get_converted_file_path(index: int):
    """
    Function to get converted path via index.
    :param index: index of converted path directory
    :type index: int
    :return: converted path directory
    :rtype: str
    """
    # Path to converted files.
    converted_file_path = f'{path.dirname(__file__)}/converted_files/{index}/'
    # Make this directory if it doesn't exist.
    makedirs(converted_file_path, exist_ok=True)
    return converted_file_path


def convert_linux(filepath: str, files: [str], converted_file_path: str):
    """
    Conversion algorithm for Linux-like OS.

    :param converted_file_path: path to output files
    :type converted_file_path: str
    :param filepath: path to input files
    :type filepath: str
    :param files: file names
    :type files: list of str
    :return: path to converted files
    :rtype: str
    """
    if not len(files):
        return []
    cmd = f'cd {filepath}'
    # For all files call lowriter for conversion (LibreOffice).
    for file in files:
        cmd += f' && lowriter --convert-to pdf {file} --outdir {converted_file_path}'
    # Execute all console commands.
    subprocess.call(cmd, shell=True)
    return converted_file_path
