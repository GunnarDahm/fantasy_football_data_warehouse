import pandas
import requests

class league_data_prv:
    ''' Used to establish a retrieve a previous season's data as a json file.
    League_id is obtained from url of your ESPN fantasy home, expressed as int
    Year is simply an int
    '''
    def __init__(self, league_id, year):
        self.league_id=league_id
        self.year= year

    def __repr__(self):
        return "<Fantasy Football League Data Object for League ID:{} for {}>".format(self.league_id, self.year)

    def get_data(self):
        '''
        Used to retrieve the JSON data object
        :return:
        '''
        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(self.league_id) + \
        "?seasonId=" + str(self.year)

        print(url)

        try:
            r=requests.get(url)
        except:
            print("Error Retrieving URL: Please ensure league ID is correct.")
            return None

        # Previous seasons return a list of 1 with a JSON object inside for some reason
        #TODO return data as a dataframe

        #return r.json()

        tms= r.json()[0]
        print(tms)

        for tm in tms['members']:
            print(tm)


my_season_2018=league_data_prv(league_id=819126, year=2020).get_data()

