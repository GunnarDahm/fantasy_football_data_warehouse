SELECT 
	t.location,
    t.nickname,
    t.owner_name,
    g.week_no,
    p.player_id,
    n.first_name,
    n.last_name,
    n.position,
    p.pos as slot,
    p.player_status,
    p.projected_pts,
    p.actual_pts,
    p.actual_pts-p.projected_pts as error
FROM fact_ff_performance as p

LEFT JOIN dim_ff_teams as t
	ON t.team_id=p.team_id
    
LEFT JOIN dim_nfl_players as n
	ON n.player_id = p.player_id
    
LEFT JOIN dim_ff_games as g
	ON g.game_id=p.game_id

WHERE 
	t.team_id=8
    AND p.pos !='Bench'

ORDER BY 
	t.owner_name,
    g.week_no,
    p.actual_pts DESC
;

SELECT 
*
FROM dim_ff_games
LIMIT 100;

SELECT 
*
FROM dim_ff_teams;

SELECT 
	g.season,
    g.week_no,
    g.type,
	h.owner_name as home_team,
    g.home_score,
    a.owner_name as away_team,
    g.away_score,
    CASE WHEN g.home_score>g.away_score THEN h.owner_name 
		 WHEN g.home_score<g.away_score THEN a.owner_name
         ELSE 'TIE' END as winner
FROM dim_ff_games as g

LEFT JOIN dim_ff_teams as h
	ON g.home_id = h.team_id
    
LEFT JOIN dim_ff_teams as a 
	ON g.away_id = a.team_id
    
WHERE 
	1=1
    AND 
		(h.owner_name='gunnar.dahm'
		OR
        a.owner_name='gunnar.dahm'
        )

ORDER BY 
	1, 2
        ;