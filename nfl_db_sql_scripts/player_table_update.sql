SELECT
*
FROM dim_nfl_players

WHERE
	last_name='Miller';

# Adding in robbie gould because he isn't in the nfl api
INSERT INTO dim_nfl_players (player_id, first_name, last_name, position, birth_day, height, weight, college)
	VALUES ('gouldrob01','Robbie', 'Gould', 'K', '1982-12-6','6-0', 190, 'Penn St.');
    
# Fix scott to Scotty
UPDATE dim_nfl_players 
SET 
	first_name = 'Scotty'
WHERE 
	player_id = 'MillSc01';