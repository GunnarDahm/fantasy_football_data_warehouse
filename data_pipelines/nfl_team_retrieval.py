import sportsipy.nfl.teams as nfl
import mysql.connector
import pandas as pd
import sqlalchemy as sql


def update_teams():
    '''
    Updates the teams table in the nfl database for changes in team names or cities
    :return: None, deletes and updates team names and cities in teams table
    '''

    engine = sql.create_engine("mysql+pymysql://nfl_retrieval_app:indesCYTJd2cLgt7LoAQ@localhost:3306/nfl")

    #clearing table
    engine.execute('DELETE FROM teams')

    conf=pd.read_csv(r'C:\Users\Gunnar\my_code\fantasy_football\data_pipelines\conf_mapping.csv')

    teams = nfl.Teams()


    for team in teams:
        team_split=str(team.name).split(' ')
        team_name=team_split[-1]
        team_split.pop(-1)
        team_city = ' '.join(team_split)

        team_data={
            'team_id': team.abbreviation,
            'team_city': team_city,
            'team_name': team_name
        }

        team_data = pd.DataFrame(team_data, index=[0])

        df = team_data.merge(conf, left_on=['team_id'], right_on=['Team_Id'], how='inner').drop(columns=['Team_Id'])

        df.to_sql('teams', con=engine, index=False, if_exists='append')

        print('Inputted {}, {}, {}'.format(team.abbreviation, team_city, team_name))



update_teams()