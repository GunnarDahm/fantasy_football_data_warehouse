import sportsipy.nfl.teams as nfl
import pandas as pd
import sqlalchemy as sql
import json

def update_teams(season, cred='credentials.json'):
    '''
    Updates the teams table in the nfl database for changes in team names or cities
    :return: None, deletes and updates team names and cities in teams table
    '''

    # establishing connection and cursor
    f = open(cred)

    login=json.load(f)

    engine = sql.create_engine("mysql+pymysql://{}:{}@localhost:3306/nfl".format(str(login['userId']),
                                                                                 str(login['password'])))

    f.close()

    # clearing table
    engine.execute('DELETE FROM dim_nfl_teams')

    # loadingin a conference mapping seeing as it isn't in the api
    conf = pd.read_csv(r'.\conf_mapping.csv')

    teams = nfl.Teams(year=season)

    for team in teams:
        team_split = str(team.name).split(' ')
        team_name = team_split[-1]
        team_split.pop(-1)
        team_city = ' '.join(team_split)

        team_data = {
            'team_id': team.abbreviation,
            'team_city': team_city,
            'team_name': team_name
        }

        team_data = pd.DataFrame(team_data, index=[0])

        df = team_data.merge(conf, left_on=['team_id'], right_on=['Team_Id'], how='inner').drop(columns=['Team_Id'])

        df.to_sql('dim_nfl_teams', con=engine, index=False, if_exists='append')

        print('Inputted {}, {}, {}'.format(team.abbreviation, team_city, team_name))


update_teams(season=2020)
