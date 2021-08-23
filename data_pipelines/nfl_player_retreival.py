# intended to retrieve all player information

import sportsipy.nfl.teams as nfl
import pandas as pd
import sqlalchemy as sql
import requests
from bs4 import BeautifulSoup
import json


def get_player_data(season, cred='credentials.json'):
    # establishing connection and cursor
    f = open(cred)

    login=json.load(f)

    engine = sql.create_engine("mysql+pymysql://{}:{}@localhost:3306/nfl".format(str(login['userId']),
                                                                                 str(login['password'])))

    f.close()

    # inputting base attributes to the database

    for team in nfl.Teams(year=season):
        for player in team.roster.players:

            # Check to see if this dude already exists in the players database
            try:
                check = engine.execute("SELECT player_id FROM dim_nfl_players "
                                       "WHERE "
                                       "player_id = '{}'".format(player.player_id))

            except sql.exc.ProgrammingError:
                check=[]

            if len(list(check)) > 0:
                print('Player {} already present in Players table.'.format(player.name))

            else:
                # building the input dictionary
                try:

                    player_data = {
                        'player_id': player.player_id,
                        'first_name': player.name.split(' ')[0].replace('.',''),
                        'last_name': player.name.split(' ')[1].replace('.',''),
                        'position': None,
                        'birth_day': player.birth_date,
                        'height': player.height,
                        'weight': player.weight,
                        'college': None
                    }

                    # pulling position straight from the website seeing as it doesn't want to play nice

                    url = 'https://www.pro-football-reference.com/players/{}/{}.htm'.format(player_data['last_name'][0],
                                                                                            player_data['player_id'])
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, "html.parser")

                    try:
                        result = soup.find_all('p')

                        # Literally second paragraph on page
                        raw = str(result[1])
                        position = raw.split(':')[1].replace('</p>', '')
                        if position.strip()[:3] == 'OLB' or position.strip()[:3] == 'ILB':
                            position = position.strip()[:3]

                        else:
                            position = position.strip()[:2]

                        player_data['position'] = position

                    except TypeError:
                        pass

                    except IndexError:
                        pass

                    # pulling university too
                    try:
                        result = soup.find_all('a')

                        for x in result:
                            if str(x).find('/schools') != -1:
                                college = str(x).split('>')[1].replace('</a', '')
                                college = college.strip().replace('amp;', '')

                                if len(college) <= 40:
                                    player_data['college'] = college.strip()
                                break

                    except TypeError:
                        pass

                    except IndexError:
                        pass

                    df = pd.DataFrame(player_data, index=[0])

                    df.to_sql('dim_nfl_players', con=engine, index=False, if_exists='append')

                    print('Inputted Player: {} {}'.format(player_data['first_name'], player_data['last_name']))

                except sql.exc.IntegrityError:
                    print('Player {} already present in Players table.'.format(player.name))

                except AttributeError:
                    print('Exception: Empty String')


get_player_data(season=2017)
