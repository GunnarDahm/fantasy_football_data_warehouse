import datetime as dt
import mysql.connector
from sportsipy.nfl.teams import Team
from sportsipy.nfl.teams import Teams
from sportsipy.nfl.boxscore import Boxscore
from sportsipy.nfl.player import AbstractPlayer as Player


def get_player_performance(player_name, player_id, player_data):
    player=Player(player_name=player_name, player_id=player_id, player_data= player_data)