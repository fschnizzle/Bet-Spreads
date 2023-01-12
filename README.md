# Bet Spreads

Finds arbitrage markets for a given player using indicative odds as the metric.

This code is written in Python and uses the pandas, nba_api libraries.
The code utilizes the NBA API to retrieve player information and game logs for a given player.
The code is divided into 3 main parts:

1. get_player_id(): function is used to find the player id of a given player name by making a request to the NBA API.
2. get_game_logs(): function is used to fetch the game logs for a given player and season by making a request to the NBA API.
3. get_percent_greater_than_or_equal_to() : function accepts a dataframe and column name and returns the percentage of rows in the dataframe where the value in the specified column is greater than or equal to a given value.

Then it runs the following script:

- A player name is prompted as an input.
- It then specifies the columns of interest in columns and the threshold values in x_vals.
- It then fetches player_id and game logs of the player using the above functions.
- It then calculates the percentage of rows where the value in the specified column is greater than or equal to x, for all columns and threshold values.
- Then it displays the indicative_odds for all given columns and threshold value if the result is greater than 1.00 overall (filters out most not-offered markets) and for first 10 games where the odds are less than 1.35. Anything outside these thresholds are likely not useful for arbitrage fixed-odds multis.
