# ===============================
# Terminal Interface for Sentilab
# ===============================

import argparse

import pandas as pd
import six 
from datetime import datetime, timedelta
from sentilab import config_terminal as cfg
from pyfiglet import figlet_format

from prompt_toolkit.completion import NestedCompleter

from sentilab import feature_flags as ff
from sentilab.menu import session
from sentilab.sentiment import sentiment_menu as sm
from sentilab.helper_functions import is_market_open, get_flair
from sentilab.main_helper import print_help
# from sentilab.fundamental_analysis import fa_menu as fam

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
    
    choices = [
          "help",
          "quit",
          "export",
          "sentiment",
          ]

    terminal_menu.add_argument("opt", choices=choices)
    
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
        
        if session and ff.USE_PROMPT_TOOLKIT:
            as_input = session.prompt(f"{get_flair()}?> ", completer=completer)
        else:
            as_input = input(f"{get_flair()}> ")
        
        # Check if command is empty
        if not as_input:
            print("")
            continue
        
        # Parse main command list
        try:
            (ns_known_args, l_args) = terminal_menu.parse_known_args(as_input.split())
        
        except SystemExit:
            print("The command doesn't exist\n")
            continue

        b_quit = False
        if ns_known_args.opt == "help":
            help_print = True 
        
        elif (ns_known_args.opt == "quit") or (ns_known_args.opt == "q"):
            break
            
        
        elif ns_known_args.opt == "sentiment":
            b_quit = sm.sentiment_menu(ticker, start)
        
        
        else:
            print("Should not get to this command")
            continue
        
        if b_quit:
            break
        else:
            if not main_command:
                help_print = True 
        
        
    print("Exiting sentilab Terminal.\n")
    

if __name__ == "__main__":
    main()