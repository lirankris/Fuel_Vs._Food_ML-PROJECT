import os


def DivideByContinents(df):
    filespath = r'D:\DataBase\Analyze\continents'
    filelist = os.listdir(filespath)
    continents = {}

    df_countrys = list(df[0])

    for file in filelist:
        with open(f'{filespath}\\{file}', 'r',
                  encoding="utf8") as f:  # open text file with all the countries per continent.
            countries = []
            for c in f.readlines():
                country = c.split("\n")[0]
                if country in df_countrys:  # if country from text file in df.
                    countries.append(country)
            continents[(str(file).split('.')[
                0]).lower()] = countries  # add all the countries per continent to the dataset continents.
    return continents