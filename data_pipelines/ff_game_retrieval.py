# basically need to pull games using this https://stmorse.github.io/journal/espn-fantasy-v3.html
# And from here; https://github.com/stmorse/footballdrop/blob/master/roster_management_clean.ipynb
import pandas as pd
import requests
import sqlalchemy as sql
import json

def get_ff_game_data(year, league_id, cred='credentials.json'):
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + \
          "?seasonId=" + str(year)

    # creating the connection
    f = open(cred)

    login=json.load(f)

    engine = sql.create_engine("mysql+pymysql://{}:{}@localhost:3306/nfl".format(str(login['userId']),
                                                                                 str(login['password'])))

    f.close()

    r = requests.get(url, params={"view": 'mMatchup'})

    d = r.json()[0]

    df = [[
        game['matchupPeriodId'],
        game['home']['teamId'], game['home']['totalPoints'],
        game['away']['teamId'], game['away']['totalPoints']
    ] for game in d['schedule']]

    df = pd.DataFrame(df, columns=['week_no', 'home_id', 'home_score', 'away_id', 'away_score'])
    df['type'] = ['Regular' if w <= 14 else 'Playoff' for w in df['week_no']]
    df['season'] = year
    df['game_id'] = df['season'].map(str) + '_' + df['week_no'].map(str) + '_' + df['home_id'].map(str)

    df.to_sql('dim_ff_games', con=engine, index=False, if_exists='append')

    print('Table DIM_FF_GAMES updated successfully.')

#get_data(year=2020, league_id=819126)
