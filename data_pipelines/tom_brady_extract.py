from sportsipy.nfl.roster import Player
from sportsipy.nfl.boxscore import Boxscore
import pandas as pd

sb_app={'202102070tam':2020,
        '201902030ram':2018,
        '201802040nwe':2017,
        '201702050atl':2016,
        '201502010sea':2014,
        '201202050nwe':2011,
        '200802030nwe':2007,
        '200502060nwe':2004,
        '200402010car':2003,
        '200202030nwe':2001
        }

data=pd.DataFrame(
    columns=[
        'name',
        'team',
        'completed_passes',
        'attempted_passes',
        'passing_yards',
        'passing_touchdowns',
        'interceptions_thrown',
        'times_sacked',
        'yards_lost_from_sacks',
        'longest_pass',
        'quarterback_rating',
        'rush_attempts',
        'rush_yards',
        'rush_touchdowns',
        'longest_rush',
        'times_pass_target',
        'receptions',
        'receiving_yards',
        'receiving_touchdowns',
        'longest_reception',
        'fumbles',
        'fumbles_lost',
        'interceptions',
        'yards_returned_from_interception',
        'interceptions_returned_for_touchdown',
        'longest_interception_return',
        'passes_defended',
        'sacks',
        'combined_tackles',
        'solo_tackles',
        'assists_on_tackles',
        'tackles_for_loss',
        'quarterback_hits',
        'fumbles_recovered',
        'yards_recovered_from_fumble',
        'fumbles_recovered_for_touchdown',
        'fumbles_forced',
        'kickoff_returns',
        'kickoff_return_yards',
        'average_kickoff_return_yards',
        'kickoff_return_touchdown',
        'longest_kickoff_return',
        'punt_returns',
        'punt_return_yards',
        'yards_per_punt_return',
        'punt_return_touchdown',
        'longest_punt_return',
        'extra_points_made',
        'extra_points_attempted',
        'field_goals_made',
        'field_goals_attempted',
        'punts',
        'total_punt_yards',
        'yards_per_punt',
        'longest_punt'])

for x in sb_app.keys():
    game_data = Boxscore(x)

    home_df = game_data.home_players[0].dataframe
    for player in game_data.home_players[1:]:
        home_df = pd.concat([home_df, player.dataframe], axis = 0)
    home_df['name'] = [x.name for x in game_data.home_players]
    home_df['team']=game_data.home_abbreviation
    home_df['season']=sb_app[x]

    away_df = game_data.away_players[0].dataframe
    for player in game_data.away_players[1:]:
        away_df = pd.concat([away_df, player.dataframe], axis = 0)
    away_df['name'] = [x.name for x in game_data.away_players]
    away_df['team']=game_data.away_abbreviation
    away_df['season']=sb_app[x]

    data=data.append(home_df)
    data=data.append(away_df)
    print(len(data))

print(data.head())
print(data.describe())

data.to_csv('tom_brady_data.csv')