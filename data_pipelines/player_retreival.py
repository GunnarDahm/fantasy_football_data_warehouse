# intended to retrive the team information


import mysql.connector


def get_player_data(name):
    # establishing connection and cursor
    cnx = mysql.connector.connect(user='nfl_retrieval_app',
                                  password='indesCYTJd2cLgt7LoAQ',
                                  host='localhost',
                                  database='nfl',
                                  auth_plugin='mysql_native_password')

    cursor=cnx.cursor()

    # inputting base attributes to the database



    for player in players:

        info=players[player]

        add_player = ("INSERT INTO players (first_name ,last_name ,position ,team_id, birth_day, college, height, weight) "
                      "VALUES (%(first_name)s,%(last_name)s, %(position)s, %(team_id)s, %(birth_day)s,%(college)s,%(height)s,"
                      "%(weight)s)")

        #input cleaning

        if len(str(info.birthdate))>=8:
            birth_day_info=str(info.birthdate).split('/')
            birth_day=str(birth_day_info[2] + '/' + birth_day_info[0] + '/' + birth_day_info[1])
        else:
            birth_day=None

        if info.team == '':
            team= None
        else:
            team=info.team

        if info.height == '':
            height= None
        else:
            height=info.height

        if info.weight == '':
            weight = None
        else:
            weight = info.weight

        # building the input dictionary
        player_data = {
            'first_name': info.first_name,
            'last_name': info.last_name,
            'position': info.position,
            'team_id': team,
            'birth_day': birth_day,
            'college': info.college,
            'height': height,
            'weight': weight
        }

        cursor.execute(add_player, player_data)

        print('Inputted: ',info.first_name,info.last_name)

    #committing and closing the cursor and connection
    cnx.commit()
    cursor.close()
    cnx.close()