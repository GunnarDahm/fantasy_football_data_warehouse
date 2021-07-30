# intended to retrieve all player information

import sportsipy.nfl.teams as nfl
import pandas as pd
import sqlalchemy as sql
import requests
from bs4 import BeautifulSoup


def get_player_data(season):
    # establishing connection and cursor
    engine = sql.create_engine("mysql+pymysql://nfl_retrieval_app:indesCYTJd2cLgt7LoAQ@localhost:3306/nfl")

    # inputting base attributes to the database

    for team in nfl.Teams(year=season):
        for player in team.roster.players:

            # TODO Do a quick check to see if player id already exists in table, speed dups up a bit

            # building the input dictionary
            try:

                player_data = {
                    'player_id': player.player_id,
                    'first_name': player.name.split(' ')[0],
                    'last_name': player.name.split(' ')[1],
                    'position': None,
                    'birth_day': player.birth_date,
                    'height': player.height,
                    'weight': player.weight,
                    'college': None
                }

                # pulling position straight from the website seeing as it doesn't want to play nice
                try:
                    url = 'https://www.pro-football-reference.com/players/{}/{}.htm'.format(player_data['last_name'][0],
                                                                                            player_data['player_id'])

                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, "html.parser")

                    result = soup.find_all('p')

                    # Literally second paragraph on page
                    raw = str(result[1])
                    position = raw.split(':')[1].replace('</p>', '')
                    if position.strip()[:3] == 'OLB' or position.strip()[:3] == 'ILB':
                        position = position.strip()[:3]

                    else:
                        position = position.strip()[:2]

                    player_data['position']=position

                except TypeError:
                    pass

                except IndexError:
                    pass

                # pulling university too
                try:
                    url = 'https://www.pro-football-reference.com/players/{}/{}.htm'.format(player_data['last_name'][0],
                                                                                            player_data['player_id'])

                    page = requests.get(url)

                    soup = BeautifulSoup(page.content, "html.parser")

                    result = soup.find_all('a')

                    for x in result:
                        if str(x).find('/schools') != -1:
                            college = str(x).split('>')[1].replace('</a', '')
                            college=college.strip().replace('amp;','')

                            if len(college) <= 40:

                                player_data['college'] = college.strip()
                            break

                except TypeError:
                    pass

                except IndexError:
                    pass

                df = pd.DataFrame(player_data, index=[0])

                df.to_sql('players', con=engine, index=False, if_exists='append')

                print('Inputted Player: {} {}'.format(player_data['first_name'], player_data['last_name']))

            except sql.exc.IntegrityError:
                print('Player {} already present in Players table.'.format(player.name))

            except AttributeError:
                print('Exception: Empty String')


get_player_data(season=2020)
