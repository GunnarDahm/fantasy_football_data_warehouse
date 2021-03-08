from nfl_objects.player_data import Player_Data

class Data_Cache:
    '''
    This object is used to generate a cache of player and league data in the ./data directory.
    Specifically, a csv will generated for player data for each individual year specified in generator range
    (See .generate()) as well as league data csv for the current fantasy season
    '''
    def __init__(self, league_id,swid, espn_s2):
        '''
        The following parameters are all necessary to access the ESPN Fantasy Football API

        Note: that swid and espn_s2 are cookie values that must be retrieved through your browser
        For Chrome Users:
        Settings >> Privacy and Security >> Site Settings >> Cookies >> See All Cookies and Site Data>>espn.com

        :param league_id: INT, can be obtained through the URL of your fantasy home
        :param swid: STR, contained in brackets. See Note above for retrieving this value.
        :param espn_s2: STR, ~300 chars. See Note above for retrieving this value.
        '''
        self.league_id = league_id
        self.swid = swid,
        self.espn_s2 = espn_s2

    def __repr__(self):

        return "<Data Cache Generator for League ID:{}>".format(self.league_id)

    def generate(self, beg_year, end_year):
        '''
        Use the generate func to download and cache csv files of current league data
        :param beg_year: INT, used to specify beginning of data range, inclusive.
        :param end_year: INT, used to specify end of data range, inclusive.
        :return: None, downloads csv files to ./data directory
        '''
        for n in range(beg_year,end_year+1):
            try:
                data=Player_Data(league_id=self.league_id,
                            swid=self.swid,
                            espn_s2=self.espn_s2,
                            year=n).get_data()
                data.to_csv("./data/Player Data {}.csv".format(n))



            except:
                print("Could not retrieve player data for {}.".format(n))
                pass
        print("Cache generated.")

        #TODO Add in Fantasy League Generation caching

# generating a cache
Data_Cache(league_id=819126,
         espn_s2="AEBz5srHGNwu0R59Kph1V6HlwJ5fEvDV2J3tcsrtJMSFPl37c%2FgTvZgEkOO2yCNUIHYsmcl4Ik6opp5BE4c5GWoFZNUd%2FbVm%2FDyf7XOBpZyZ3EDejSXTDv1aZMhD13Um3ImdsQ%2BfRxDiZX%2BKw3cx%2F6sLV1XJHOS5mbeKvozbGujHQuDS78qVzUofSCqbiMs9LzsFOLOjRBLfXipjUmdCa7ozwW8ceNymLBXoQnZUdqdkjynhuMs9Ovg7QoWLX8kml1GxHYxN9kUm6gRZipwFlVygVNpGcuBt1bDJS6Of2V0FMA%3D%3D",
         swid = "{0581F0A8-617D-47D8-81F0-A8617D37D85B}"
           ).generate(beg_year=2018,end_year=2020)
