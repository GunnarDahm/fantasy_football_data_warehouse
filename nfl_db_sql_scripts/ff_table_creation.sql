
### TEAMS TABLE ==============================================================================================
CREATE TABLE dim_ff_teams (
  team_id VARCHAR(3) PRIMARY KEY,
  abbrev VARCHAR(4),
  location VARCHAR(20),
  nickname VARCHAR(20),
  owner_name VARCHAR(20)
);
 
 
 ## GAMES TABLE ==================================================================================================
 CREATE TABLE dim_ff_games (game_id VARCHAR(12) PRIMARY KEY ,
 	season FLOAT,
 	week_no FLOAT,
    type VARCHAR(7),
    home_id VARCHAR(3),
    away_id VARCHAR(3),
	home_score FLOAT,
    away_score FLOAT,
    
    FOREIGN KEY (home_id) REFERENCES dim_ff_teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (away_id) REFERENCES dim_ff_teams(team_id) ON DELETE SET NULL
    );


CREATE UNIQUE INDEX team_date
ON dim_ff_games(home_id, away_id, week_no);

### CREATE PERFORMANCE TABLE ======================================================================================
CREATE TABLE fact_ff_performance ( 
game_id VARCHAR(12) NOT NULL,
team_id VARCHAR(3) NOT NULL,
player_id VARCHAR(12) NOT NULL,
pos VARCHAR(10),
player_status VARCHAR(20),
projected_pts FLOAT,
actual_pts FLOAT
);

CREATE UNIQUE INDEX ff_player_perf
ON fact_ff_performance(game_id, team_id, player_id);


#DROP table fact_ff_performance;