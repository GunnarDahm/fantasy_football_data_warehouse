import datetime as dt
import mysql.connector
from sportsipy.nfl.teams import Team
from sportsipy.nfl.teams import Teams
from sportsipy.nfl.boxscore import Boxscore

# Pulling from https://www.sports-reference.com/

def retrieve_schedule(year, team, first_game):
    """Used to retrieve the schedule information for played games of a specified team and insert the info into the NFL
    DB in the local MySQL server.
    year: int of year the season started in, takes into account spillover into Jan/Feb
    team: Used to specify which team will be retrieved
    first_game: YYYY/MM/DD date in which the first game of the season is played, used for week calculation
    :return : None, uploads teams (home and away), final score, week, season, and date to games table
    """

    # establishing connection and cursor
    # TODO create a txt file to store the connection information and pull from there
    cnx = mysql.connector.connect(user='nfl_retrieval_app',
                                  password='indesCYTJd2cLgt7LoAQ',
                                  host='localhost',
                                  database='nfl',
                                  auth_plugin='mysql_native_password')

    cursor = cnx.cursor()

    # Establishing some necessary objects for iteration
    schedule = Team(team_name=team, year=year).schedule
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

    # Iterating through each game and adding home games to the schedule
    for game in schedule:

        # creating the necessary url and retrieving box score
        game_split = str(game).split(' ')

        # handling for Jan/Feb spillover into the next year
        if str(game).split(' ')[0] == 'January' or str(game).split(' ')[0] == 'February':
            boxscore = Boxscore(uri=(str(year + 1) + months_dict[game_split[0]] + str(game_split[1].zfill(2)) + '0'
                                     + team.lower()))
        else:
            boxscore = Boxscore(uri=(str(year) + months_dict[game_split[0]] + str(game_split[1].zfill(2)) + '0'
                                     + team.lower()))

        # boxscore url's are only generated for home games, so handling for such exceptions
        if boxscore.home_abbreviation == 'None':
            print('Game data does not exist. Game is either away game for {} or is yet to be played.'.format(team))

        else:
            # Unique index already created to avoid duplicates in table when updating, error handling for this
            try:
                # SQL command
                add_game = (
                    "INSERT INTO games (home ,away ,home_score ,away_score, season, week_no, game_date)"
                    "VALUES (%(home)s,%(away)s, %(home_score)s, %(away_score)s, %(season)s,%(week_no)s,%(game_date)s)")

                game_data = {
                    'home': str(boxscore.home_abbreviation).upper(),
                    'away': str(boxscore.away_abbreviation).upper(),
                    'home_score': boxscore.home_points,
                    'away_score': boxscore.away_points,
                    'season': year,
                    'week_no': ((boxscore.datetime - dt.datetime.strptime(first_game, '%Y/%m/%d')).days // 7) + 1,
                    'game_date': dt.date.strftime(boxscore.datetime, '%Y-%m-%d')
                }

                cursor.execute(add_game, game_data)

                print('Game inputted: {} vs. {} on {} (Week {})'.format(str(boxscore.home_abbreviation),
                                                                        str(boxscore.away_abbreviation),
                                                                        dt.date.strftime(boxscore.datetime, '%Y-%m-%d'),
                                                                        ((boxscore.datetime - dt.datetime.strptime(
                                                                            first_game, '%Y/%m/%d')).days // 7) + 1))

            except mysql.connector.errors.IntegrityError:
                print('Game: {} vs. {} on {} already present in table.'.format(str(boxscore.home_abbreviation),
                                                                               str(boxscore.away_abbreviation),
                                                                               dt.date.strftime(boxscore.datetime,
                                                                                                '%Y-%m-%d')))

    # committing and closing the cursor and connection
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Schedule inputted: {} for {}'.format(team, year))


def update_games(year, first_game):
    """
    Function to iterate through all teams and update the games table for specified year
    :param year: int of year the season started in, takes into account spillover into Jan/Feb
    first_game: YYYY/MM/DD date in which the first game of the season is played, used for week calculation
    :return: None, Games table updated
    """

    for team in Teams():
        retrieve_schedule(year=year, team=str(team.abbreviation).upper(), first_game=first_game)

    print('Table "Games" updated for {}'.format(year))


update_games(year=2020, first_game='2020/09/10')
