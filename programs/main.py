from constants import ABORT_ALL_POSITONS, FIND_COINTEGRATED, PLACE_TRADES, MANAGE_EXITS
from func_connections import connect_dydx
from func_private import abort_all_open_positions
from func_public import construct_market_prices
from func_cointegration import store_cointegration_results
from func_entry_pairs import open_positions
from func_exit_pairs import manage_trade_exits

if __name__ == "__main__":

    # Connect to client
    try:
        print("Connecting to client...")
        client = connect_dydx()
    except Exception as e:
        print("Error connecting to client: ", e)
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITONS:
        try:
            print("Closing all open Positions...")
            close_orders = abort_all_open_positions(client)
        except Exception as e:
            print("Error aborting all open positions: ", e)
            exit(1)

    # Find Co-integrated Pairs

    if FIND_COINTEGRATED:

        #Construct Market prices
        try:
            print("Fetching Market Prices, Please allow 3 minutes...")
            df_market_prices = construct_market_prices(client)
        except Exception as e:
            print("Error constructing market prices: ", e)
            exit(1)

        #Store cointegrated pairs
        try:
            print("Storing cointegrated pairs, Please allow a bit of your time")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print(" Error saving cointegrated pairs: ", e)
            exit(1)

    while True:

        #Place trades for opening positions
        if MANAGE_EXITS:
            try:
                print("Managing exits...")
                manage_trade_exits(client)
            except Exception as e:
                print("Error Error managing exiting trades: ", e)
                exit(1)

        #Place trades for opening positions
        if PLACE_TRADES:
            try:
                print("Finding trading opportunities...")
                open_positions(client)
            except Exception as e:
                print("Error trading pairs: ", e)
                exit(1)