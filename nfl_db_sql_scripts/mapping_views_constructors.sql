CREATE VIEW ff_def_mapping AS (
	#Used to create an easily refreshable mapping table to compare defense fantasy "players" to the actual nfl players that constitute it
	WITH fan AS (SELECT 
		g.week_no,
		p.player_id,
		LEFT(p.player_id, 3) as nfl_team_id
	FROM fact_ff_performance as p

	LEFT JOIN dim_ff_games as g 
		ON g.game_id = p.game_id
		
	WHERE 
		RIGHT(p.player_id,3) ='DEF'
		
	GROUP BY 
		1, 2
	), nfl AS (
		SELECT 
			p.team_id,
			g.game_id,
			g.week_no,
			p.player_id,
			pl.position,
			pl.first_name,
			pl.last_name
		FROM fact_nfl_performance as p
		
		INNER JOIN dim_nfl_games as g
			ON g.game_id = p.game_id
			
		INNER JOIN dim_nfl_players as pl
			ON pl.player_id = p.player_id
			
		WHERE 
			1=1
			AND pl.position IS NOT NULL
			AND pl.position NOT IN (
				'QB',
				'RB',
				'WR',
				'FB',
				'TE',
				'LT',
				'LG',
				'C',
				'RG',
				'RT',
				'K',
				'P'
			)
)

SELECT 
	f.week_no,
    f.player_id as ff_player_id ,
    n.team_id as nfl_team_id,
    n.game_id as nfl_game_id,
    n.player_id as nfl_player_id,
    n.position,
    n.first_name,
    n.last_name
FROM fan as f

LEFT JOIN nfl as n 
	ON n.team_id=f.nfl_team_id
    AND n.week_no = f.week_no
    
ORDER BY 
	f.week_no,
    f.player_id
)
    ;
    


SELECT
*
FROM dim_ff_teams;


# Making a view that just pulls together all defensive player performances 
SELECT 
	f.game_id as ff_game_id,
    f.team_id as ff_team_id,
    f.player_id as ff_player_id,
    g.week_no,
    m.nfl_player_id,
    m.position,
    m.first_name,
    m.last_name,
    n.interceptions,
    n.yards_returned_from_interception,
    n.interceptions_returned_for_touchdown,
    n.longest_interception_return,
    n.passes_defended,
    n.sacks,
    n.combined_tackles,
    n.solo_tackles,
    n.assists_on_tackles,
    n.tackles_for_loss,
    n.quarterback_hits,
    n.fumbles_recovered,
    n.yards_recovered_from_fumble,
    n.fumbles_recovered_for_touchdown,
    n.fumbles_forced,
    f.actual_pts,
    f.projected_pts
    
FROM fact_ff_performance as f

INNER JOIN dim_ff_games as g
	ON f.game_id = g.game_id

LEFT JOIN ff_def_mapping as m
	ON m.ff_player_id = f.player_id
    AND m.week_no = g.week_no

LEFT JOIN fact_nfl_performance as n
	ON m.nfl_player_id=n.player_id
    AND m.nfl_game_id = n.game_id

WHERE
	f.pos ='Def'
    
ORDER BY 
	g.week_no,
    f.player_id

;