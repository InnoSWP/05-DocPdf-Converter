from zipfile import ZipFile
from os.path import basename


def zip_files_in_dir(filepath: str, files: [str], zip_file_name: str):
    with ZipFile(f'{filepath}{zip_file_name}', 'w') as zipObj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zipObj.write(file_full_name, basename(file_full_name))

from msilib import Directory
from sys import platform, stdout

import subprocess
import shlex
from unittest import result

from zipfile import ZipFile
from os.path import basename


def zip_files_in_dir(filepath: str, files: [str], zip_file_name: str):
    with ZipFile(f'{filepath}{zip_file_name}', 'w') as zipObj:
        for file in files:
            file_full_name = f'{filepath}{file.rsplit(".", 1)[0]}.pdf'
            zipObj.write(file_full_name, basename(file_full_name))

def convert_Lnx(files):
    # ��� ������ ������� ����������
    if (len(files) == 0):
        # ���� ������ ������ - ������ ���-��
        print('Come back soon...')
    else:
        # ���� �� ������ - �������� ���� �� ������
        # P.S. ��� �� ������ ��� ��� � �� ���� �� �����
        directory = files[0][0:files[0].rfind('/')]

        # debugging thing
        print(directory)

        # ������ � �������
        cmd = 'cd ' + directory
        for i in range (len(files)):
            f_name = files[i][files[i].rfind('/') + 1:]
            # � ��� ������� ����� �� ������ ��������� ����������� � ������� ��������
            cmd += ' && lowriter --convert-to pdf ' + f_name + ' && rm ' + f_name

            # �������������� ���� �� ������ ��� ����������� �����
            files[i] = files[i][0:files[i].rfind('.')] + '.pdf'

        # �������� �������� �������� ���������� ������
        result = subprocess.call(cmd, shell = True)

        # �� � ���������� ����� ������
        return files



# � �� ����� �� main ... ���� ���, �� �����

def main():
    if platform == "linux" or platform == "linux2":

        convert_Lnx()
        print("Hello Linux User")

    elif platform == "win32":
        # ��� ���-�� �����
        print("Hello Windows User")

main()
