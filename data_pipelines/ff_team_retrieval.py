import pandas as pd
import requests
import sqlalchemy as sql
import json


def get_data(league_id, year, cred ='credentials.json'):
    '''
    Used to retrieve the JSON data object
    :return:
    '''

    # creating the connection
    f = open(cred)

    login=json.load(f)

    engine = sql.create_engine("mysql+pymysql://{}:{}@localhost:3306/nfl".format(str(login['userId']),
                                                                                 str(login['password'])))

    f.close()

    # clearing table
    engine.execute('DELETE FROM dim_ff_teams')

    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + \
          "?seasonId=" + str(year)

    print('Retrieving league data from {}'.format(url))

    try:
        r = requests.get(url)
    except:
        print("Error Retrieving URL: Please ensure league ID is correct.")
        return None

    # return r.json()

    tms = r.json()[0]

    df = pd.DataFrame(tms['teams'])
    df['member_id'] = df['owners'].str[0]

    mem_df = pd.DataFrame(tms['members'])

    df = df.merge(mem_df, left_on='member_id', right_on='id', how='left').drop(columns=['id_y', 'isLeagueManager',
                                                                                        'owners', 'member_id'])

    column_map = {
        'id_x': 'team_id',
        'displayName': 'owner_name'
    }
    df = df.rename(columns=column_map)

    print('League data sample:')
    print(df.head())

    df.to_sql('dim_ff_teams', con=engine, index=False, if_exists='append')

    print('\nDIM_ff_teams Table updated successfully.')


get_data(league_id=819126, year=2020)
