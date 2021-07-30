
### TEAMS TABLE ==============================================================================================
CREATE TABLE teams (
  team_id VARCHAR(3) PRIMARY KEY,
  team_city VARCHAR(20),
  team_name VARCHAR(20)
);

# SELECT DISTINCT team_id FROM teams ;


### PLAYERS TABLE =============================================================================================
CREATE TABLE players (player_id VARCHAR(12) PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
	position VARCHAR(20),
	birth_day DATE,
	height VARCHAR(4),
	weight FLOAT,
	college VARCHAR(40)
    );

# enforcing that the combination of first name, last name, and birthday have to be unique to avoid duplicates 
CREATE UNIQUE INDEX name_birthday
ON players(first_name, last_name, birth_day);

UPDATE players
SET position = NULL
WHERE position="";

# SELECT * FROM players
# WHERE team_id="JAC";


### GAMES TABLE ==================================================================================================
CREATE TABLE games (game_id VARCHAR(12) PRIMARY KEY ,
    home VARCHAR(3),
    away VARCHAR(3),
	home_score FLOAT,
    away_score FLOAT,
	season FLOAT,
	week_no FLOAT,
    game_date DATE,
    
    FOREIGN KEY (home) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (away) REFERENCES teams(team_id) ON DELETE SET NULL
    );

CREATE UNIQUE INDEX team_date
ON games(home, away, game_date);

# SELECT * FROM games WHERE season=2018;

UPDATE games
SET week_no = week_no+1;


### CREATE PERFORMANCE TABLE ======================================================================================
CREATE TABLE performance ( 
game_id VARCHAR(12) NOT NULL,
team_id VARCHAR(3) NOT NULL,
player_id VARCHAR(12) NOT NULL, 
completed_passes FLOAT,
attempted_passes FLOAT,
passing_yards FLOAT,
passing_touchdowns FLOAT,
interceptions_thrown FLOAT,
times_sacked FLOAT,
yards_lost_from_sacks FLOAT,
longest_pass FLOAT,
quarterback_rating FLOAT ,
rush_attempts FLOAT,
rush_yards FLOAT,
rush_touchdowns FLOAT,
longest_rush FLOAT,
times_pass_target FLOAT,
receptions FLOAT,
receiving_yards FLOAT,
receiving_touchdowns FLOAT,
longest_reception FLOAT,
fumbles FLOAT,
fumbles_lost FLOAT,
interceptions FLOAT,
yards_returned_from_interception FLOAT,
interceptions_returned_for_touchdown FLOAT,
longest_interception_return FLOAT,
passes_defended FLOAT,
sacks FLOAT,
combined_tackles FLOAT,
solo_tackles FLOAT,
assists_on_tackles FLOAT,
tackles_for_loss FLOAT,
quarterback_hits FLOAT,
fumbles_recovered FLOAT,
yards_recovered_from_fumble FLOAT,
fumbles_recovered_for_touchdown FLOAT,
fumbles_forced FLOAT,
kickoff_returns FLOAT,
kickoff_return_yards FLOAT,
average_kickoff_return_yards FLOAT,
kickoff_return_touchdown FLOAT,
longest_kickoff_return FLOAT,
punt_returns FLOAT,
punt_return_yards FLOAT,
yards_per_punt_return FLOAT,
punt_return_touchdown FLOAT,
longest_punt_return FLOAT,
extra_points_made FLOAT,
extra_points_attempted FLOAT,
field_goals_made FLOAT,
field_goals_attempted FLOAT,
punts FLOAT,
total_punt_yards FLOAT,
yards_per_punt FLOAT,
longest_punt FLOAT
	#FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE SET NULL,
	#FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    #FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
);

CREATE UNIQUE INDEX player_perf
ON performance(game_id, team_id, player_id);

# SELECT * FROM performance;



