import datetime as dt
##import mysql.connector
from sportsipy.nfl.teams import Team
import sportsipy.nfl.teams as Teams
from sportsipy.nfl.boxscore import Boxscore
from sportsipy.nfl.player import AbstractPlayer as Player


def get_player_performance(season, week):
    teams = Teams.Teams()

    for team in teams:
        team_id = team.abbreviation.lower()

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

    # iterate through every team
        #log team id for the team key

    # iterate through every game on their schedule
        #log game_id for the game key

    # once we have both those, iterate through each player
        # log player id for player key
        # grab performance, then push push data with the keys to the database for the record
        # enforce the compound key and handle for key errors when duplicates show up
            # Technically I think we will be grabbing both home and away games, so that might double our efforts
            # But hey it's gonna be weekly refresh so I don't really give a shit

get_player_performance(season=2020, week=1)
