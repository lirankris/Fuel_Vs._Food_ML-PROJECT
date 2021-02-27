import os
import datetime


def data2text(data, filename, type=None):

    ToDay = str(datetime.date.today().strftime("%d_%m_%Y"))
    DataBasePath = r"C:\Users\liran\OneDrive\Desktop\School\data scientist\Jhon Bryce\DataBase"
    FileDirName = f"\Data_Set {ToDay}"

    texFilePath = DataBasePath + FileDirName + f'\\testText {ToDay}'
    d2text = os.path.join(texFilePath, f'{filename} {ToDay}.json')

    if type is None:
        with open(d2text, 'w') as f:
            data.to_json(d2text, orient="split")
    else:
        with open(d2text, 'a') as f:
            f.writelines(data)

    return data
