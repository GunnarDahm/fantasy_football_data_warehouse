import mysql.connector
import pandas as pd
from sportsipy.nfl.teams import Team
import sportsipy.nfl.teams as Teams
from sportsipy.nfl.boxscore import Boxscore
import sqlalchemy as sql
import pymysql


def get_player_performance(season, week):
    # Establishing connection
    engine = sql.create_engine("mysql+pymysql://nfl_retrieval_app:indesCYTJd2cLgt7LoAQ@localhost:3306/nfl")

    # Iterating through teams
    teams = Teams.Teams()

    for team in teams:
        team_id = team.abbreviation.upper()

        schedule = Team(team_name=team_id, year=season).schedule
        months_dict = {'January': '01',
                       'February': '02',
                       'March': '03',
                       'April': '04',
                       'May': '05',
                       'June': '06',
                       'July': '07',
                       'August': '08',
                       'September': '09',
                       'October': '10',
                       'November': '11',
                       'December': '12'
                       }

        # Iterating through the schedule of each one of those teams
        for game in schedule:
            game_split = str(game).split(' ')

            # handling for Jan/Feb spillover into the next year
            if str(game).split(' ')[0] == 'January' or str(game).split(' ')[0] == 'February':
                game_id = str(season + 1) + months_dict[game_split[0]] + str(game_split[1].zfill(2)) + '0' \
                          + team_id.lower()
                boxscore = Boxscore(uri=game_id)

            else:
                game_id = uri = str(season) + months_dict[game_split[0]] + str(game_split[1].zfill(2)) \
                                + '0' + team_id.lower()
                boxscore = Boxscore(uri=game_id)

            # boxscore url's are only generated for home games, so handling for such exceptions
            if boxscore.home_abbreviation == 'None':
                print('Game data does not exist. Game is either away game for {} or is yet to be played.'.format(team))
                pass

            else:
                print("Inputting {} for team {}".format(game_id, team_id))

                # inputting home player performance
                for player in boxscore.home_players:
                    home_df = player.dataframe

                    home_df['game_id'] = game_id
                    home_df['team_id'] = team_id
                    home_df['player_id']=home_df.index[0]

                    try:
                        home_df.to_sql('performance', con=engine, index=False, if_exists='append')
                        print('Inputted: {} {} for game {}.'.format(player.name, team_id, game_id))

                    except sql.exc.IntegrityError:
                        print('Player {} performance for {} already present in performance table.'.format(player.name,
                                                                                                          game_id))

                    except AttributeError:
                        print('Exception: Empty String')

                # inputting away player performance
                for player in boxscore.away_players:
                    away_df = player.dataframe

                    away_df = player.dataframe

                    away_df['game_id'] = game_id
                    away_df['team_id'] = str(boxscore.away_abbreviation).upper()
                    away_df['player_id'] = away_df.index[0]

                    try:
                        away_df.to_sql('performance', con=engine, index=False, if_exists='append')
                        print('Inputted: {} {} for game {}.'.format(player.name, team_id, game_id))

                    except sql.exc.IntegrityError:
                        print('Player {} performance for {} already present in performance table.'.format(player.name,
                                                                                                          game_id))

                    except AttributeError:
                        print('Exception: Empty String')



get_player_performance(season=2020, week=1)
