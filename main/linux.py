import subprocess
import time
from os import makedirs

import env_consts as ec


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
