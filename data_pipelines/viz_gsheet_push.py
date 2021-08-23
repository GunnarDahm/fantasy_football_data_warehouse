# Used to push mysql data to google sheets, which will then connect to Tableau Public
# This id needed because Tableau Public won't connect directly to MySQL (paid feature)

import pandas as pd
import gspread as g
from gspread_dataframe import set_with_dataframe
import sqlalchemy as sql

engine = sql.create_engine("mysql+pymysql://{}:{}@localhost:3306/nfl".format('nfl_retrieval_app', 'indesCYTJd2cLgt7LoAQ'))

# placeholder query, will likely replace with a full view
# TODO update to push multiple queries as visualization needs are finalized

player_data = engine.execute('''SELECT
	p.first_name,
    p.last_name,
    p.position,
    SUM(f.projected_pts) as total_proj_pts,
    SUM(f.actual_pts) total_act_pts,
    AVG(f.projected_pts) as avg_proj_pts,
    AVG(f.actual_pts) as avg_actual_pts,
    COUNT(f.game_id) as starts
FROM fact_ff_performance as f

INNER JOIN dim_nfl_players as p
	ON f.player_id = p.player_id

WHERE
    1=1

GROUP BY
    1, 2, 3

ORDER BY
    4 DESC

''')

# Convert to df
df = pd.DataFrame(player_data.fetchall())
df.columns = player_data.keys()

#print(p_df.head(10))

# Connecting to google sheets
gc = g.service_account(filename='fantasy-viz-data-connection-9a0d019c14e3.json')
sh = gc.open_by_key('1jTTXJ_VJneTK8HCGh0jt2yP6q3GKBkxYh_MgNvje0Z0')
worksheet = sh.get_worksheet(0) # 0 pulls first sheet

# Clearing content for a refresh, need to update column range in line below
range_of_cells = worksheet.range('A1:Z1000') #-> Select the range you want to clear
for cell in range_of_cells:
    cell.value = ''
worksheet.update_cells(range_of_cells)


# pushing data
set_with_dataframe(worksheet, df)