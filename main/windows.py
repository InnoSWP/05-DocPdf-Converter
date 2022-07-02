from pathlib import Path
from typing import Dict, List, Union

import env_consts as ec


def convert_windows(
    filepath: str,
    files: List[str],
    converted_file_path: str,
    has_type_in_request: Dict[str, bool],
):
    """
    Windows conversion core.

    :param has_type_in_request: flag of each type in request
    :type has_type_in_request: Dict[str, bool]
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
    doc_opened = False
    doc = None
    try:
        doc = word.Documents.Open(docx_filepath)
        doc_opened = True
        doc.SaveAs(pdf_filepath, FileFormat=pdf_format)
    finally:
        if doc_opened and doc is not None:
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
    sheets_opened = False
    xl_sheets = None
    try:
        xl_sheets = excel.Workbooks.Open(xlsx_filepath)
        sheets_opened = True
        xl_sheets.Worksheets[0].ExportAsFixedFormat(0, pdf_filepath)
    finally:
        if sheets_opened and xl_sheets is not None:
            xl_sheets.Close(True)


def windows(
    paths: Dict[str, Union[bool, str, Path]],
    files: List[str],
    has_type_in_request: Dict[str, bool],
):
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

    word = None
    excel = None
    CoInitializeEx(0)

    # Open word application for conversion.
    docx_type, doc_type, xlsx_type, xls_type = ".docx", ".doc", ".xlsx", ".xls"
    word_types = [doc_type, docx_type]
    excel_types = [xlsx_type, xls_type]

    if any(has_type_in_request[file_type] for file_type in word_types):
        word = w32c.Dispatch("Word.Application")

    # Open excel application for conversion.
    if any(has_type_in_request[file_type] for file_type in excel_types):
        excel = w32c.Dispatch("Excel.Application")

    # Format of PDF file.
    wd_format_pdf = 17

    # Convert each file via word application.
    for file in files:
        document_filepath = f"{paths['input']}{ec.OS_SLASH}{file}"
        pdf_filepath = (
            f"{paths['output']}{ec.OS_SLASH}{Path(document_filepath).stem}.pdf"
        )
        if isinstance(word, w32c.CDispatch) and any(
            file_type in file for file_type in word_types
        ):
            windows_convert_docx(word, document_filepath, pdf_filepath, wd_format_pdf)
        elif isinstance(excel, w32c.CDispatch) and any(
            file_type in file for file_type in excel_types
        ):
            windows_convert_xlsx(excel, document_filepath, pdf_filepath)

    # Close word application.
    if word is w32c.CDispatch:
        word.Quit()

    # Close excel application.
    if excel is w32c.CDispatch:
        excel.Quit()
