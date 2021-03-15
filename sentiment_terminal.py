# ===============================
# Terminal Interface for Sentilab
# ===============================

import argparse
import pandas as pd
import six 
import config_terminal as cfg
from pyfiglet import figlet_format

from alpa_vantage.timeseries import TimeSeries
from prompt_toolkit.completion import NestedCompleter

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

def main():
    """
    Sentiment Terminal
    """

    ticker = ""
    start = ""
    df_ticker = pd.DataFrame()
    interval = "1440min"

    # Arguments
    terminal_menu = argparse.ArgumentParser(prog="sentilab", add_help=False)

    terminal_menu.add_argument(
        "opt",
        choices=[
          "help",
          "quit",
          "clear",
          "load",
          "view",
          "load",
          "export",
          "sentiment",  
        ],
    )
    
    # Complete the arguments that are not used
    completer = NestedCompleter.from_nested_dict({c: None for c in choices})

    print("WELCOME TO SENTILAB TERMINAL")
    help_print = True

    # Continuous loop
    while True:
        main_command = False
        if help_print:
            print_help(ticker, start, interval, is_market_open())
            help_print = False
        
        if session and 



# --------------------------------
def load(args, ticker, start, interval, stock):
    """
    Function for loading infromation on a given ticker.

    Args:
        args (List): [description]
        ticker (String): [description]
        start (String): [description]
        interval (String): [description]
        stock (DataFrame): [description]
    """

    parser = argparse.ArgumentParser()

if __name__ == "__main__":
    main()