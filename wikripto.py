import os
import glob
import sys
import datetime
import pandas as pd
from time import sleep
from subprocess import call

class WikriptoTerminal():
    def __init__(self):
        """Open Dataset from path and concatenate files to work with"""
        self.df = pd.concat(map(pd.read_csv, glob.glob('data/archive/*.csv')))

    def clear(self):
        """define clear screen function, check and make call for specific operating system"""
        _ = call('clear' if os.name =='posix' else 'cls')

    def valid_date(self, date):
        """Method to validate if given string is a valid date"""
        try:
          datetime.datetime.strptime(date, "%Y-%m-%d")

        except ValueError:
            return False

        # True by default (correct format)
        return True

    def main(self):
        self.clear()
        choice = input("""
            ************Welcome to Wikripto Terminal**************\n
            A: Get Available coins in dataset.\n
            B: Close price of X coin at date yyyy-mm-dd\n
            C: Best possible buy and sell times to maximise profit betwen two dates\n
            Q: Logout\n
            Please enter your choice: """
        )

        if choice in('a', 'A'):
            self.clear()
            print("There you got the coins availables in our dataset:\n")
            for row in set(self.df.Name): print(row)

            # Calling menu again after 5 secs.
            sleep(5)
            self.main()

        if choice in('b', 'B'):
            self.clear()
            query_name = input("Insert Coin name: ")
            query_date = input("Insert Date (yyy-mm-dd): ")

            # Validating date fotmat.
            if self.valid_date(query_date) == False:
                print("Incorrect date string format. It should be YYYY-MM-DD")
                sleep(5)
                self.main()


            """filtering dataframe with loc utility: ->
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html
            """
            query_results = self.df.loc[
                (
                    (self.df['Name'] == query_name) & (self.df['Date'].str.contains(query_date)),
                    ['Close',]
                )
            ]

            if query_results.empty:
                print(
                    f"""there are no results given parameters:\n
                    name -> {query_name} date -> {query_date}"""
                )

            else:
                print(
                    f"""Here you got the results:\n
                    the CLOSE price for {query_name} at {query_date} is: {query_results.values.item()}"""
                )

            # Calling menu again after 5 secs.
            sleep(5)
            self.main()

        if choice in('c', 'C'):
            self.clear()
            start_date = input("Insert Start Date (yyy-mm-dd): ")
            end_date = input("Insert End Date (yyy-mm-dd): ")

            # Validating date format.
            if self.valid_date(start_date) == False or self.valid_date(end_date) == False:
                print("Incorrect date string format. It should be YYYY-MM-DD")
                sleep(5)
                self.main()

            # Converting dates to datetime format in dateframe.
            self.df['Date'] = pd.to_datetime(self.df['Date'])

            # Creating filter by the given dates.
            date_range_filter = (self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)
            pre_filter_data = self.df.loc[date_range_filter]

            if pre_filter_data.empty:
                print(
                    f"""there are not results given parameters:\n
                    start date -> {start_date} end date -> {end_date}"""
                )

            else:
                # Obtain the max and min profit.
                max_sell_profit = pre_filter_data.iloc[pre_filter_data['High'].argmax(), [1, 2, 3]]
                max_buy_profit = pre_filter_data.iloc[pre_filter_data['Low'].argmin(), [1, 2, 3]]

                # Printing results.
                print(
                    f"""Here you got the results:\n
                    the max profit by SELL is {max_sell_profit.Name} at {max_sell_profit.Date} \n
                    the max profit by BUY is {max_buy_profit.Name} at {max_buy_profit.Date}"""
                )

            # Calling menu again after 5 secs.
            sleep(5)
            self.main()

        if choice in ('q', 'Q'):
            sys.exit()

        # here by default just in case you mess the options.
        self.clear()
        print("You must only select either given options, please try again.")

        # Calling menu again after 2 secs.
        sleep(2)
        self.main()


if __name__ == '__main__':
    # the program is initiated...
    WikriptoTerminal().main()
