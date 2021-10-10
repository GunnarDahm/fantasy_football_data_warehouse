import espn_api.football as espn
import pandas as pd

class fantasy_retrieval:
    '''Creates a connection object to the espn '''
    def __init__(self, league_id, year, espn_s2, swid, current_week):
        self.league_id = league_id
        self.year = year
        self.espn_s2 = espn_s2
        self.swid = swid
        self.current_week = current_week
        self.league = espn.League(league_id= league_id, year=year, espn_s2=espn_s2, swid=swid)

    def pull_teams(self):
        '''Retrieves current league team data and returns it as a pandas dataframe'''
        team_data = []

        for team in self.league.teams:
            team_data.append([team.team_abbrev, team.team_id, team.team_name, team.owner])

        team_df =pd.DataFrame(team_data, columns = ['abbrev', 'team_id', 'team_name', 'owner_name'])
        return(team_df)

    def pull_games(self):
        '''Pulls matchup data for defined year and returns a dataframe'''
        game_data=[]

        for week in range(1, (self.current_week+1)):
            for score in self.league.box_scores(week=week):
                game_data.append([week, score.home_team.team_id, score.home_score,
                                  score.away_team.team_id, score.away_score])

        game_df = pd.DataFrame(game_data, columns=['week_no', 'home_id', 'home_score', 'away_id', 'away_score'])
        game_df['game_id'] = str(self.year) + '_' + game_df['week_no'].map(str) + '_' + game_df['home_id'].map(str)

        return(game_df)

    def ff_look_up_player(self, player_name):
        return(None)
        #TODO complete lookup of player_id by name

    def pull_performance(self):
        perf_data =[]
        for week in range(1, (self.current_week+1)):
            for score in self.league.box_scores(week=week):
                game_id = str(self.year)+'_'+str(week)+'_'+str(score.home_team.team_id)

                #grabbing home lineup
                for player in score.home_lineup:
                    perf_data.append([game_id, score.home_team.team_id, None, player.position, player.injuryStatus,
                                      player.projected_points, player.points])
                #grabbing away lineup
                for player in score.away_lineup:
                    perf_data.append([game_id, score.home_team.team_id, None, player.position, player.injuryStatus,
                                  player.projected_points, player.points])

        perf_df = pd.DataFrame(perf_data, columns=['game_id', 'team_id', 'player_id',
                                                   'pos', 'player_status', 'projected_pts', 'actual_pts'])
        return(perf_df)

ff = fantasy_retrieval(league_id=819126,
                     year=2021,
                     espn_s2="AEBz5srHGNwu0R59Kph1V6HlwJ5fEvDV2J3tcsrtJMSFPl37c%2FgTvZgEkOO2yCNUIHYsmcl4Ik6opp5BE4c5GWoFZNUd%2FbVm%2FDyf7XOBpZyZ3EDejSXTDv1aZMhD13Um3ImdsQ%2BfRxDiZX%2BKw3cx%2F6sLV1XJHOS5mbeKvozbGujHQuDS78qVzUofSCqbiMs9LzsFOLOjRBLfXipjUmdCa7ozwW8ceNymLBXoQnZUdqdkjynhuMs9Ovg7QoWLX8kml1GxHYxN9kUm6gRZipwFlVygVNpGcuBt1bDJS6Of2V0FMA%3D%3D",
                     swid="{0581F0A8-617D-47D8-81F0-A8617D37D85B}",
                     current_week=5
                     )

print(ff.pull_performance())
