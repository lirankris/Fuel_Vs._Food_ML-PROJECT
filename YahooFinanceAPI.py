
import time
import datetime
import math
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException


def ClickExchange(elementNames, Logger):

    ExchangePath = {}

    for eleName in elementNames:
        eName = eleName.text.strip()
        ExchangePath[eName] = eleName

        if ['NasdaqGS', 'NYSE', 'Nasdaq'] not in eName:
            Logger.debug(f"***Clicking on the Exchange rate {eName} check box\n")
            ExchangePath[eName].click()

        else:
            continue


'/////////////////////////////////////////////////////////////////////////////'


def GetDate(NextPageButton, findElement, SecName, YahooFinanceFilepath,
            browser, Logger):

    Logger.info("*"*20 + 'Starting to get data from tables' + "*"*20 + '\n\n')

    # get the above line of the table.
    MatchingStocksNum = findElement['xpath'](
        '//*[@id="fin-scr-res-table"]/div[1]/div[1]/span[2]/span').text
    ResultNum = int(MatchingStocksNum.split()[2])  # get the number of stocks.
    PageNum = math.floor(ResultNum/25)  # get the number of pages.
    Logger.debug(f'***There is: {ResultNum} stock results in his sector.\n')
    Data = []

    # source of the table data.
    selector = '#scr-res-table > div.Ovx\(a\).Ovx\(h\)--print.Ovy\(h\).W\(100\%\) > table > tbody'
    count = 0

    try:

        for page in range(PageNum):  # get data from each page until the last page.

            TableSelect = findElement['selector'](selector).text  # get the first page table data.
            Logger.debug(f'{SecName} page number: {page+1}')
            DataInRows = TableSelect.split('\n')  # split list of values to list.
            Symbol = DataInRows[:len(DataInRows):2]  # get all the stock keys values per page.
            status = DataInRows[1::2]  # get all the stock content values per page.

            for r in range(len(Symbol)):  # combain the Symbol and the status.
                RowData = [Symbol[r], status[r]]
                Data.append(RowData)
                count = + 1

            time.sleep(1)
            Logger.debug(f'***Going to next Page {page+2}')
            NextPageButton.click()  # go to next page.
            time.sleep(1)

    except StaleElementReferenceException as Serr:
        Logger.info(f'Probaly Unable to load Screener {Serr}')
        Logger.debug('element is not attached to the page document')
        Logger.debug('Trying again next time...')

    except IndexError as Ierr:
        Logger.debug(f'End of the loop of the bad url {Ierr}')

    finally:
        print(count, SecName)
        Logger.debug(f'\nThe total result that were gathered is:\t {int(ResultNum)}')
        Logger.warning(
            f'The is a gape of {int(ResultNum - count)} between the table results and the gathered Data. \n' + "\\"*300)
        # call the create json format file function.
        return JsonFormatPerSector(Data, SecName, YahooFinanceFilepath, Logger)


'/////////////////////////////////////////////////////////////////////////////'


def JsonFormatPerSector(StocksTable, SecName, YahooFinanceFilepath, Logger):
    Logger.info('Creating a json format file so store data\n\n')

    ToDay = str(datetime.date.today().strftime("%d_%m_%Y"))  # get the date to add to the file name.

    # create data frame of all the table data.
    df = pd.DataFrame(StocksTable, columns=['Symbol', 'status'])
    pd.DataFrame.drop_duplicates(df)  # delete duplicates.
    path = YahooFinanceFilepath
    FileName = f'\\{SecName} {ToDay}.json'

    df.to_json(path+FileName, orient="index")
    Logger.debug(f'A json File was created: {FileName} \n  in the path: {path}')

    return df


'/////////////////////////////////////////////////////////////////////////////'


def YahooFinanceAPI(Filepath, browser, Logger):

    # site action buttons click.
    buttons = {
        'edit_button': '//*[@id="screener-criteria"]/div[2]/div[1]/div/button[1]',
        'find_Stocks_button': "//button[@data-test='find-stock']",
        'Industries': '/html/body/div[1]/div/div/div[1]/div/div[1]/div[2]/div[1]/div/div/div/div[1]/div/div/div/nav/div/div/div/div[3]/div/nav/ul/li[8]/a',
        'add_sector': '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[5]/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/ul/li[2]/div/div',
        'add_exchange': '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[3]/div/div[2]/ul/li[4]/div/div',
        'next': '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[2]/button[3]'
    }

# site path to action buttons.
    findElement = {
        'xpath': browser.find_element_by_xpath,
        'Sxpath': browser.find_elements_by_xpath,
        'tag_name': browser.find_element_by_tag_name,
        'Stag_name': browser.find_elements_by_tag_name,
        'selector': browser.find_element_by_tag_name,
        'Sselector': browser.find_elements_by_tag_name
    }

    # sector_select_list_checkbox
    Yahoo_url = {
        'YTurl': 'https://finance.yahoo.com/sector/ms_technology',
        # 'YRurl' : 'https://finance.yahoo.com/sector/ms_Real_Estate',
        'YHurl': 'https://finance.yahoo.com/sector/ms_Healthcare',
        'YIurl': 'https://finance.yahoo.com/sector/ms_Industrials',
        # 'YEurl' : 'https://finance.yahoo.com/sector/ms_Energy'
    }

    dfTotal = []

    UrlNames = Yahoo_url.keys()
    Logger.info("Yahoo url's: \n")
    [Logger.info(f'{Yahoo_url[key]}\n') for key in UrlNames]

    try:

        Logger.info("***Starting the Yahoo url's Data Extruction Process:\n\n")
        for url in UrlNames:

            Logger.debug("\\"*10 + f"Getting Yahoo url: \t {Yahoo_url[url]} " + "\\"*10 + '\n')
            browser.get(Yahoo_url[url])

            SecName = Yahoo_url[url].split('/')[4].replace('ms_', '')
            Logger.info(f"***Sector Name: {SecName}**\n")

            time.sleep(4)

            try:
                Logger.warning("***Clicking on the Edit button:\n")
                Editbutton = findElement['xpath'](buttons['edit_button'])  # Start the filiteing.
                Editbutton.click()

            except Exception as err:
                Logger.error(f'Got an {err} error.')
                Logger.debug('Clicking on the Edit button failed, trying again!')
                time.sleep(2)
                Editbutton.click()

            time.sleep(1)

            Logger.warning("***Clicking on the Add Exchange button:\n")
            # Find the edit button to start.
            AddExchangeButton = findElement['xpath'](buttons['add_exchange'])
            AddExchangeButton.click()

            time.sleep(2)

            Logger.debug("***Selecting all Exchange rates:\n")
            elementNames = findElement['Sxpath']('//*[@id="dropdown-menu"]/div/div/ul/li/label')
            for elem in elementNames[2:]:
                elem.click()

            time.sleep(4)

            try:
                Logger.warning("**Clicking on the Find Stocks button:\n")
                # Find Stocks button to show stocks.
                FindStocksButton = findElement['xpath'](buttons['find_Stocks_button'])
                FindStocksButton.click()  # click Find Stocks button to show stocks.

                time.sleep(2)

                Logger.debug("**Getting Next Page Button web element\n")
                # next page button to show stocks.
                NextPageButton = findElement['xpath'](buttons['next'])

            except Exception as err:
                print(f"This sector ({SecName}) data Extruction failed: {err}!!")

            Logger.info('***Calling GetDate function')
            # extract data from page in Technology_sector.
            dfTotal.append(GetDate(NextPageButton, findElement,
                                   SecName, Filepath, browser, Logger))
            Logger.info(f'There is {len(dfTotal)} set of sector data in the system!\n\n')

    except Exception as err:
        Logger.error(f"This is the error: {err}")
        Logger.critical('Script failed!')

    else:
        Logger.info("Finished YahooFinanceAPI")
