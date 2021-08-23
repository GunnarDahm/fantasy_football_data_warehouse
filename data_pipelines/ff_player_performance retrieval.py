import pandas as pd
import requests
import sqlalchemy as sql
import json



def get_ff_perf_data(league_id, year, swid, espn_s2, cred='credentials.json'):
    '''
    Call this function to retrieve player data
    :return: Pandas Dataframe with the following columns ['Week', 'Fantasy Team ID', 'Professional Team','Player',
        'Slot','Pos', 'Status', 'Proj', 'Actual']
    '''

    # establishing connection and cursor
    f = open(cred)

    login = json.load(f)

    engine = sql.create_engine("mysql+pymysql://{}:{}@localhost:3306/nfl".format(str(login['userId']),
                                                                                 str(login['password'])))

    f.close()

    slotcodes = {
        0: 'QB', 2: 'RB', 4: 'WR',
        6: 'TE', 16: 'Def', 17: 'K',
        20: 'Bench', 21: 'IR', 23: 'Flex'
    }

    pro_team_codes = {
        0: 'None',
        1: 'ATL',
        2: 'BUF',
        3: 'CHI',
        4: 'CIN',
        5: 'CLE',
        6: 'DAL',
        7: 'DEN',
        8: 'DET',
        9: 'GNB',
        10: 'OTI',
        11: 'CLT',
        12: 'KAN',
        13: 'RAI',
        14: 'RAM',
        15: 'MIA',
        16: 'MIN',
        17: 'NWE',
        18: 'NOR',
        19: 'NYG',
        20: 'NYJ',
        21: 'PHI',
        22: 'CRD',
        23: 'PIT',
        24: 'SDG',
        25: 'SFO',
        26: 'SEA',
        27: 'TAM',
        28: 'WAS',
        29: 'CAR',
        30: 'JAX',
        33: 'RAV',
        34: 'HTX'
    }

    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + \
          str(year) + '/segments/0/leagues/' + str(league_id) + \
          '?view=mMatchup&view=mMatchupScore'

    print("Retrieving Fantasy Performance Data for {} from {}.".format(year, url))

    for week in range(1, 17):

        r = requests.get(url,
                         params={'scoringPeriodId': week},
                         cookies={"SWID": str(swid), "espn_s2": str(espn_s2)})
        d = r.json()

        for tm in d['teams']:

            team_id = tm['id']
            print(team_id)

            # looking up game_id

            gm_q = engine.execute(
                "SELECT game_id FROM dim_ff_games WHERE week_no={} AND (home_id = {} OR away_id={})".format(week,
                                                                                                            team_id,
                                                                                                            team_id))
            gm_raw = list(gm_q)

            game_id = str(gm_raw[0]).split("'")[1]
            print(game_id)

            for p in tm['roster']['entries']:


                data = []
                slot = p['lineupSlotId']
                pro_team_code = p['playerPoolEntry']['player']['proTeamId']
                name = p['playerPoolEntry']['player']['fullName']
                pos = slotcodes[slot]

                #print( name)
                #print(slot)
                # looking up/creating a player_id

                if name[-4:]== 'D/ST':
                    player_id = pro_team_codes[pro_team_code]+'_DEF'

                else:
                    first_name = name.split(' ')[0].replace('.','')
                    last_name = name.split(' ')[1].replace('.','')

                    plyr_q = engine.execute(
                        'SELECT player_id FROM dim_nfl_players WHERE first_name = \"{}\" AND last_name = \"{}\"'.format(
                            first_name, last_name))

                    plyr_raw = list(plyr_q)

                    player_id = str(plyr_raw[0]).split("'")[1]

                #print(player_id)

                # injured status (need try/exc bc of D/ST)

                inj = 'NA'
                try:
                    inj = p['playerPoolEntry']['player']['injuryStatus']
                except:
                    pass

                # projected/actual points
                proj, act = None, None
                for stat in p['playerPoolEntry']['player']['stats']:
                    if stat['scoringPeriodId'] != week:
                        continue
                    if stat['statSourceId'] == 0:
                        act = stat['appliedTotal']
                    elif stat['statSourceId'] == 1:
                        proj = stat['appliedTotal']

                data.append([
                    game_id, team_id, player_id, pos, inj, proj, act
                ])

                data = pd.DataFrame(data,
                                    columns=['game_id', 'team_id', 'player_id',
                                             'pos', 'player_status', 'projected_pts', 'actual_pts'])

                try:
                    data.to_sql('fact_ff_performance', con=engine, index=False, if_exists='append')
                    print('Inputted: {} {} for game {}.'.format(team_id, player_id, game_id))

                except sql.exc.IntegrityError:
                    print('Performance for player {} and game {} already present.'.format(player_id, game_id))



get_data(league_id=819126,
         year=2020,
         espn_s2="AEBz5srHGNwu0R59Kph1V6HlwJ5fEvDV2J3tcsrtJMSFPl37c%2FgTvZgEkOO2yCNUIHYsmcl4Ik6opp5BE"
                 "4c5GWoFZNUd%2FbVm%2FDyf7XOBpZyZ3EDejSXTDv1aZMhD13Um3ImdsQ%2BfRxDiZX%2BKw3cx%2F6sLV1X"
                 "JHOS5mbeKvozbGujHQuDS78qVzUofSCqbiMs9LzsFOLOjRBLfXipjUmdCa7ozwW8ceNymLBXoQnZUdqdkjyn"
                 "huMs9Ovg7QoWLX8kml1GxHYxN9kUm6gRZipwFlVygVNpGcuBt1bDJS6Of2V0FMA%3D%3D",
         swid="{0581F0A8-617D-47D8-81F0-A8617D37D85B}")

