CREATE TABLE teams (
  team_id VARCHAR(3) PRIMARY KEY,
  team_city VARCHAR(20),
  team_name VARCHAR(20)
);

# SELECT DISTINCT team_id FROM teams ;

CREATE TABLE players (player_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
	position VARCHAR(3),
	birth_day DATE,
	college VARCHAR(40),
	height int,
	weight int
    );

# enforcing that the combination of first name, last name, and birthday have to be unique to avoid duplicates 
CREATE UNIQUE INDEX name_birthday
ON players(first_name, last_name, birth_day);

UPDATE players
SET position = NULL
WHERE position="";

# SELECT * FROM players
# WHERE team_id="JAC";

CREATE TABLE games (game_id INT PRIMARY KEY AUTO_INCREMENT,
    home VARCHAR(3),
    away VARCHAR(3),
	home_score INT,
    away_score INT,
	season INT,
	week_no INT,
    game_date DATE,
    FOREIGN KEY (home) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (away) REFERENCES teams(team_id) ON DELETE SET NULL
    );

# SELECT * FROM games WHERE season=2018;

UPDATE games
SET week_no = week_no+1;

CREATE TABLE performance ( 
	game_id INT NOT NULL,
    team_id VARCHAR(3) NOT NULL,
    player_id INT NOT NULL, 
    passing_att INT,
	passing_cmp INT,
	passing_yds INT,
	passing_tds INT,
	passing_ints INT,
	passing_twopta INT,
	passing_twoptm INT,
	rushing_att INT,
	rushing_yds INT,
	rushing_tds INT,
	rushing_lng INT,
	rushing_lngtd INT,
	rushing_twopta INT,
	rushing_twoptm INT,
	receiving_rec INT,
	receiving_yds INT,
	receiving_tds INT,
	receiving_lng INT,
	receiving_lngtd INT,
	receiving_twopta INT,
	receiving_twoptm INT,
	puntret_ret INT,
	puntret_avg DOUBLE,
	puntret_tds INT,
	puntret_lng INT,
	puntret_lngtd INT,
	kicking_fga INT,
	kicking_fgyds INT,
	kicking_totpfg INT,
	kicking_xpmade INT,
	kicking_xpmissed INT,
	kicking_xpa INT,
	kicking_xpb INT,
	kicking_xptot INT,
	punting_yds INT,
	punting_avg DOUBLE,
	punting_i20 INT,
	punting_lng INT,
	defense_ast INT,
	defense_sk INT,
	defense_int INT,
	defense_ffum INT,
	fumbles_tot INT,
	fumbles_rcv INT,
	fumbles_trcv INT,
	fumbles_yds INT,
	fumbles_lost INT,
	kickret_avg DOUBLE,
	kickret_tds INT,
	kickret_lng INT,
	kickret_lngtd INT,
	defense_tkl INT,
	kickret_ret INT,
	punting_pts INT,
    ff_pts_act INT,
    ff_pts_proj DOUBLE,
	FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE SET NULL,
	FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
);


# SELECT * FROM performance;



