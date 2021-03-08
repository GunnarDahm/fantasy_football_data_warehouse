import sportsipy.nfl.teams as nfl
import mysql.connector


#establishing connection and cursor
cnx = mysql.connector.connect(user='nfl_retrieval_app',
                              password='indesCYTJd2cLgt7LoAQ',
                              host='localhost',
                              database='nfl',
                              auth_plugin='mysql_native_password')
cursor=cnx.cursor()


def update_teams():
    '''
    Updates the teams table in the nfl database for changes in team names or cities
    :return: None, deletes and updates team names and cities in teams table
    '''
    #clearing table
    clear_table='DELETE FROM teams'
    cursor.execute(clear_table)

    teams = nfl.Teams()

    add_team= ("INSERT INTO teams (team_id, team_city, team_name) VALUES (%(team_id)s,%(team_city)s,%(team_name)s)")

    for team in teams:
        team_split=str(team.name).split(' ')
        team_name=team_split[-1]
        team_split.pop(-1)
        team_city = ' '.join(team_split)

        team_data={
            'team_id':team.abbreviation,
            'team_city':team_city,
            'team_name': team_name,
        }
        cursor.execute(add_team,team_data)

        print('Inputted {}, {}, {}'.format(team.abbreviation, team_city, team_name))

    #committing and closing the cursor and connection
    cnx.commit()
    cursor.close()
    cnx.close()

update_teams()