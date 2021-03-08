import os
import datetime


def data2text(data, dirname, filename, type=None):

    ToDay = str(datetime.date.today().strftime("%d_%m_%Y"))
    DataBasePath = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase\Analyze"

    texFilePath = DataBasePath + f'\\testText {ToDay}'

    if type is None:
        d2text = os.path.join(texFilePath, f'{filename} {ToDay}.txt')
        with open(d2text, 'w') as f:
            f.writelines(data)

    else:
        d2text = os.path.join(texFilePath, f'{filename} {ToDay}.json')
        with open(d2text, 'a') as f:
            data.to_json(d2text, orient="split")
