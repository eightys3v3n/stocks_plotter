from plot import plot
from helpers import *
from pathlib import Path

import yahoo_finance


def main():
    accounts = {}
    
    accounts.update(yahoo_finance.load("csv_files/xrp_usd.csv", "XRP/USD", scale=50))
    accounts.update(yahoo_finance.load("csv_files/btc_usd.csv", "BTC/USD", scale=0.005))
    accounts.update(yahoo_finance.load("csv_files/eth_usd.csv", "ETH/USD", scale=0.1))
    accounts.update(yahoo_finance.load("csv_files/cad_usd.csv", "CAD/USD", scale=100))
    accounts.update(yahoo_finance.load("csv_files/gspc.csv", "S&P 500", scale=.05))
    #accounts.update(yahoo_finance.load("csv_files/cad_usd.csv", "CAD/USD", scale=100))

    # adds a line for total value of all accounts.
    #create_total(accounts)
    
    plot(accounts)


if __name__ == '__main__':
    main()
