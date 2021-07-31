import pandas as pd
import requests

class Player_Data:
    '''
    The purpose of this class is to establish a dataframe containing the needed player data on weekly basis.
    Call the get_data func to retrieve the data.
    '''
    def __init__(self, league_id, year, swid, espn_s2):
        '''
        The following parameters are all necessary to access the ESPN Fantasy Football API

        Note: that swid and espn_s2 are cookie values that must be retrieved through your browser
        For Chrome Users:
        Settings >> Privacy and Security >> Site Settings >> Cookies >> See All Cookies and Site Data>>espn.com

        :param league_id: INT, can be obtained through the URL of your fantasy home
        :param year: INT
        :param swid: STR, contained in brackets. See Note above for retrieving this value.
        :param espn_s2: STR, ~300 chars. See Note above for retrieving this value.
        '''
        self.league_id=league_id
        self.year= year
        self.swid = swid,
        self.espn_s2 = espn_s2


    def __repr__(self):
        return "<Fantasy Football Player Dataframe for League ID:{} for year {}>".format(self.league_id, self.year)

    def get_data(self):
        '''
        Call this function to retrieve player data
        :return: Pandas Dataframe with the following columns ['Week', 'Fantasy Team ID', 'Professional Team','Player',
            'Slot','Pos', 'Status', 'Proj', 'Actual']
        '''
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
            9: 'GB',
            10: 'TEN',
            11: 'IND',
            12: 'KC',
            13: 'OAK',
            14: 'LAR',
            15: 'MIA',
            16: 'MIN',
            17: 'NE',
            18: 'NO',
            19: 'NYG',
            20: 'NYJ',
            21: 'PHI',
            22: 'ARI',
            23: 'PIT',
            24: 'LAC',
            25: 'SF',
            26: 'SEA',
            27: 'TB',
            28: 'WSH',
            29: 'CAR',
            30: 'JAX',
            33: 'BAL',
            34: 'HOU'
        }

        url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + \
              str(self.year) + '/segments/0/leagues/' + str(self.league_id) + \
              '?view=mMatchup&view=mMatchupScore'

        print("Retrieving Data for {}.".format(self.year))

        data = []
        print('Week ', end='')
        for week in range(1, 17):
            print(week, end=' ')

            r = requests.get(url,
                             params={'scoringPeriodId': week},
                             cookies={"SWID": str(self.swid), "espn_s2": str(self.espn_s2)})
            d = r.json()

            for tm in d['teams']:
                tmid = tm['id']
                for p in tm['roster']['entries']:
                    name = p['playerPoolEntry']['player']['fullName']
                    slot = p['lineupSlotId']
                    pos = slotcodes[slot]
                    pro_team_code=p['playerPoolEntry']['player']['proTeamId']
                    pro_team_name=pro_team_codes[pro_team_code]

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
                        week, tmid, pro_team_name, name, slot, pos, inj, proj, act
                    ])
        print('\nData Retrieved for {}.'.format(self.year))

        data = pd.DataFrame(data,
                            columns=['Week', 'Fantasy Team ID', 'Professional Team','Player', 'Slot',
                                     'Pos', 'Status', 'Proj', 'Actual'])

        return data


season_2018=Player_Data(league_id=819126,
                         year=2020,
                         espn_s2="AEBz5srHGNwu0R59Kph1V6HlwJ5fEvDV2J3tcsrtJMSFPl37c%2FgTvZgEkOO2yCNUIHYsmcl4Ik6opp5BE4c5GWoFZNUd%2FbVm%2FDyf7XOBpZyZ3EDejSXTDv1aZMhD13Um3ImdsQ%2BfRxDiZX%2BKw3cx%2F6sLV1XJHOS5mbeKvozbGujHQuDS78qVzUofSCqbiMs9LzsFOLOjRBLfXipjUmdCa7ozwW8ceNymLBXoQnZUdqdkjynhuMs9Ovg7QoWLX8kml1GxHYxN9kUm6gRZipwFlVygVNpGcuBt1bDJS6Of2V0FMA%3D%3D",
                         swid = "{0581F0A8-617D-47D8-81F0-A8617D37D85B}").get_data()

print(season_2018)