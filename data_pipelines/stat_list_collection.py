# Intended to compile the listing of all unique possible stats collected from the API
# This then goes in to the table creation of the MySQL server

# imports
import nflgame
import pandas as pd

# collecting values from the 2019 season
season = nflgame.games(year=2019)
stat_string = ''

for x in range(17):
    game = season[x]
    for player in game.players:
        stat_string = stat_string + player.formatted_stats()

# splitting formatted strings
full_stat_list = stat_string.split(',')
formatted_stat_list = []

for item in full_stat_list:
    stats = item.split(':')
    formatted_stat_list.append(stats[0])

# dumping the stats in to dataframe and saving as a CSV for reference
stats_frame = pd.DataFrame(formatted_stat_list)
formatted_stat_frame = stats_frame.drop_duplicates()

# reformatting
formatted_stat_frame = formatted_stat_frame.reset_index(drop=True)
formatted_stat_frame['description'] = None
formatted_stat_frame = formatted_stat_frame.rename(columns={formatted_stat_frame.columns[0]: 'stat',
                                                            formatted_stat_frame.columns[1]: 'description'})
# printing and saving
print(formatted_stat_frame)
formatted_stat_frame.to_csv('stats_dict.csv')