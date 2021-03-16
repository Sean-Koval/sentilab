import argparse
from sys import stdout
import matplotlib.pyplot as plt
import pandas as pd
# from alpha_vantage.timeseries import TimeSeries
import mplfinance as mpf
import yfinance as yf

from sentilab.helper_functions import (
    valid_date,
    parse_known_args_and_warn,
    lett_to_num,
    check_sources,
)

from sentilab import config_terminal as cfg
from sentilab import feature_flags as ff
# from sentilab.fundamental_analysis import trendline_api as trend


def print_help(s_ticker, s_start, s_interval, b_is_market_open):
    """Print help"""
    print("What do you want to do?")
    print("   help        help to see this menu again")
    print("   quit        to abandon the program")
    print("")
    
    if s_ticker:
        print(
            "   export      export the currently loaded dataframe to a file or stdout"
        )

    s_intraday = (f"Intraday {s_interval}", "Daily")[s_interval == "1440min"]
    
    if s_ticker and s_start:
        print(f"\n{s_intraday} Stock: {s_ticker} (from {s_start.strftime('%Y-%m-%d')})")
    elif s_ticker:
        print(f"\n{s_intraday} Stock: {s_ticker}")
    else:
        print("\nStock: ?")

    print(f"Market {('CLOSED', 'OPEN')[b_is_market_open]}.")

    print("\nMenus:")

    print(
        "   sen         sentiment of the market, \t from: reddit, stocktwits, twitter"
    )
    if s_ticker:
        print(
            "   res         research web page,       \t e.g.: macroaxis, yahoo finance, fool"
        )
        print(
            "   dd          in-depth due-diligence,  \t e.g.: news, analyst, shorts, insider, sec"
        )
        print(
            "   pred        prediction techniques,   \t e.g.: regression, arima, rnn, lstm, prophet"
        )
    print("")



def export(l_args, df_stock):
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="export",
        description="Exports the historical data from this ticker to a file or stdout.",
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        dest="s_filename",
        default=stdout,
        help="Name of file to save the historical data exported (stdout if unspecified)",
    )
    parser.add_argument(
        "-F",
        "--format",
        dest="s_format",
        type=str,
        default="csv",
        help="Export historical data into following formats: csv, json, excel, clipboard",
    )
    try:
        ns_parser = parse_known_args_and_warn(parser, l_args)
        if not ns_parser:
            return

    except SystemExit:
        print("")
        return

    if df_stock.empty:
        print("No data loaded yet to export.")
        return

    if ns_parser.s_format == "csv":
        df_stock.to_csv(ns_parser.s_filename)

    elif ns_parser.s_format == "json":
        df_stock.to_json(ns_parser.s_filename)

    elif ns_parser.s_format == "excel":
        df_stock.to_excel(ns_parser.s_filename)

    elif ns_parser.s_format == "clipboard":
        df_stock.to_clipboard()

    print("")