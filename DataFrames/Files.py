import os


def Get_Files(path, file_names):
    files = os.listdir(path)
    FileToAna = []

    for f in file_names:
        for file in files:
            if f in file:
                FileToAna.append(f'{path}\\{file}')
            if len(FileToAna) == 3:
                break

    return FileToAna[0], FileToAna[1], FileToAna[2]