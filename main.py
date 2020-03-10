import json
from plot import plot
import first_calgary
from helpers import *
from pathlib import Path


def main():
    if Path("aliases.json").exists():
        print("Loading aliases from aliases.json")
        act_aliases = json.loads(open("aliases.json", "r").read())
    else:
        act_aliases = None

    accounts = {}
    
    accounts.update(first_calgary.load())

    if act_aliases is not None:
        accounts = apply_aliases(accounts, act_aliases)
    
    # adds a line for total value of all accounts.
    create_total(accounts)
    
    plot(accounts)


if __name__ == '__main__':
    main()
