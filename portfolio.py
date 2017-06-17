#!/usr/bin/env python3
"""
Some toy code that reads in a CSV file of ticker symbols and the desired
fraction of each in an investment portfolio. After specifying the total
cash available to invest and currency using the parameters below, the
script uses Yahoo! Finance to retrieve share prices and (if necessary)
a currency exchange rate. Given the desired fraction of each share in the
portfolio, the script determines the quantity of shares to buy.
"""
import csv
import json
import numpy as np
from yahoo_finance import Share
from yahoo_finance import Currency

__author__ = "Mikhail Klassen"
__version__ = "0.1.0"
__license__ = "MIT"

STOCK_RATIO_FILE = 'stock_ratios.csv'
CURRENCY = 'CAD'
TOTAL_CASH = 10000.0 

def main():
    """ Reads in a CSV file specifying the portfolio of stocks
    and their respective ratios within the portfolio."""
    stocks = {}
    with open(STOCK_RATIO_FILE) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            ticker, fraction = row[0].strip(), float(row[1].strip())
            stocks[ticker] = {}
            share = Share(ticker)
            scurr = share.get_currency()
            if scurr != CURRENCY:
                xchrate = float(Currency(scurr+CURRENCY).get_rate())
            else:
                xchrate = 1.0
            price = float(share.get_price())*xchrate
            stocks[ticker]['price'] = price
            stocks[ticker]['in_currency'] = CURRENCY 
            stocks[ticker]['target_ratio'] = fraction
            stocks[ticker]['name'] = share.get_name()
            stocks[ticker]['target_number'] = np.round(fraction*TOTAL_CASH / price)

    print(json.dumps(stocks,indent=2))

    total_value = 0
    for stock in stocks:
        s = stocks[stock]
        total_value += s['price']*s['target_number']

    print('Total Portfolio Value:')
    print(total_value)


if __name__ == "__main__":
    """ Run the script. """
    main()
