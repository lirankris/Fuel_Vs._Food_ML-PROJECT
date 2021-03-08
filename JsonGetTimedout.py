# Convert all JSON datasets into multi-indexed CSV files

# where to save or read

ERRORS_DIR = 'error_reports'

UNICODE_ERROR_FILE = os.path.join(ERRORS_DIR, 'unicode_errors.csv')
KEY_ERROR_FILE = os.path.join(ERRORS_DIR, 'key_errors.csv')
NO_TIME_PERIOD_FILE = os.path.join(ERRORS_DIR, 'no_time_period.csv')

# unicodeErrorFile = 'error_reports/unicode_errors.csv'
# keyErrorFile = 'error_reports/key_errors.csv'
# noTimePeriodFile = 'error_reports/no_time_period.csv'


# generator of empty lists
def create(n, constructor=list):
    for _ in range(n):
        yield constructor()


# note this function extracts annual data
# DataFrame in long format
def create_df(sdmx_data, use_ids=False):

    series_list = list(sdmx_data.series)

    # does it have a frequency dimension?
    # if only use the annual data
    keycheck_tuple = series_list[0].key._fields                 # noqa
    for keycheck in keycheck_tuple:
        if keycheck == 'FREQUENCY':
            series_list = (anl for anl in sdmx_data.series if anl.key.FREQUENCY == 'A')
            break
        elif keycheck == 'FREQ':
            series_list = (anl for anl in sdmx_data.series if anl.key.FREQ == 'A')
            break

    # variable series key columns for the data set
    # list of empty lists
    key_columns = list(create(sdmx_data._reader._key_len))      # noqa

    # fixed columns for time period and values
    time_period_col = []
    value_col = []

    for s in series_list:
        s_key_tuple = s.key
        s_elem_dict = s._elem                                   # noqa
        s_reader = s._reader                                    # noqa

        obs_dim_dict = s_reader._obs_dim[0]['values']           # noqa

        total_keys = s_reader._key_len                          # noqa
        key_col_codes = []

        for key in range(total_keys):
            keys_list = s_reader._series_dim[key]['values']     # noqa
            key_field_abbrev = s_key_tuple._fields[key]         # noqa
            key_code = s_key_tuple[key_field_abbrev]
            if use_ids:
                key_col_codes.append(key_code)
            else:
                for entry_dict in keys_list:
                    if entry_dict['id'] == key_code:
                        key_col_codes.append(entry_dict['name'])

        obs_dict = s_elem_dict['observations']
        for key, val_list in sorted(obs_dict.items()):
            value_col.append(val_list[0])
            yr = obs_dim_dict[int(key)]['name']
            time_period_col.append(yr)
            for ky in range(sdmx_data._reader._key_len):        # noqa
                key_columns[ky].append(key_col_codes[ky])

    pandasdict = OrderedDict()

    tp = 'Time Period'
    ob = 'Observation'
    if use_ids:
        tp = 'TIME_PERIOD'
        ob = 'OBS'

    pandasdict[tp] = time_period_col
    pandasdict[ob] = value_col

    for t in range(sdmx_data._reader._key_len):                 # noqa
        if use_ids:
            # use this for abbreviated column names
            pandasdict[s_key_tuple._fields[t]] = key_columns[t]             # noqa
        else:
            # use this for un-abbreviated column names
            pandasdict[s_reader._series_dim[t]['name']] = key_columns[t]    # noqa

    oecd_df = pd.DataFrame(pandasdict)
    oecd_df.set_index(tp, inplace=True)

    return oecd_df

    # OECD data
    oecd = Request('OECD')

    # note where pandasdmx fails
    unicodeErrors = []
    keyErrors = []
    noTimePeriod = []
    count, jsonDir = OECD_json_get_all()
    # iterate through each JSON file in the directory and convert it
    for filename in os.listdir(jsonDir):
        if filename.endswith(".json"):
            fname = os.path.splitext(filename)[0]
            try:
                data_response = oecd.data(fromfile=os.path.join(jsonDir, filename))
            except UnicodeDecodeError:
                unicodeErrors.append(fname)
            except KeyError:
                keyErrors.append(fname)
            else:
                data = data_response.data

                if data.dim_at_obs == 'TIME_PERIOD':
                    df = create_df(data, use_ids=False)
                    df.to_json(os.path.join(CSV_DIR, fname + '.csv'))
                else:
                    noTimePeriod.append(fname)

    # log the issues
    unicodeErrorsDF = pd.DataFrame({'UnicodeErrors': unicodeErrors})
    unicodeErrorsDF.set_index('UnicodeErrors', inplace=True)
    unicodeErrorsDF.to_csv(UNICODE_ERROR_FILE)

    keyErrorsDF = pd.DataFrame({'KeyErrors': keyErrors})
    keyErrorsDF.set_index('KeyErrors', inplace=True)
    keyErrorsDF.to_csv(KEY_ERROR_FILE)

    noTimePeriodDF = pd.DataFrame({'NoTimePeriod': noTimePeriod})
    noTimePeriodDF.set_index('NoTimePeriod', inplace=True)
    noTimePeriodDF.to_csv(NO_TIME_PERIOD_FILE)

    print("completed ...")
    print(len(unicodeErrors), 'UnicodeDecodeError')
    print(len(keyErrors), 'KeyError')
    print(len(noTimePeriod), 'NoTimePeriod')


def OECD_json_get_timedout(FilePath, Logger):

    keyNamesFile = 'error_reports/timedout.csv'

    # logging
    logging.basicConfig(filename=LOGFILE, filemode='w', level=logging.DEBUG)
    logging.debug("Log started at %s", str(datetime.datetime.now()))

    # read in list of dataset ids
    datasourceUrl = 'http://stats.oecd.org/sdmx-json/data/'

    dataset_ids_df = pd.read_csv(keyNamesFile)
    dataset_ids = dataset_ids_df['KeyFamilyId'].tolist()

    success_count = 0

    with requests.Session() as s:
        for dataset_id in tqdm(dataset_ids):
            try:
                r = s.get(datasourceUrl + dataset_id + '/all/all', timeout=61)
            except requests.exceptions.ReadTimeout:
                print(dataset_id, ": OECD data request read timed out")
                logging.debug('%s: OECD data request read timed out', dataset_id)
            except requests.exceptions.Timeout:
                print(dataset_id, ": OECD data request timed out")
                logging.debug('%s: OECD data request timed out', dataset_id)
            except requests.exceptions.HTTPError:
                print(dataset_id, ": HTTP error")
                logging.debug('%s: HTTP error', dataset_id)
            except requests.exceptions.ConnectionError:
                print(dataset_id, ": Connection error", )
                logging.debug('%s: Connection error', dataset_id)
            else:
                if r.status_code == 200:
                    # save the json file - don't prettify to save space
                    target = os.path.join(STORE_DIR, dataset_id + ".json")
                    with open(target, 'w', encoding='utf-8') as f:
                        f.write(r.text)
                        success_count += 1
                else:
                    print(dataset_id, 'HTTP Failed with code', r.status_code)
                    logging.debug('%s HTTP Failed with code %d', dataset_id, r.status_code)

    print("completed ...")
    print(len(dataset_ids), " Dataset Ids")
    print(success_count, " datasets retrieved")
    logging.debug("Log ended at %s", str(datetime.datetime.now()))
