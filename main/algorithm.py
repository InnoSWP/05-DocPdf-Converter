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
    # тут узнаем рабочую директорию
    if (len(files) == 0):
        # если пустой список - делаем что-то
        print('Come back soon...')
    else:
        # если не пустой - получаем путь до файлов
        # P.S. тут мб ошибки так как я не шарю за питон
        directory = files[0][0:files[0].rfind('/')]

        # debugging thing
        print(directory)

        # входим в каталог
        cmd = 'cd ' + directory
        for i in range (len(files)):
            f_name = files[i][files[i].rfind('/') + 1:]
            # и для каждого файла из списка процессим конвертацию и удаляем исходник
            cmd += ' && lowriter --convert-to pdf ' + f_name + ' && rm ' + f_name

            # перенаправляем пути на только что сгенеренные файлы
            files[i] = files[i][0:files[i].rfind('.')] + '.pdf'

        # сгенерив комманду передаем полномочия модулю
        result = subprocess.call(cmd, shell = True)

        # ну и фозвращаем новый список
        return files



# я хз нужен ли main ... если нет, то ладно

def main():
    if platform == "linux" or platform == "linux2":

        convert_Lnx()
        print("Hello Linux User")

    elif platform == "win32":
        # тут что-то будет
        print("Hello Windows User")

main()
