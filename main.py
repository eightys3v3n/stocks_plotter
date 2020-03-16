from plot import plot
from helpers import *
from pathlib import Path

import yahoo_finance
import big_query


def main():
    accounts = {}
    
    accounts.update(yahoo_finance.load("csv_files/yahoo_finance/xrp_usd.csv", "XRP/USD", 0, 3))
    accounts.update(yahoo_finance.load("csv_files/yahoo_finance/btc_usd.csv", "BTC/USD", 0, 20000))
    accounts.update(yahoo_finance.load("csv_files/yahoo_finance/eth_usd.csv", "ETH/USD", 0, 1400))
    accounts.update(yahoo_finance.load("csv_files/yahoo_finance/cad_usd.csv", "CAD/USD", .5, 1))
    accounts.update(yahoo_finance.load("csv_files/yahoo_finance/gspc.csv"   , "S&P 500", 1500, 3500))
    
    accounts.update(big_query.load("csv_files/big_query/xrp_activity.csv", "/r/XRP Activity", 0, 400))

    # adds a line for total value of all accounts.
    #create_total(accounts)
    
    plot(accounts)


if __name__ == '__main__':
    main()
