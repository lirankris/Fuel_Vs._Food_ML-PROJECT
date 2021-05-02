from datetime import date
from currency_converter import CurrencyConverter


def ConvertToUSD(currency, year):
    if currency == 'ARS':
        return 0.036  # ARS - Argentine Peso
    elif currency == 'TWN' or currency == 'TWD':
        return 0.12  # TWD - New Taiwan Dollar
    elif currency == 'CLP':
        return 0.0045  # CLP - Chilean Peso
    elif currency == 'CAD':
        return 0.38  # CLP - Candian Dollar
    elif currency == 'COP':
        return 0.00091  # COP - Colombian peso
    else:
        conv = CurrencyConverter(fallback_on_wrong_date=True)
        return conv.convert(1, 'USD', currency, date=date(year, 9, 1))