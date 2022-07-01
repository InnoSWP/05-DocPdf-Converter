import subprocess
import time
from mimetypes import MimeTypes
from os import makedirs, path, rename
from os.path import basename
from pathlib import Path
from shutil import copyfileobj
from sys import platform
from zipfile import ZipFile

from django.http import HttpResponse

import env_consts as ec


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
    file_path = (
        f"{path.dirname(__file__)}{ec.OS_SLASH}files{ec.OS_SLASH}{last_id}{ec.OS_SLASH}"
    )
    converted_file_path = get_converted_file_path(last_id)
    makedirs(converted_file_path, exist_ok=True)
    # Allocate new directory if it doesn't exist.
    makedirs(file_path, exist_ok=True)
    # Save each file to file_path directory.
    files_to_convert = []
    for file in files:
        if ".pdf" not in file.name:
            files_to_convert.append(file.name)
            filename = f"{file_path}{file.name}"
        else:
            filename = f"{converted_file_path}{file.name}"
        with open(filename, "wb") as out_file:
            copyfileobj(file, out_file)
    return file_path, files_to_convert


def zip_files_in_dir(filepath: str, files, zip_file_name: str):
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
        rename(
            f'{filepath}{files[0].rsplit(".", 1)[0]}.pdf',
            f"{filepath}{zip_file_name}.pdf",
        )
        return ".pdf"
    with ZipFile(f"{filepath}{zip_file_name}.zip", "w") as zip_obj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zip_obj.write(file_full_name, basename(file_full_name))
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

    with open(f"{file_path}{file_name}", "rb") as file:
        response = HttpResponse(
            file, content_type=f"{MimeTypes().guess_type(file_name)}"
        )
    response["files"] = f"attachment; filename={file_name}"
    return response


def convert(filepath: str, files, index, has_type_in_request):
    """
    Conversion operator that determines the OS, calls suitable
    conversion algorithm, and returns path to them.

    :param has_type_in_request: flag of each type in request
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
    if platform in ("linux", "linux2"):
        convert_linux(filepath, files, converted_file_path, has_type_in_request)
    elif platform == "win32":
        convert_windows(filepath, files, converted_file_path, has_type_in_request)
    return converted_file_path


def convert_windows(
    filepath: str, files, converted_file_path: str, has_type_in_request: dict
):
    """
    Windows conversion core.

    :param has_type_in_request: flag of each type in request
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

    if not files:
        return
    paths = resolve_paths(filepath, converted_file_path)
    windows(paths, files, has_type_in_request)


def windows_convert_docx(word, docx_filepath: str, pdf_filepath: str, pdf_format: int):
    """
    Windows conversion docx part.

    :param word: Word application
    :param docx_filepath: path to docx file
    :type docx_filepath: str
    :param pdf_filepath: path to future pdf file
    :type pdf_filepath: str
    :param pdf_format: pdf format code
    :type pdf_format: int
    """

    doc = word.Documents.Open(docx_filepath)
    doc.SaveAs(pdf_filepath, FileFormat=pdf_format)
    doc.Close(0)


def windows_convert_xlsx(excel, xlsx_filepath: str, pdf_filepath: str):
    """
    Windows conversion xlsx part.

    :param excel: Excel application
    :param xlsx_filepath: path to xlsx file
    :type xlsx_filepath: str
    :param pdf_filepath: path to future pdf file
    :type pdf_filepath: str
    """
    xl_sheets = excel.Workbooks.Open(xlsx_filepath)
    xl_sheets.Worksheets[0].ExportAsFixedFormat(0, pdf_filepath)
    xl_sheets.Close(True)


def windows(paths, files, has_type_in_request: dict):
    """
    Conversion algorithm for Windows OS.

    :param has_type_in_request: flag of each type in request
    :param paths: paths
    :type paths: dict[str, Union[bool, str, Path]]
    :param files: files for conversion
    :type files: list of str
    :return:
    """
    import win32com.client as w32c
    from servicemanager import CoInitializeEx

    CoInitializeEx(0)
    # Open word application for conversion.
    word = None
    excel = None
    if has_type_in_request[".docx"]:
        word = w32c.Dispatch("Word.Application")
    # Open excel application for conversion.
    if has_type_in_request[".xlsx"]:
        excel = w32c.Dispatch("Excel.Application")
    # Format of PDF file.
    wd_format_pdf = 17
    # Convert each file via word application.
    for file in files:
        document_filepath = f"{paths['input']}{ec.OS_SLASH}{file}"
        pdf_filepath = (
            f"{paths['output']}{ec.OS_SLASH}{Path(document_filepath).stem}.pdf"
        )
        if ".docx" in file:
            windows_convert_docx(word, document_filepath, pdf_filepath, wd_format_pdf)
        elif ".xlsx" in file:
            windows_convert_xlsx(excel, document_filepath, pdf_filepath)
    # Close word application.
    if has_type_in_request[".docx"]:
        word.Quit()
    # Close excel application.
    if has_type_in_request[".xlsx"]:
        excel.Quit()


def get_converted_file_path(index: int):
    """
    Function to get converted path via index.
    :param index: index of converted path directory
    :type index: int
    :return: converted path directory
    :rtype: str
    """
    # Path to converted files.
    converted_file_path = (
        f"{path.dirname(__file__)}{ec.OS_SLASH}"
        f"converted_files{ec.OS_SLASH}{index}{ec.OS_SLASH}"
    )
    # Make this directory if it doesn't exist.
    makedirs(converted_file_path, exist_ok=True)
    return converted_file_path


def install_libre():
    """
    install libre on environment
    :return:
    """
    subprocess.run(
        f"echo {ec.SYS_PWD}|sudo -S apt -y update && sudo -S apt -y install libreoffice",
        shell=True,
        check=True,
    )
    ec.INSTALLED_LIBRE = True


def convert_one_linux():
    pass


def convert_linux(filepath: str, files, converted_file_path: str, has_type_in_request):
    """
    Conversion algorithm for Linux-like OS.

    :param has_type_in_request:
    :param converted_file_path: path to output files
    :type converted_file_path: str
    :param filepath: path to input files
    :type filepath: str
    :param files: file names
    :type files: list of str
    :return: path to converted files
    :rtype: str
    """
    start = time.time()
    if not files:
        return
    if not ec.INSTALLED_LIBRE:
        with subprocess.Popen(
            "apt list -a libreoffice",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:
            if "installed" not in process.communicate()[0].decode("utf-8"):
                install_libre()

    command = f"cd {filepath}"
    if has_type_in_request[".docx"]:
        command += f"&& lowriter --headless --convert-to pdf *.docx --outdir {converted_file_path}"
    if has_type_in_request[".xlsx"]:
        command += f"&& lowriter --headless --convert-to pdf *.xlsx --outdir {converted_file_path}"
    makedirs(converted_file_path, exist_ok=True)
    # For all files call lowriter for conversion (LibreOffice).
    # Execute all console commands.
    subprocess.run(command, shell=True, check=True)
    print(time.time() - start)
