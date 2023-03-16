import pandas as pd
import requests
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

"""
Function Declarations
"""

def get_player_id(player_name: str) -> int:
    # Use the nba_api to get the player's ID
    player_info = players.find_players_by_full_name(player_name)[0]

    # Return the largest player ID (most recent player if duplicate full_name)
    return player_info

def get_game_logs(player_id: int) -> pd.DataFrame:
    # Use the nba_api to get game logs for the given player in the 2019-20 season
    game_logs = playergamelog.PlayerGameLog(player_id=player_id, season="2022-23")

    # Create a Pandas DataFrame from the game logs
    game_logs_df = game_logs.get_data_frames()[0]

    # Return dataframe with valid market columns (+ date)
    return game_logs_df[["GAME_DATE", "PTS", "AST", "REB", "MIN","FG3M"]]

def get_percent_greater_than_or_equal_to(df: pd.DataFrame, column_name: str, x: int) -> float:
    # Get the number of rows where the value in the specified column is greater than or equal to x
    num_rows = df[df[column_name] >= x].shape[0]

    # Returns % of rows in column greater than or equal to x
    return (num_rows / df.shape[0]) * 100
"""
Name Database 
"""

# Make a GET request to the NBA API to retrieve the list of players
response = requests.get('https://data.nba.net/prod/v1/2022/players.json')

# Check if the request was successful
if response.status_code == 200:
    # Convert the response JSON to a Python dictionary
    data = response.json()

    # Extract the list of players' names
    players = []
    for player in data['league']['standard']:
        full_name = player['firstName'] + ' ' + player['lastName']
        players.append(full_name)

    # Save the list of players' names to a local file
    with open('nba_players.txt', 'w') as f:
        f.write('\n'.join(players))

"""
Main
"""

def main():
    choice = 'n'
    while True:
        if choice == 'n':
            # Input Player
            player_name = input("Enter player name: ")

            # Get Dataframe from player name
            player = get_player_id(player_name)
            player_id = player['id']
            game_logs_df = get_game_logs(player_id)

            # Possible Markets
            columns = ["PTS","AST","REB"]
            x_vals = [[10,15,20,25],[2,4,6,8,10],[4,6,8,10,12]]

            # Filter columns by threshold indicative odds
            for i in range(len(columns)):
                # loop through the columns and their corresponding x_vals
                column_name = columns[i]
                for x in x_vals[i]:
                    # calculate percentage and overall indicative odds
                    percentage = get_percent_greater_than_or_equal_to(game_logs_df, column_name, x) + 0.001
                    indicative_odds = round(100/(percentage+0.01),2)

                    # calculate percentage and indicative odds for last 10 games
                    p_10 = get_percent_greater_than_or_equal_to(game_logs_df.head(10), column_name, x) + 0.001
                    i_10 = round(100/(p_10+0.01),2)

                    # Display Market details
                    if indicative_odds > 1.00 and i_10 < 1.40:
                        print('\n{} {}: {} ({})'.format(x, column_name, i_10, indicative_odds))
        elif choice == 's':
            # Show game logs
            # player_name = input("Enter player name: ")
            # player_id = get_player_id(player_name)['id']
            # game_logs_df = get_game_logs(player_id)
            print("".join(['-' for _ in range(80)]))
            print(f"Game Logs for {player_name}:")
            print(game_logs_df.to_string())
            print("".join(['-' for _ in range(80)]))
        else:
            print("Invalid choice. Please enter 'n' or 's'.")

        print("".join(['-' for _ in range(80)]))
        choice = input("Analyse new player ('n') or Show game logs ('s'): ")

    
"""
Call to main function
"""

main()