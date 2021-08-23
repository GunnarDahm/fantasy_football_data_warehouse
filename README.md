# fantasy_football_data_warehouse
## Purpose
This repo serves to house the scripts for the creation and upkeep of my fantasy football data warehouse. 
Additionally, some analysis and ml work will be housed here as well.

## Status: In Progress

## To Do:
- Complete ReadMe
- Complete pipelines into fantasy football data warehouse
- Create python analysis objects
- Create Tableau Public Dashboard connected to data warehouse
- Begin work on ML/AI functionalities

## Technologies 
- Python (v3.7)
- MySQL Server
- Jupyter Notebooks
- Tableau Public

## Project Overview
This project seeks to buildout and deploy of full analytics platform for the fantasy football league I am a part.
This fantasy league is hosted on ESPN Fantasy, however I found the available data and analysis somewhat lacking/rigid. 
So this project is broken out into 4 components; the data warehouse, the analysis library,
the self-service dashboard, and the ML models.

### Data Warehouse
The first component that is the data warehouse that will serve every other component of this project. This 

#### Table Structure

Data related to fantasy and nfl team/player performance is stored within 7 tables.
- DIM_Players: Contains a roster of all players that have played in NFL games from the min game date onward.
- DIM_Teams: Contains all nfl teams, their location, and conference information
- DIM_Games: Contains a record for all match-ups in a particular season, as well as score
- FACT_Performance: Each record contains a compound foreign key of Game ID, Team ID, and Player ID. For each record, player
stats such as passing yards, rushing yards, receptions, etc. are tracked. I.E. For Tom Brady at the Tampa Bay Bucs on
the game date of 2/7/2021, here are the stats for his performance.
- DIM_Fantasy Teams: Contains all fantasy teams in the T.O.F.T.B. league and their team owners
- DIM_Fantasy Games: Contains the matchup of all fantasy teams and their respective scores and dates.
- FACT_Fantasy Performance: Each record contains a compound foreign key of Fantasy Game ID, Fantasy Team ID, 
and Player ID. For each record, player fantasy stats and vegas odds are tracked.

##### Entity Relationship Diagram 
![Data Warehouse ERD](.\img\dw_erd.png)
- Will need an intermediary defense view that connects the nfl player concept to the fantasy football player concept

#### Data Pipelines

- nfl_team_retrieval (Status: Complete) : Updates teams in Teams and Fantasy Teams table. 
- nfl_game_retrieval (Status: Complete): Upates game schedules for a specific season for games and fantasy games table
- nfl_player_retrieval (Status: Complete): Updates player table with static information about the player
- nfl_performance_retrieval: (Status: Complete): Updates player performance table 
- ff_team_retrieval: (Status: Complete): 
- ff_game_retrieval (Status: Complete):
- ff_performance_retrieval (Status: Complete): 
- Master Retrieval

### Analysis Library


### Self-Service Dashboard


### ML Modeling