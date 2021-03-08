import os
import pandas as pd
import requests as req
import xmltodict
import lxml.etree as etree


def OECD_Key_Familis(Url, KeynamesFILE, Logger, MainPath):

    Logger.warning('Starting to reach OECD key Family names')

    # Create a loop for a Session in the OECD Site (OecdStructureUrl) to get
    # the key family id's to reach all the data from OecdsourceUrl.

    # Url = 'http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/'
    # KeynamesFILE (write)= ....'\OECD_key_names {ToDay}.json'
    # Logger = Oecd_log.

    # In: data from OECD server.
    # Out: OECD_keys/OECD_key_names.json

    try:
        GetRequest = req.get(Url, timeout=60)
    except req.exceptions.ReadTimeout:
        print("Data request read timed out")
        Logger.debug('Data read timed out')
    except req.exceptions.Timeout:
        print("Data request timed out")
        Logger.debug('Data request timed out')
    except req.exceptions.HTTPError:
        print("HTTP error")
        Logger.debug('HTTP error')
    except req.exceptions.ConnectionError:
        print("Connection error")
        Logger.debug('Connection error')
    else:
        if GetRequest.status_code == 200:
            # the request was received and understood and is being processed (Http code = 200).
            keyFamIdList = []  # key Family Id, example: QNA, OECD_TSE2010, AEO11_OVERVIEW_CHAPTER1_TAB1_PT,
            keyFamNameList = []  # key Family Name, example :
            keyfamilies_dict = xmltodict.parse(GetRequest.text)
            keyFamilies = keyfamilies_dict['message:Structure']['message:KeyFamilies']['KeyFamily']
            # <message:Structure>
            #       <message:KeyFamilies>
            #           <KeyFamily>
            #               **keyFamily**
            #           </KeyFamily>
            #       </message:KeyFamilies>
            # </message:Structure>
            # cf(Pos='text', FileName=f'{OECD_Key_Familis.__name__} - keyFamilies ',
            #   level=0, data=keyFamilies)
            for keyF in keyFamilies:
                keyfam_id = keyF['@id']
                keyFamIdList.append(keyfam_id)
                keyNames = keyF['Name']
                #  checking if keyNames is a list or a dictionary:
                if isinstance(keyNames, list):
                    for keyN in keyNames:
                        try:
                            keyfam_lang = keyN['@xml:lang']
                            # example:    <xs:documentation xml:lang="en">Experimental value</xs:documentation>
                            # Insert family keyfam_text the text for the given keyNames.
                            if keyfam_lang == 'en':  # if the language is english.
                                # get a object name, example: Information, communication.
                                keyfam_text = keyN['#text']
                                keyFamNameList.append(keyfam_text)
                        except KeyError:
                            Logger.debug(f"No @xml:lang/#text key in {keyN}")

                        Logger.debug(
                            f'\nThis is the key famly id: {keyfam_id}. \n and name list: {keyfam_text}!')

                elif isinstance(keyNames, dict):
                    try:
                        keyfam_lang = keyNames['@xml:lang']  # get a language.
                        if keyfam_lang == 'en':   # if the language is english.
                            # Insert family keyfam_text the text for the given keyNames.
                            keyfam_text = keyNames['#text']
                            keyFamNameList.append(keyfam_text)
                    except KeyError:
                        Logger.debug(f"No @xml:lang/#text key in {keyNames}")

                Logger.debug(
                    f'\nThis is the key famly id: {keyfam_id}. \n and name list: {keyfam_text}!')
            # Create data frame with the index of key Family Id and key Family Name.
            keyFamdf = pd.DataFrame.from_dict(
                {'KeyFId': keyFamIdList, 'KeyFName': keyFamNameList}, orient='index')
            keyFamdf.to_json(KeynamesFILE, orient="index")
            keyFamdf.to_excel(excel_writer=f"{MainPath}\keyFamdf.xlsx", na_rep="0",
                              header=["KeyFId", "KeyFName"])
            Logger.debug("finished creating key Family as a json file.")
            Logger.info(f"key Family file path is: {KeynamesFILE}")
            return True

        else:
            print('HTTP Failed', GetRequest.status_code)
            Logger.debug('HTTP Failed with code %d', GetRequest.status_code)
            return False


'/////////////////////////////////////////////////////////////////////////////'


def OECD_Schema(Url, Path, keynames, Logger):

    # Create a for loop with for a Session in the OECD Site to get xml schema files.

    # Url = 'http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/'
    # KeynamesFILE (read)= ....'\OECD_key_names {ToDay}.json'
    # Path (write)= file directory of OECD_Schema path.
    # keynames = List of 'Key Family Id' such as: 'QNA', 'SNA_TABLE11'.
    # Logger = Oecd_log.

    # In: data from OECD server; OECD_keys/OECD_key_names.json
    # Out: OECD_schema/dataset id.xml

    success_count = 0  # Reset the count of success in attempts of requests.

    Logger.warning('Starting to reach out Oecd Data source for xml schema')

    with req.Session() as ReqS:
        for keyname in keynames:
            try:
                GetRequest = ReqS.get(Url + keyname, timeout=60)
                # example request: http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/QNA

            except req.exceptions.ReadTimeout:
                print(keyname, ": Data request read timed out")
                Logger.debug('%s: Data read timed out', keyname)
            except req.exceptions.Timeout:
                print(keyname, ": Data request timed out")
                Logger.debug('%s: Data request timed out', keyname)
            except req.exceptions.HTTPError:
                print(keyname, ": HTTP error")
                Logger.debug('%s: HTTP error', keyname)
            except req.exceptions.ConnectionError:
                print(keyname, ": Connection error")
                Logger.debug('%s: Connection error', keyname)

            else:
                if GetRequest.status_code == 200:  # success to get Keys.
                    write2file = os.path.join(Path, 'OECD_Schema' + ' ' + keyname + ".xml")
                    tree = etree.fromstring(GetRequest.text)
                    pretty_xml_str = etree.tostring(tree, pretty_print=True).decode("utf-8")

                    # write to a new text file all the schema data.
                    with open(write2file, 'w', encoding='utf-8') as f:
                        f.write(pretty_xml_str)
                        success_count += 1
                else:
                    print(keyname, GetRequest.status_code)
                    Logger.debug('%s HTTP Failed with code %d',
                                 keyname, GetRequest.status_code)

    return success_count, write2file


'/////////////////////////////////////////////////////////////////////////////'


def OECD_json_get_all(Url, Path, keynames, Logger):

    # Create a for loop with for a Session in the OECD Site to get sdmx-json files.

    # Url = 'http://stats.oecd.org/sdmx-json/data/'
    # KeynamesFILE (read)= ....'\OECD_key_names {ToDay}.json'
    # Path (write)= file directory of OECD_json_get_all path.
    # keynames = List of 'Key Family Id' such as: 'QNA', 'SNA_TABLE11'.
    # Logger = Oecd_log.

    # In: data from OECD server; OECD_keys/OECD_key_names.json
    # Out: OECD_json_datasets/dataset id.json

    Logger.warning('Starting to reach out Oecd Data source for json_get_all')

    success_count = 0  # Reset the count of success in attempts of requests.

    with req.Session() as ReqS:
        for dataset_id in keynames:
            try:
                GetRequest = ReqS.get(Url + dataset_id + '/all/all', timeout=60)
                # example request: http://stats.oecd.org/sdmx-json/data/QNA/all/all
            except req.exceptions.ReadTimeout:
                print(dataset_id, ": OECD data request read timed out")
                Logger.debug('%s: OECD data request read timed out', dataset_id)
            except req.exceptions.Timeout:
                print(dataset_id, ": OECD data request timed out")
                Logger.debug('%s: OECD data request timed out', dataset_id)
            except req.exceptions.HTTPError:
                print(dataset_id, ": HTTP error")
                Logger.debug('%s: HTTP error', dataset_id)
            except req.exceptions.ConnectionError:
                print(dataset_id, ": Connection error", )
                Logger.debug('%s: Connection error', dataset_id)
            else:
                if GetRequest.status_code == 200:  # success to get dataset.
                    write2file = os.path.join(Path, dataset_id + ".json")

                    # write to a new text file of the source data.
                    with open(write2file, 'w', encoding='utf-8') as file:
                        file.write(GetRequest.text)
                        success_count += 1

                else:
                    print(dataset_id, 'HTTP Failed with code', GetRequest.status_code)
                    Logger.debug('%s HTTP Failed with code %d',
                                 dataset_id, GetRequest.status_code)

    print(f'{success_count} HTTP success out of {len(keynames)}, Total {len(keynames)-success_count} Failed')

    return success_count, write2file
