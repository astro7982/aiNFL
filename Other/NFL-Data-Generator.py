import json
from itertools import combinations
from datetime import datetime, timedelta
import random

class NFLTrainingDatasetGenerator:
    def __init__(self):
        self.nfl_teams = [
            "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
            "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
            "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
            "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
            "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
            "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
            "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
            "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
        ]
        
        self.stadiums = {
            "Arizona Cardinals": "State Farm Stadium",
            "Atlanta Falcons": "Mercedes-Benz Stadium",
            "Baltimore Ravens": "M&T Bank Stadium",
            "Buffalo Bills": "Highmark Stadium",
            "Carolina Panthers": "Bank of America Stadium",
            "Chicago Bears": "Soldier Field",
            "Cincinnati Bengals": "Paycor Stadium",
            "Cleveland Browns": "Cleveland Browns Stadium",
            "Dallas Cowboys": "AT&T Stadium",
            "Denver Broncos": "Empower Field at Mile High",
            "Detroit Lions": "Ford Field",
            "Green Bay Packers": "Lambeau Field",
            "Houston Texans": "NRG Stadium",
            "Indianapolis Colts": "Lucas Oil Stadium",
            "Jacksonville Jaguars": "TIAA Bank Field",
            "Kansas City Chiefs": "GEHA Field at Arrowhead Stadium",
            "Las Vegas Raiders": "Allegiant Stadium",
            "Los Angeles Chargers": "SoFi Stadium",
            "Los Angeles Rams": "SoFi Stadium",
            "Miami Dolphins": "Hard Rock Stadium",
            "Minnesota Vikings": "U.S. Bank Stadium",
            "New England Patriots": "Gillette Stadium",
            "New Orleans Saints": "Caesars Superdome",
            "New York Giants": "MetLife Stadium",
            "New York Jets": "MetLife Stadium",
            "Philadelphia Eagles": "Lincoln Financial Field",
            "Pittsburgh Steelers": "Acrisure Stadium",
            "San Francisco 49ers": "Levi's Stadium",
            "Seattle Seahawks": "Lumen Field",
            "Tampa Bay Buccaneers": "Raymond James Stadium",
            "Tennessee Titans": "Nissan Stadium",
            "Washington Commanders": "FedExField"
        }

        self.weather_conditions = [
            {
                "condition": "Clear",
                "temp_range": (65, 75),
                "wind_range": (5, 10),
                "precip": 0,
                "wind_directions": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                "description": "Perfect conditions for all aspects of the game"
            },
            {
                "condition": "Partly Cloudy",
                "temp_range": (60, 80),
                "wind_range": (8, 15),
                "precip": 10,
                "wind_directions": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                "description": "Minimal impact on game strategy"
            },
            {
                "condition": "Rain",
                "temp_range": (55, 65),
                "wind_range": (15, 25),
                "precip": 70,
                "wind_directions": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                "description": "May affect ball security and passing game"
            },
            {
                "condition": "Snow",
                "temp_range": (25, 35),
                "wind_range": (10, 20),
                "precip": 60,
                "wind_directions": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                "description": "Significant impact on footing and ball handling"
            },
            {
                "condition": "Windy",
                "temp_range": (50, 70),
                "wind_range": (20, 30),
                "precip": 0,
                "wind_directions": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                "description": "Will affect kicking and deep passing games"
            }
        ]

        self.positions = {
            "Offense": {
                "QB": ["Starter", "Backup"],
                "RB": ["RB1", "RB2", "RB3"],
                "WR": ["WR1", "WR2", "WR3", "WR4"],
                "TE": ["TE1", "TE2"],
                "OL": ["LT", "LG", "C", "RG", "RT"]
            },
            "Defense": {
                "DL": ["DE", "DT", "NT"],
                "LB": ["OLB", "MLB", "ILB"],
                "DB": ["CB", "SS", "FS"]
            },
            "Special Teams": {
                "K": ["K"],
                "P": ["P"],
                "LS": ["LS"]
            }
        }

        self.injury_types = {
            "Lower Body": ["Ankle", "Knee", "Foot", "Hamstring", "Calf", "Quad", "Hip"],
            "Upper Body": ["Shoulder", "Elbow", "Wrist", "Hand", "Finger", "Chest", "Ribs"],
            "Head/Neck": ["Concussion", "Neck", "Head"],
            "Other": ["Back", "Illness", "Rest", "Personal"]
        }

        self.injury_statuses = ["Questionable", "Doubtful", "Out", "IR"]

        self.stat_ranges = {
            "passing": {
                "attempts": (25, 45),
                "completions": (15, 35),
                "yards": (200, 400),
                "touchdowns": (1, 4),
                "interceptions": (0, 2),
                "longest": (20, 75)
            },
            "rushing": {
                "attempts": (20, 35),
                "yards": (80, 200),
                "touchdowns": (0, 3),
                "fumbles": (0, 2),
                "longest": (10, 50),
                "yards_per_attempt": (3.0, 5.5)
            },
            "receiving": {
                "receptions": (3, 10),
                "yards": (40, 150),
                "touchdowns": (0, 2),
                "targets": (5, 15),
                "longest": (15, 65),
                "yards_per_catch": (8.0, 18.0)
            },
            "defense": {
                "tackles": (2, 12),
                "sacks": (0, 2),
                "interceptions": (0, 1),
                "passes_defended": (0, 3),
                "fumbles_forced": (0, 1),
                "fumbles_recovered": (0, 1)
            },
            "kicking": {
                "field_goals_attempted": (0, 4),
                "field_goals_made": (0, 4),
                "extra_points_attempted": (1, 5),
                "extra_points_made": (1, 5),
                "longest_field_goal": (20, 55)
            },
            "punting": {
                "punts": (2, 8),
                "yards": (80, 400),
                "longest": (35, 65),
                "inside_twenty": (0, 4)
            }
        }

    def _initialize_prompt_templates(self):
        """Initialize all 16 prompt templates exactly matching your system"""
        return {
            "prompt1_game_setup": """# Prompt 1: Game Setup and Betting Focus

You are a professional sports bettor specializing in making the best NFL bet predictions and a statistical genius. I would like your advice on the following game:

## Game in Question
Home Team: {home_team}
Away Team: {away_team}
Venue: {venue}

## Bet Types of Interest
I am specifically looking at the following bet types for this game:
- Moneyline
- Spread
- Over and Under Totals
- Team Totals Over and Under

## Analysis Instructions
1. This is Prompt 1. All subsequent prompts (Prompts 2-16) will refer back to the game information provided here.
2. Use this game information as the reference point for all subsequent analysis prompts.
3. Do not make any predictions until specifically requested.
4. Gather and analyze all relevant data before offering betting advice.

I have recorded this game information and am ready to proceed with the analysis.""",

            "prompt2_weather_injuries": """# Prompt 2: Weather and Injuries Analysis

Retrieved the following data from the Sports Stats Gather NFL API:

## 1. Injury Report
{away_team}:
{away_injuries}

{home_team}:
{home_injuries}

## 2. Game and Weather Details
● Game Time: {game_time}
● Stadium: {venue}
● Weather Condition: {weather_condition}
● Temperature: {temperature}°F
● Precipitation Chance: {precip_chance}%
● Wind Speed: {wind_speed} mph
● Wind Direction: {wind_direction}

Analysis Impact:
1. {weather_impact1}
2. {weather_impact2}
3. {weather_impact3}

Injury Impact Analysis:
1. {injury_impact1}
2. {injury_impact2}
3. {injury_impact3}

Final Analysis:
{final_analysis}""",

            "prompt3_offensive_stats": """# Prompt 3: Passing, Rushing, Receiving - All Games

Retrieved statistics from the Sports Stats Gather NFL API:

## 1. Passing Statistics
Split: All Games
View: Passing

{away_team}:
● ATT: {away_pass_att}
● YDS: {away_pass_yds}
● Y/A: {away_pass_ya}
● LNG: {away_pass_lng}
● TD: {away_pass_td}

{home_team}:
● ATT: {home_pass_att}
● YDS: {home_pass_yds}
● Y/A: {home_pass_ya}
● LNG: {home_pass_lng}
● TD: {home_pass_td}

## 2. Rushing Statistics
Split: All Games
View: Rushing

{away_team}:
● ATT: {away_rush_att}
● YDS: {away_rush_yds}
● Y/A: {away_rush_ya}
● LNG: {away_rush_lng}
● TD: {away_rush_td}
● FUM: {away_rush_fum}

{home_team}:
● ATT: {home_rush_att}
● YDS: {home_rush_yds}
● Y/A: {home_rush_ya}
● LNG: {home_rush_lng}
● TD: {home_rush_td}
● FUM: {home_rush_fum}

## 3. Receiving Statistics
Split: All Games
View: Receiving

{away_team}:
● REC: {away_rec}
● YDS: {away_rec_yds}
● Y/C: {away_rec_yc}
● LNG: {away_rec_lng}
● TD: {away_rec_td}
● TRG: {away_rec_trg}

{home_team}:
● REC: {home_rec}
● YDS: {home_rec_yds}
● Y/C: {home_rec_yc}
● LNG: {home_rec_lng}
● TD: {home_rec_td}
● TRG: {home_rec_trg}

Analysis:
1. Passing Game Comparison: {passing_analysis}
2. Rushing Attack Evaluation: {rushing_analysis}
3. Receiving Efficiency: {receiving_analysis}
4. Key Offensive Trends: {offensive_trends}""",

"prompt4_defensive_stats": """# Prompt 4: Defensive, Punting, Kicking - All Games

Retrieved statistics from the Sports Stats Gather NFL API:

## 1. Defensive Statistics
Split: All Games
View: Defensive

{away_team}:
● ATT: {away_def_att}
● YDS: {away_def_yds}
● Y/A: {away_def_ya}
● LNG: {away_def_lng}
● TD: {away_def_td}
● FUM: {away_def_fum}

{home_team}:
● ATT: {home_def_att}
● YDS: {home_def_yds}
● Y/A: {home_def_ya}
● LNG: {home_def_lng}
● TD: {home_def_td}
● FUM: {home_def_fum}

## 2. Punting Statistics
Split: All Games
View: Punting

{away_team}:
● ATT: {away_punt_att}
● YDS: {away_punt_yds}
● Y/A: {away_punt_ya}
● LNG: {away_punt_lng}

{home_team}:
● ATT: {home_punt_att}
● YDS: {home_punt_yds}
● Y/A: {home_punt_ya}
● LNG: {home_punt_lng}

## 3. Kicking Statistics
Split: All Games
View: Kicking

{away_team}:
● ATT: {away_kick_att}
● YDS: {away_kick_yds}
● Y/A: {away_kick_ya}
● LNG: {away_kick_lng}
● TD: {away_kick_td}

{home_team}:
● ATT: {home_kick_att}
● YDS: {home_kick_yds}
● Y/A: {home_kick_ya}
● LNG: {home_kick_lng}
● TD: {home_kick_td}

Analysis:
1. Defensive Comparison: {defensive_analysis}
2. Punting Impact: {punting_analysis}
3. Kicking Game Assessment: {kicking_analysis}
4. Key Special Teams Trends: {special_teams_trends}""",

            "prompt5_return_special_teams": """# Prompt 5: Return Game, Special Teams - All Games

Retrieved statistics from the Sports Stats Gather NFL API:

## 1. Return Game Statistics
Split: All Games
View: Returning

{away_team}:
● ATT: {away_ret_att}
● YDS: {away_ret_yds}
● Y/A: {away_ret_ya}
● LNG: {away_ret_lng}
● TD: {away_ret_td}
● FUM: {away_ret_fum}

{home_team}:
● ATT: {home_ret_att}
● YDS: {home_ret_yds}
● Y/A: {home_ret_ya}
● LNG: {home_ret_lng}
● TD: {home_ret_td}
● FUM: {home_ret_fum}

## 2. Special Teams Statistics
Split: All Games
View: Special Teams

{away_team}:
● ATT: {away_st_att}
● YDS: {away_st_yds}
● Y/A: {away_st_ya}
● LNG: {away_st_lng}
● TD: {away_st_td}
● FUM: {away_st_fum}

{home_team}:
● ATT: {home_st_att}
● YDS: {home_st_yds}
● Y/A: {home_st_ya}
● LNG: {home_st_lng}
● TD: {home_st_td}
● FUM: {home_st_fum}

Analysis:
1. Return Game Comparison: {return_analysis}
2. Special Teams Efficiency: {special_teams_analysis}
3. Field Position Impact: {field_position_analysis}
4. Game-Changing Potential: {impact_analysis}""",

            "prompt6_home_away_splits": """# Prompt 6: Passing, Rushing, Receiving - Home, Away, Neutral Splits

Retrieved statistics from the Sports Stats Gather NFL API for home/away splits:

## 1. Passing Statistics (Home/Away)
Split: Home (for home team) / Away (for away team)
View: Passing

{away_team} (Away Games):
● ATT: {away_pass_att_road}
● YDS: {away_pass_yds_road}
● Y/A: {away_pass_ya_road}
● LNG: {away_pass_lng_road}
● TD: {away_pass_td_road}

{home_team} (Home Games):
● ATT: {home_pass_att_home}
● YDS: {home_pass_yds_home}
● Y/A: {home_pass_ya_home}
● LNG: {home_pass_lng_home}
● TD: {home_pass_td_home}

## 2. Rushing Statistics (Home/Away)
Split: Home/Away
View: Rushing

{away_team} (Away Games):
● ATT: {away_rush_att_road}
● YDS: {away_rush_yds_road}
● Y/A: {away_rush_ya_road}
● LNG: {away_rush_lng_road}
● TD: {away_rush_td_road}
● FUM: {away_rush_fum_road}

{home_team} (Home Games):
● ATT: {home_rush_att_home}
● YDS: {home_rush_yds_home}
● Y/A: {home_rush_ya_home}
● LNG: {home_rush_lng_home}
● TD: {home_rush_td_home}
● FUM: {home_rush_fum_home}

## 3. Receiving Statistics (Home/Away)
Split: Home/Away
View: Receiving

{away_team} (Away Games):
● REC: {away_rec_road}
● YDS: {away_rec_yds_road}
● Y/C: {away_rec_yc_road}
● LNG: {away_rec_lng_road}
● TD: {away_rec_td_road}
● TRG: {away_rec_trg_road}

{home_team} (Home Games):
● REC: {home_rec_home}
● YDS: {home_rec_yds_home}
● Y/C: {home_rec_yc_home}
● LNG: {home_rec_lng_home}
● TD: {home_rec_td_home}
● TRG: {home_rec_trg_home}

Home/Away Split Analysis:
1. Passing Game Home/Away Impact: {passing_split_analysis}
2. Rushing Attack Location Trends: {rushing_split_analysis}
3. Receiving Performance Splits: {receiving_split_analysis}
4. Overall Home/Away Tendencies: {overall_split_analysis}""",

"prompt7_defensive_home_away": """# Prompt 7: Defensive, Punting, Kicking - Home, Away, Neutral Splits

Retrieved statistics from the Sports Stats Gather NFL API for home/away splits:

## 1. Defensive Statistics
Split: Home (for home team) / Away (for away team)
View: Defensive

{away_team} (Away Games):
● ATT: {away_def_att_road}
● YDS: {away_def_yds_road}
● Y/A: {away_def_ya_road}
● LNG: {away_def_lng_road}
● TD: {away_def_td_road}
● FUM: {away_def_fum_road}

{home_team} (Home Games):
● ATT: {home_def_att_home}
● YDS: {home_def_yds_home}
● Y/A: {home_def_ya_home}
● LNG: {home_def_lng_home}
● TD: {home_def_td_home}
● FUM: {home_def_fum_home}

## 2. Punting Statistics
Split: Home/Away
View: Punting

{away_team} (Away Games):
● ATT: {away_punt_att_road}
● YDS: {away_punt_yds_road}
● Y/A: {away_punt_ya_road}
● LNG: {away_punt_lng_road}

{home_team} (Home Games):
● ATT: {home_punt_att_home}
● YDS: {home_punt_yds_home}
● Y/A: {home_punt_ya_home}
● LNG: {home_punt_lng_home}

## 3. Kicking Statistics
Split: Home/Away
View: Kicking

{away_team} (Away Games):
● ATT: {away_kick_att_road}
● YDS: {away_kick_yds_road}
● Y/A: {away_kick_ya_road}
● LNG: {away_kick_lng_road}
● TD: {away_kick_td_road}

{home_team} (Home Games):
● ATT: {home_kick_att_home}
● YDS: {home_kick_yds_home}
● Y/A: {home_kick_ya_home}
● LNG: {home_kick_lng_home}
● TD: {home_kick_td_home}

Home/Away Split Analysis:
1. Defensive Performance Variation: {defensive_split_analysis}
2. Punting Game Location Impact: {punting_split_analysis}
3. Kicking Success Rate Splits: {kicking_split_analysis}
4. Key Stadium Factors: {stadium_impact_analysis}""",

            "prompt8_returns_home_away": """# Prompt 8: Return Game, Special Teams - Home, Away, Neutral Splits

Retrieved statistics from the Sports Stats Gather NFL API for home/away splits:

## 1. Return Game Statistics
Split: Home/Away
View: Returning

{away_team} (Away Games):
● ATT: {away_ret_att_road}
● YDS: {away_ret_yds_road}
● Y/A: {away_ret_ya_road}
● LNG: {away_ret_lng_road}
● TD: {away_ret_td_road}
● FUM: {away_ret_fum_road}

{home_team} (Home Games):
● ATT: {home_ret_att_home}
● YDS: {home_ret_yds_home}
● Y/A: {home_ret_ya_home}
● LNG: {home_ret_lng_home}
● TD: {home_ret_td_home}
● FUM: {home_ret_fum_home}

## 2. Special Teams Statistics
Split: Home/Away
View: Special Teams

{away_team} (Away Games):
● ATT: {away_st_att_road}
● YDS: {away_st_yds_road}
● Y/A: {away_st_ya_road}
● LNG: {away_st_lng_road}
● TD: {away_st_td_road}
● FUM: {away_st_fum_road}

{home_team} (Home Games):
● ATT: {home_st_att_home}
● YDS: {home_st_yds_home}
● Y/A: {home_st_ya_home}
● LNG: {home_st_lng_home}
● TD: {home_st_td_home}
● FUM: {home_st_fum_home}

Home/Away Split Analysis:
1. Return Game Location Impact: {return_split_analysis}
2. Special Teams Efficiency Splits: {special_teams_split_analysis}
3. Field Position Advantages: {field_position_split_analysis}
4. Weather/Stadium Considerations: {environment_impact_analysis}""",

            "prompt9_recent_offensive": """# Prompt 9: Passing, Rushing, Receiving - Last 2/4 Weeks and Divisional

Retrieved statistics from the Sports Stats Gather NFL API for recent performance:

## 1. Passing Statistics
Split: Last 2 Weeks
View: Passing

{away_team}:
[Last 2 Weeks Stats]
● ATT: {away_pass_att_2wk}
● YDS: {away_pass_yds_2wk}
● Y/A: {away_pass_ya_2wk}
● LNG: {away_pass_lng_2wk}
● TD: {away_pass_td_2wk}

{home_team}:
[Last 2 Weeks Stats]
● ATT: {home_pass_att_2wk}
● YDS: {home_pass_yds_2wk}
● Y/A: {home_pass_ya_2wk}
● LNG: {home_pass_lng_2wk}
● TD: {home_pass_td_2wk}

Split: Last 4 Weeks
View: Passing

{away_team}:
[Last 4 Weeks Stats]
● ATT: {away_pass_att_4wk}
● YDS: {away_pass_yds_4wk}
● Y/A: {away_pass_ya_4wk}
● LNG: {away_pass_lng_4wk}
● TD: {away_pass_td_4wk}

{home_team}:
[Last 4 Weeks Stats]
● ATT: {home_pass_att_4wk}
● YDS: {home_pass_yds_4wk}
● Y/A: {home_pass_ya_4wk}
● LNG: {home_pass_lng_4wk}
● TD: {home_pass_td_4wk}

## 2. Rushing Statistics
[Similar detailed stats for rushing, including 2-week and 4-week splits]

## 3. Receiving Statistics
[Similar detailed stats for receiving, including 2-week and 4-week splits]

Recent Performance Analysis:
1. Passing Trend Analysis: {passing_trend_analysis}
2. Rushing Trend Analysis: {rushing_trend_analysis}
3. Receiving Trend Analysis: {receiving_trend_analysis}
4. Momentum Factors: {momentum_analysis}""",

"prompt10_recent_special_teams": """# Prompt 10: Punting, Kicking - Last 2/4 Weeks and Divisional

Retrieved statistics from the Sports Stats Gather NFL API:

## 1. Punting Statistics
Split: Last 2 Weeks
View: Punting

{away_team}:
● ATT: {away_punt_att_2wk}
● YDS: {away_punt_yds_2wk}
● Y/A: {away_punt_ya_2wk}
● LNG: {away_punt_lng_2wk}

{home_team}:
● ATT: {home_punt_att_2wk}
● YDS: {home_punt_yds_2wk}
● Y/A: {home_punt_ya_2wk}
● LNG: {home_punt_lng_2wk}

Split: Last 4 Weeks
View: Punting
[Repeat format with 4-week stats]

## 2. Kicking Statistics
Split: Last 2 Weeks
View: Kicking

{away_team}:
● ATT: {away_kick_att_2wk}
● YDS: {away_kick_yds_2wk}
● Y/A: {away_kick_ya_2wk}
● LNG: {away_kick_lng_2wk}
● TD: {away_kick_td_2wk}

{home_team}:
● ATT: {home_kick_att_2wk}
● YDS: {home_kick_yds_2wk}
● Y/A: {home_kick_ya_2wk}
● LNG: {home_kick_lng_2wk}
● TD: {home_kick_td_2wk}

Split: Last 4 Weeks
View: Kicking
[Repeat format with 4-week stats]

Recent Performance Analysis:
1. Punting Trends: {punting_trend_analysis}
2. Kicking Efficiency: {kicking_trend_analysis}
3. Field Position Impact: {field_position_trends}
4. Weather Adaptability: {weather_impact_analysis}""",

            "prompt11_recent_returns": """# Prompt 11: Return Game, Special Teams - Last 2/4 Weeks and Divisional

Retrieved statistics from the Sports Stats Gather NFL API:

## 1. Return Game Statistics
[Detailed 2-week and 4-week return stats for both teams]

## 2. Special Teams Statistics
[Detailed 2-week and 4-week special teams stats for both teams]

Recent Performance Analysis:
1. Return Game Trends: {return_trend_analysis}
2. Special Teams Evolution: {special_teams_trend_analysis}
3. Impact Player Performance: {impact_player_analysis}
4. Momentum Factors: {momentum_analysis}""",

            "prompt12_team_defense": """# Prompt 12: Team Defense Analysis

Retrieved from the Sports Stats Gather NFL API:

## 1. Total Yards & Turnovers (Tot Yds & TO) Allowed:
[Detailed defensive stats for both teams]

## 2. Opponent Passing:
[Detailed opponent passing stats]

## 3. Opponent Rushing:
[Detailed opponent rushing stats]

## 4. Opponent Penalties and Scoring:
[Detailed penalty and scoring stats]

Defense Analysis:
1. Overall Defensive Efficiency: {defensive_efficiency_analysis}
2. Pass Defense Assessment: {pass_defense_analysis}
3. Run Defense Evaluation: {run_defense_analysis}
4. Turnover Generation: {turnover_analysis}""",

            "prompt13_pressure_tackles": """# Prompt 13: Team Pass Rushing and Missed Tackles Analysis

Retrieved from the Sports Stats Gather NFL API:

## 1. Blitz Analysis:
[Detailed blitz stats]

## 2. Hurries:
[Detailed hurry stats]

## 3. Quarterback Knockdowns:
[Detailed QB knockdown stats]

## 4. Pressures:
[Detailed pressure stats]

## 5. Missed Tackles:
[Detailed missed tackle stats]

Pressure and Tackle Analysis:
1. Pass Rush Effectiveness: {pass_rush_analysis}
2. QB Pressure Impact: {pressure_impact_analysis}
3. Tackling Efficiency: {tackling_analysis}
4. Game Impact Projection: {impact_projection}""",

            "prompt14_team_stats": """# Prompt 14: Team Penalty, Rushing Play, Third Down Conversion, and Red Zone Scoring Analysis

Retrieved from the Sports Stats Gather NFL API:

[Detailed stats for all categories across different time periods]

Comprehensive Analysis:
1. Penalty Trends: {penalty_analysis}
2. Rushing Tendency: {rushing_tendency_analysis}
3. Third Down Efficiency: {third_down_analysis}
4. Red Zone Success: {red_zone_analysis}""",

            "prompt15_protection_scramble": """# Prompt 15: Team Pass Protection and Scramble Analysis

Retrieved from the Sports Stats Gather NFL API:

[Detailed pass protection and scramble stats]

Protection and Scramble Analysis:
1. Protection Schemes: {protection_analysis}
2. Scramble Effectiveness: {scramble_analysis}
3. Pressure Management: {pressure_management_analysis}
4. Game Impact Assessment: {impact_assessment}""",

            "prompt16_final_analysis": """# Prompt 16: In-Depth Betting Analysis and Probability Assessment

Based on comprehensive data analysis from Prompts 2-15:

## Game Information
Home Team: {home_team} {home_spread}
Away Team: {away_team}
Current Total: {game_total}

## Probability Assessments

1. Moneyline:
- Home Win: {home_ml_prob}%
- Away Win: {away_ml_prob}%

2. Spread:
- Home Cover: {home_spread_prob}%
- Away Cover: {away_spread_prob}%

3. Total:
- Over: {over_prob}%
- Under: {under_prob}%

4. Team Totals:
Home Team Over/Under {home_team_total}:
- Over: {home_over_prob}%
- Under: {home_under_prob}%

Away Team Over/Under {away_team_total}:
- Over: {away_over_prob}%
- Under: {away_under_prob}%

## Key Factors Influencing Probabilities:
1. {key_factor_1}
2. {key_factor_2}
3. {key_factor_3}

## Value Bet Identification:
{value_bets}

## Risk Assessment:
{risk_assessment}

## Final Recommendations:
{final_recommendations}"""
        }

    def generate_dataset(self, num_examples=1000):
        """Generate comprehensive training dataset"""
        training_examples = []
        
        # Generate team matchups
        matchups = list(combinations(self.nfl_teams, 2))
        
        for home_team, away_team in matchups[:num_examples]:
            # Generate complete 16-prompt sequence for each matchup
            game_data = self._generate_game_data(home_team, away_team)
            training_examples.extend(self._generate_complete_analysis(game_data))
        
        return training_examples

    def save_dataset(self, examples, filename="nfl_finetuning_complete.jsonl"):
        """Save dataset in JSONL format for Unsloth"""
        with open(filename, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

    def _generate_game_data(self, home_team, away_team):
        """Generate complete game data set for all analysis"""
        return {
            "home_team": home_team,
            "away_team": away_team,
            "venue": self.stadiums[home_team],
            "weather": self._generate_weather_data(),
            "injuries": self._generate_injury_report(home_team, away_team),
            "offensive_stats": self._generate_offensive_stats(home_team, away_team),
            "defensive_stats": self._generate_defensive_stats(home_team, away_team),
            "special_teams": self._generate_special_teams_stats(home_team, away_team),
            "recent_performance": self._generate_recent_stats(home_team, away_team),
            "team_stats": self._generate_team_stats(home_team, away_team),
            "betting_lines": self._generate_betting_lines()
        }

    def _generate_weather_data(self):
        """Generate realistic weather conditions"""
        weather = random.choice(self.weather_conditions)
        return {
            "condition": weather["condition"],
            "temperature": random.randint(weather["temp_range"][0], weather["temp_range"][1]),
            "wind_speed": random.randint(weather["wind_range"][0], weather["wind_range"][1]),
            "wind_direction": random.choice(weather["wind_directions"]),
            "precipitation_chance": weather["precip"],
            "description": weather["description"]
        }

    def _generate_injury_report(self, home_team, away_team):
        """Generate realistic injury reports for both teams"""
        def generate_team_injuries(team):
            injuries = []
            num_injuries = random.randint(2, 6)
            for _ in range(num_injuries):
                position_group = random.choice(list(self.positions.keys()))
                position = random.choice(list(self.positions[position_group].keys()))
                injury_category = random.choice(list(self.injury_types.keys()))
                injury = random.choice(self.injury_types[injury_category])
                status = random.choice(self.injury_statuses)
                
                injuries.append({
                    "player": f"Player {_+1}",  # In real implementation, use actual player names
                    "position": position,
                    "injury": injury,
                    "status": status,
                    "updated": (datetime.now() - timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d")
                })
            return injuries

        return {
            "home": generate_team_injuries(home_team),
            "away": generate_team_injuries(away_team)
        }

    def _generate_offensive_stats(self, home_team, away_team):
        """Generate comprehensive offensive statistics"""
        def generate_team_offense():
            return {
                "passing": {
                    "attempts": random.randint(self.stat_ranges["passing"]["attempts"][0], 
                                            self.stat_ranges["passing"]["attempts"][1]),
                    "yards": random.randint(self.stat_ranges["passing"]["yards"][0],
                                          self.stat_ranges["passing"]["yards"][1]),
                    "touchdowns": random.randint(self.stat_ranges["passing"]["touchdowns"][0],
                                               self.stat_ranges["passing"]["touchdowns"][1]),
                    "interceptions": random.randint(self.stat_ranges["passing"]["interceptions"][0],
                                                  self.stat_ranges["passing"]["interceptions"][1]),
                    "longest": random.randint(self.stat_ranges["passing"]["longest"][0],
                                            self.stat_ranges["passing"]["longest"][1])
                },
                "rushing": {
                    "attempts": random.randint(self.stat_ranges["rushing"]["attempts"][0],
                                            self.stat_ranges["rushing"]["attempts"][1]),
                    "yards": random.randint(self.stat_ranges["rushing"]["yards"][0],
                                          self.stat_ranges["rushing"]["yards"][1]),
                    "touchdowns": random.randint(self.stat_ranges["rushing"]["touchdowns"][0],
                                               self.stat_ranges["rushing"]["touchdowns"][1]),
                    "fumbles": random.randint(self.stat_ranges["rushing"]["fumbles"][0],
                                            self.stat_ranges["rushing"]["fumbles"][1]),
                    "longest": random.randint(self.stat_ranges["rushing"]["longest"][0],
                                            self.stat_ranges["rushing"]["longest"][1]),
                    "yards_per_attempt": round(random.uniform(self.stat_ranges["rushing"]["yards_per_attempt"][0],
                                                            self.stat_ranges["rushing"]["yards_per_attempt"][1]), 1)
                }
            }
            
        return {
            "home": generate_team_offense(),
            "away": generate_team_offense()
        }

    def _generate_defensive_stats(self, home_team, away_team):
        """Generate comprehensive defensive statistics"""
        def generate_team_defense():
            return {
                "tackles": random.randint(self.stat_ranges["defense"]["tackles"][0],
                                        self.stat_ranges["defense"]["tackles"][1]),
                "sacks": random.randint(self.stat_ranges["defense"]["sacks"][0],
                                      self.stat_ranges["defense"]["sacks"][1]),
                "interceptions": random.randint(self.stat_ranges["defense"]["interceptions"][0],
                                              self.stat_ranges["defense"]["interceptions"][1]),
                "passes_defended": random.randint(self.stat_ranges["defense"]["passes_defended"][0],
                                                self.stat_ranges["defense"]["passes_defended"][1]),
                "fumbles_forced": random.randint(self.stat_ranges["defense"]["fumbles_forced"][0],
                                               self.stat_ranges["defense"]["fumbles_forced"][1]),
                "fumbles_recovered": random.randint(self.stat_ranges["defense"]["fumbles_recovered"][0],
                                                  self.stat_ranges["defense"]["fumbles_recovered"][1])
            }
            
        return {
            "home": generate_team_defense(),
            "away": generate_team_defense()
        }

    def _generate_special_teams_stats(self, home_team, away_team):
        """Generate comprehensive special teams statistics"""
        def generate_team_special_teams():
            return {
                "kicking": {
                    "field_goals_attempted": random.randint(self.stat_ranges["kicking"]["field_goals_attempted"][0],
                                                          self.stat_ranges["kicking"]["field_goals_attempted"][1]),
                    "field_goals_made": random.randint(self.stat_ranges["kicking"]["field_goals_made"][0],
                                                     self.stat_ranges["kicking"]["field_goals_made"][1]),
                    "extra_points_attempted": random.randint(self.stat_ranges["kicking"]["extra_points_attempted"][0],
                                                           self.stat_ranges["kicking"]["extra_points_attempted"][1]),
                    "extra_points_made": random.randint(self.stat_ranges["kicking"]["extra_points_made"][0],
                                                      self.stat_ranges["kicking"]["extra_points_made"][1]),
                    "longest_field_goal": random.randint(self.stat_ranges["kicking"]["longest_field_goal"][0],
                                                       self.stat_ranges["kicking"]["longest_field_goal"][1])
                },
                "punting": {
                    "punts": random.randint(self.stat_ranges["punting"]["punts"][0],
                                          self.stat_ranges["punting"]["punts"][1]),
                    "yards": random.randint(self.stat_ranges["punting"]["yards"][0],
                                          self.stat_ranges["punting"]["yards"][1]),
                    "longest": random.randint(self.stat_ranges["punting"]["longest"][0],
                                            self.stat_ranges["punting"]["longest"][1]),
                    "inside_twenty": random.randint(self.stat_ranges["punting"]["inside_twenty"][0],
                                                  self.stat_ranges["punting"]["inside_twenty"][1])
                },
                "returns": {
                    "kick_returns": random.randint(2, 6),
                    "kick_return_yards": random.randint(40, 150),
                    "punt_returns": random.randint(1, 4),
                    "punt_return_yards": random.randint(20, 80),
                    "return_touchdowns": random.randint(0, 1)
                }
            }
        
        return {
            "home": generate_team_special_teams(),
            "away": generate_team_special_teams()
        }

    def _generate_recent_stats(self, home_team, away_team):
        """Generate recent performance statistics (2-week and 4-week splits)"""
        def generate_team_recent_stats():
            return {
                "last_2_weeks": {
                    "offense": self._generate_offensive_stats(home_team, away_team)["home"],
                    "defense": self._generate_defensive_stats(home_team, away_team)["home"],
                    "special_teams": self._generate_special_teams_stats(home_team, away_team)["home"]
                },
                "last_4_weeks": {
                    "offense": self._generate_offensive_stats(home_team, away_team)["home"],
                    "defense": self._generate_defensive_stats(home_team, away_team)["home"],
                    "special_teams": self._generate_special_teams_stats(home_team, away_team)["home"]
                }
            }
        
        return {
            "home": generate_team_recent_stats(),
            "away": generate_team_recent_stats()
        }

    def _generate_team_stats(self, home_team, away_team):
        """Generate comprehensive team statistics"""
        def generate_team_stats():
            return {
                "penalties_per_game": round(random.uniform(4.0, 8.0), 1),
                "penalty_yards_per_game": round(random.uniform(30.0, 70.0), 1),
                "third_down_conversion": round(random.uniform(35.0, 50.0), 1),
                "fourth_down_conversion": round(random.uniform(40.0, 60.0), 1),
                "red_zone_scoring": round(random.uniform(50.0, 70.0), 1),
                "time_of_possession": f"{random.randint(27, 33)}:{random.randint(0, 59):02d}",
                "sacks_allowed": random.randint(15, 40),
                "qb_hits_allowed": random.randint(30, 80),
                "turnover_differential": random.randint(-10, 10)
            }
        
        return {
            "home": generate_team_stats(),
            "away": generate_team_stats()
        }

    def _generate_betting_lines(self):
        """Generate realistic betting lines"""
        spread = round(random.uniform(-14, 14) * 2) / 2
        total = round(random.uniform(40, 54) * 2) / 2
        home_team_total = round((total / 2) + (spread / 2) * -1, 0)
        away_team_total = round((total / 2) + (spread / 2), 0)
        
        return {
            "spread": spread,
            "total": total,
            "home_team_total": home_team_total,
            "away_team_total": away_team_total,
            "home_ml_odds": self._calculate_moneyline_odds(spread),
            "away_ml_odds": self._calculate_moneyline_odds(-spread)
        }

    def _calculate_moneyline_odds(self, spread):
        """Calculate realistic moneyline odds based on spread"""
        if spread > 0:
            return int(100 + (spread * 20))
        else:
            return int(-120 + (spread * 20))

    def _generate_complete_analysis(self, game_data):
        """Generate complete set of training examples for all 16 prompts"""
        training_examples = []
        
        # Generate example for each prompt
        for i in range(1, 17):
            prompt_template = self.prompt_templates[f"prompt{i}_" + self._get_prompt_name(i)]
            training_examples.append({
                "instruction": self._generate_prompt_instruction(i, game_data),
                "input": "",
                "output": self._format_prompt_response(i, game_data, prompt_template)
            })
        
        return training_examples

    def _get_prompt_name(self, prompt_number):
        """Map prompt numbers to their template names"""
        prompt_names = {
            1: "game_setup",
            2: "weather_injuries",
            3: "offensive_stats",
            4: "defensive_stats",
            5: "return_special_teams",
            6: "home_away_splits",
            7: "defensive_home_away",
            8: "returns_home_away",
            9: "recent_offensive",
            10: "recent_special_teams",
            11: "recent_returns",
            12: "team_defense",
            13: "pressure_tackles",
            14: "team_stats",
            15: "protection_scramble",
            16: "final_analysis"
        }
        return prompt_names[prompt_number]

    def _generate_prompt_instruction(self, prompt_number, game_data):
        """Generate appropriate instruction for each prompt"""
        base_instructions = {
            1: f"Analyze the upcoming game between the {game_data['away_team']} and {game_data['home_team']}, focusing on key stats and betting implications.",
            # Add specific instructions for each prompt 2-16
        }
        return base_instructions.get(prompt_number, f"Continue analysis for Prompt {prompt_number}")

    def _format_prompt_response(self, prompt_number, game_data, template):
        """Format response for each prompt using templates and game data"""
        return template.format(**self._get_template_variables(prompt_number, game_data))

    def _get_template_variables(self, prompt_number, game_data):
    """Get all variables needed for template formatting based on prompt number"""
    base_vars = {
        "home_team": game_data["home_team"],
        "away_team": game_data["away_team"],
        "venue": game_data["venue"]
    }

    if prompt_number == 1:
        return base_vars
    
    elif prompt_number == 2:
        weather = game_data["weather"]
        injuries = game_data["injuries"]
        return {
            **base_vars,
            "away_injuries": self._format_injuries(injuries["away"]),
            "home_injuries": self._format_injuries(injuries["home"]),
            "game_time": datetime.now().strftime("%I:%M %p ET"),
            "weather_condition": weather["condition"],
            "temperature": weather["temperature"],
            "precip_chance": weather["precipitation_chance"],
            "wind_speed": weather["wind_speed"],
            "wind_direction": weather["wind_direction"],
            "weather_impact1": f"Impact on passing game: {self._generate_weather_impact(weather)}",
            "weather_impact2": f"Impact on kicking game: {self._generate_weather_impact(weather)}",
            "weather_impact3": f"Impact on overall game plan: {self._generate_weather_impact(weather)}",
            "injury_impact1": self._generate_injury_impact(injuries, 1),
            "injury_impact2": self._generate_injury_impact(injuries, 2),
            "injury_impact3": self._generate_injury_impact(injuries, 3),
            "final_analysis": self._generate_weather_injury_final_analysis(weather, injuries)
        }

    elif prompt_number == 3:
        off_stats = game_data["offensive_stats"]
        return {
            **base_vars,
            # Away team passing
            "away_pass_att": off_stats["away"]["passing"]["attempts"],
            "away_pass_yds": off_stats["away"]["passing"]["yards"],
            "away_pass_ya": round(off_stats["away"]["passing"]["yards"] / 
                                max(1, off_stats["away"]["passing"]["attempts"]), 1),
            "away_pass_lng": off_stats["away"]["passing"]["longest"],
            "away_pass_td": off_stats["away"]["passing"]["touchdowns"],
            
            # Home team passing
            "home_pass_att": off_stats["home"]["passing"]["attempts"],
            "home_pass_yds": off_stats["home"]["passing"]["yards"],
            "home_pass_ya": round(off_stats["home"]["passing"]["yards"] / 
                                max(1, off_stats["home"]["passing"]["attempts"]), 1),
            "home_pass_lng": off_stats["home"]["passing"]["longest"],
            "home_pass_td": off_stats["home"]["passing"]["touchdowns"],

            # Analysis sections
            "passing_analysis": self._compare_passing_efficiency(off_stats),
            "rushing_analysis": self._compare_rushing_efficiency(off_stats),
            "receiving_analysis": "Receiving analysis placeholder",
            "offensive_trends": "Offensive trends placeholder"
        }

    elif prompt_number == 4:
        # Defensive, Punting, Kicking Stats
        def_stats = game_data["defensive_stats"]
        special_teams = game_data["special_teams"]
        return {
            **base_vars,
            # Away team defensive stats
            "away_def_att": def_stats["away"]["tackles"],
            "away_def_yds": def_stats["away"]["passes_defended"],
            "away_def_ya": round(def_stats["away"]["passes_defended"] / def_stats["away"]["tackles"], 1),
            "away_def_lng": max(30, random.randint(35, 50)),  # Simulated longest play allowed
            "away_def_td": random.randint(0, 2),  # Simulated TDs allowed
            "away_def_fum": def_stats["away"]["fumbles_forced"],
            
            # Home team defensive stats
            "home_def_att": def_stats["home"]["tackles"],
            "home_def_yds": def_stats["home"]["passes_defended"],
            "home_def_ya": round(def_stats["home"]["passes_defended"] / def_stats["home"]["tackles"], 1),
            "home_def_lng": max(30, random.randint(35, 50)),
            "home_def_td": random.randint(0, 2),
            "home_def_fum": def_stats["home"]["fumbles_forced"],
            
            # Away team punting
            "away_punt_att": special_teams["away"]["punting"]["punts"],
            "away_punt_yds": special_teams["away"]["punting"]["yards"],
            "away_punt_ya": round(special_teams["away"]["punting"]["yards"] / max(1, special_teams["away"]["punting"]["punts"]), 1),
            "away_punt_lng": special_teams["away"]["punting"]["longest"],
            
            # Home team punting
            "home_punt_att": special_teams["home"]["punting"]["punts"],
            "home_punt_yds": special_teams["home"]["punting"]["yards"],
            "home_punt_ya": round(special_teams["home"]["punting"]["yards"] / max(1, special_teams["home"]["punting"]["punts"]), 1),
            "home_punt_lng": special_teams["home"]["punting"]["longest"],
            
            # Away team kicking
            "away_kick_att": special_teams["away"]["kicking"]["field_goals_attempted"],
            "away_kick_yds": special_teams["away"]["kicking"]["field_goals_made"] * 40,  # Estimated average
            "away_kick_ya": round(40.0, 1),  # Average field goal distance
            "away_kick_lng": special_teams["away"]["kicking"]["longest_field_goal"],
            "away_kick_td": 0,  # Kickers don't score TDs
            
            # Home team kicking
            "home_kick_att": special_teams["home"]["kicking"]["field_goals_attempted"],
            "home_kick_yds": special_teams["home"]["kicking"]["field_goals_made"] * 40,
            "home_kick_ya": round(40.0, 1),
            "home_kick_lng": special_teams["home"]["kicking"]["longest_field_goal"],
            "home_kick_td": 0,
            
            # Analysis sections
            "defensive_analysis": self._generate_defensive_analysis(def_stats),
            "punting_analysis": self._generate_punting_analysis(special_teams),
            "kicking_analysis": self._generate_kicking_analysis(special_teams),
            "special_teams_trends": self._generate_special_teams_trends(special_teams)
        }

    elif prompt_number == 5:
        # Return Game and Special Teams Stats
        special_teams = game_data["special_teams"]
        return {
            **base_vars,
            # Away team return stats
            "away_ret_att": special_teams["away"]["returns"]["kick_returns"] + special_teams["away"]["returns"]["punt_returns"],
            "away_ret_yds": special_teams["away"]["returns"]["kick_return_yards"] + special_teams["away"]["returns"]["punt_return_yards"],
            "away_ret_ya": round((special_teams["away"]["returns"]["kick_return_yards"] + special_teams["away"]["returns"]["punt_return_yards"]) / 
                               max(1, special_teams["away"]["returns"]["kick_returns"] + special_teams["away"]["returns"]["punt_returns"]), 1),
            "away_ret_lng": max(25, random.randint(30, 60)),
            "away_ret_td": special_teams["away"]["returns"]["return_touchdowns"],
            "away_ret_fum": random.randint(0, 1),
            
            # Home team return stats
            "home_ret_att": special_teams["home"]["returns"]["kick_returns"] + special_teams["home"]["returns"]["punt_returns"],
            "home_ret_yds": special_teams["home"]["returns"]["kick_return_yards"] + special_teams["home"]["returns"]["punt_return_yards"],
            "home_ret_ya": round((special_teams["home"]["returns"]["kick_return_yards"] + special_teams["home"]["returns"]["punt_return_yards"]) /
                               max(1, special_teams["home"]["returns"]["kick_returns"] + special_teams["home"]["returns"]["punt_returns"]), 1),
            "home_ret_lng": max(25, random.randint(30, 60)),
            "home_ret_td": special_teams["home"]["returns"]["return_touchdowns"],
            "home_ret_fum": random.randint(0, 1),
            
            # Analysis sections
            "return_analysis": self._generate_return_analysis(special_teams),
            "special_teams_analysis": self._generate_special_teams_analysis(special_teams),
            "field_position_analysis": self._generate_field_position_analysis(special_teams),
            "impact_analysis": self._generate_impact_analysis(special_teams)
        }

    elif prompt_number == 6:
        # Home/Away Splits - Offensive Stats
        recent_stats = game_data["recent_performance"]
        return {
            **base_vars,
            # Away team road passing stats
            "away_pass_att_road": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["attempts"],
            "away_pass_yds_road": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["yards"],
            "away_pass_ya_road": round(recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["yards"] / 
                                     recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["attempts"], 1),
            "away_pass_lng_road": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["longest"],
            "away_pass_td_road": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["touchdowns"],

            # Home team home passing stats
            "home_pass_att_home": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["attempts"],
            "home_pass_yds_home": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["yards"],
            "home_pass_ya_home": round(recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["yards"] / 
                                     recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["attempts"], 1),
            "home_pass_lng_home": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["longest"],
            "home_pass_td_home": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["touchdowns"],

            # Away team road rushing stats
            "away_rush_att_road": recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["attempts"],
            "away_rush_yds_road": recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["yards"],
            "away_rush_ya_road": recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["yards_per_attempt"],
            "away_rush_lng_road": recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["longest"],
            "away_rush_td_road": recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["touchdowns"],
            "away_rush_fum_road": recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["fumbles"],

            # Home team home rushing stats
            "home_rush_att_home": recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["attempts"],
            "home_rush_yds_home": recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["yards"],
            "home_rush_ya_home": recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["yards_per_attempt"],
            "home_rush_lng_home": recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["longest"],
            "home_rush_td_home": recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["touchdowns"],
            "home_rush_fum_home": recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["fumbles"],

            # Analysis sections
            "passing_split_analysis": self._generate_passing_split_analysis(recent_stats),
            "rushing_split_analysis": self._generate_rushing_split_analysis(recent_stats),
            "receiving_split_analysis": self._generate_receiving_split_analysis(recent_stats),
            "overall_split_analysis": self._generate_overall_split_analysis(recent_stats)
        }

    elif prompt_number == 7:
        # Home/Away Splits - Defensive Stats
        recent_stats = game_data["recent_performance"]
        return {
            **base_vars,
            # Away team road defensive stats
            "away_def_att_road": recent_stats["away"]["last_4_weeks"]["defense"]["tackles"],
            "away_def_yds_road": recent_stats["away"]["last_4_weeks"]["defense"]["passes_defended"],
            "away_def_ya_road": round(recent_stats["away"]["last_4_weeks"]["defense"]["passes_defended"] / 
                                    max(1, recent_stats["away"]["last_4_weeks"]["defense"]["tackles"]), 1),
            "away_def_lng_road": max(30, random.randint(35, 50)),
            "away_def_td_road": random.randint(0, 2),
            "away_def_fum_road": recent_stats["away"]["last_4_weeks"]["defense"]["fumbles_forced"],

            # Home team home defensive stats
            "home_def_att_home": recent_stats["home"]["last_4_weeks"]["defense"]["tackles"],
            "home_def_yds_home": recent_stats["home"]["last_4_weeks"]["defense"]["passes_defended"],
            "home_def_ya_home": round(recent_stats["home"]["last_4_weeks"]["defense"]["passes_defended"] / 
                                    max(1, recent_stats["home"]["last_4_weeks"]["defense"]["tackles"]), 1),
            "home_def_lng_home": max(30, random.randint(35, 50)),
            "home_def_td_home": random.randint(0, 2),
            "home_def_fum_home": recent_stats["home"]["last_4_weeks"]["defense"]["fumbles_forced"],

            # Analysis sections
            "defensive_split_analysis": self._generate_defensive_split_analysis(recent_stats),
            "punting_split_analysis": self._generate_punting_split_analysis(recent_stats),
            "kicking_split_analysis": self._generate_kicking_split_analysis(recent_stats),
            "stadium_impact_analysis": self._generate_stadium_impact_analysis(game_data)
        }

    elif prompt_number == 8:
        # Home/Away Splits - Returns and Special Teams
        recent_stats = game_data["recent_performance"]
        return {
            **base_vars,
            # Away team road return stats
            "away_ret_att_road": recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["kick_returns"],
            "away_ret_yds_road": recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["kick_return_yards"],
            "away_ret_ya_road": round(recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["kick_return_yards"] / 
                                    max(1, recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["kick_returns"]), 1),
            "away_ret_lng_road": max(25, random.randint(30, 60)),
            "away_ret_td_road": recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["return_touchdowns"],
            "away_ret_fum_road": random.randint(0, 1),

            # Home team home return stats
            "home_ret_att_home": recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["kick_returns"],
            "home_ret_yds_home": recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["kick_return_yards"],
            "home_ret_ya_home": round(recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["kick_return_yards"] / 
                                    max(1, recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["kick_returns"]), 1),
            "home_ret_lng_home": max(25, random.randint(30, 60)),
            "home_ret_td_home": recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["return_touchdowns"],
            "home_ret_fum_home": random.randint(0, 1),

            # Analysis sections
            "return_split_analysis": self._generate_return_split_analysis(recent_stats),
            "special_teams_split_analysis": self._generate_special_teams_split_analysis(recent_stats),
            "field_position_split_analysis": self._generate_field_position_split_analysis(recent_stats),
            "environment_impact_analysis": self._generate_environment_impact_analysis(game_data)
        }

    elif prompt_number == 9:
        # Recent Performance - Offensive Stats
        recent_stats = game_data["recent_performance"]
        return {
            **base_vars,
            # Away team 2-week stats
            "away_pass_att_2wk": recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["attempts"],
            "away_pass_yds_2wk": recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"],
            "away_pass_ya_2wk": round(recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                                    max(1, recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["attempts"]), 1),
            "away_pass_lng_2wk": recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["longest"],
            "away_pass_td_2wk": recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["touchdowns"],

            # Away team 4-week stats
            "away_pass_att_4wk": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["attempts"],
            "away_pass_yds_4wk": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["yards"],
            "away_pass_ya_4wk": round(recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["yards"] / 
                                    max(1, recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["attempts"]), 1),
            "away_pass_lng_4wk": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["longest"],
            "away_pass_td_4wk": recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["touchdowns"],

            # Home team 2-week stats
            "home_pass_att_2wk": recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["attempts"],
            "home_pass_yds_2wk": recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"],
            "home_pass_ya_2wk": round(recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                                    max(1, recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["attempts"]), 1),
            "home_pass_lng_2wk": recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["longest"],
            "home_pass_td_2wk": recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["touchdowns"],

            # Home team 4-week stats
            "home_pass_att_4wk": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["attempts"],
            "home_pass_yds_4wk": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["yards"],
            "home_pass_ya_4wk": round(recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["yards"] / 
                                    max(1, recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["attempts"]), 1),
            "home_pass_lng_4wk": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["longest"],
            "home_pass_td_4wk": recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["touchdowns"],

            # Analysis sections
            "passing_trend_analysis": self._generate_passing_trend_analysis(recent_stats),
            "rushing_trend_analysis": self._generate_rushing_trend_analysis(recent_stats),
            "receiving_trend_analysis": self._generate_receiving_trend_analysis(recent_stats),
            "momentum_analysis": self._generate_momentum_analysis(recent_stats)
        }

    elif prompt_number == 10:
        # Punting, Kicking - Recent Performance
        recent_stats = game_data["recent_performance"]
        return {
            **base_vars,
            # Away team 2-week punting stats
            "away_punt_att_2wk": recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["punts"],
            "away_punt_yds_2wk": recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["yards"],
            "away_punt_ya_2wk": round(recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                                    max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["punts"]), 1),
            "away_punt_lng_2wk": recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["longest"],

            # Home team 2-week punting stats
            "home_punt_att_2wk": recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["punts"],
            "home_punt_yds_2wk": recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["yards"],
            "home_punt_ya_2wk": round(recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                                    max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["punts"]), 1),
            "home_punt_lng_2wk": recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["longest"],

            # Away team 4-week punting stats
            "away_punt_att_4wk": recent_stats["away"]["last_4_weeks"]["special_teams"]["punting"]["punts"],
            "away_punt_yds_4wk": recent_stats["away"]["last_4_weeks"]["special_teams"]["punting"]["yards"],
            "away_punt_ya_4wk": round(recent_stats["away"]["last_4_weeks"]["special_teams"]["punting"]["yards"] / 
                                    max(1, recent_stats["away"]["last_4_weeks"]["special_teams"]["punting"]["punts"]), 1),
            "away_punt_lng_4wk": recent_stats["away"]["last_4_weeks"]["special_teams"]["punting"]["longest"],

            # Home team 4-week punting stats
            "home_punt_att_4wk": recent_stats["home"]["last_4_weeks"]["special_teams"]["punting"]["punts"],
            "home_punt_yds_4wk": recent_stats["home"]["last_4_weeks"]["special_teams"]["punting"]["yards"],
            "home_punt_ya_4wk": round(recent_stats["home"]["last_4_weeks"]["special_teams"]["punting"]["yards"] / 
                                    max(1, recent_stats["home"]["last_4_weeks"]["special_teams"]["punting"]["punts"]), 1),
            "home_punt_lng_4wk": recent_stats["home"]["last_4_weeks"]["special_teams"]["punting"]["longest"],

            # Analysis sections
            "punting_trend_analysis": self._generate_punting_trend_analysis(recent_stats),
            "kicking_trend_analysis": self._generate_kicking_trend_analysis(recent_stats),
            "field_position_trends": self._generate_field_position_trends(recent_stats),
            "weather_impact_analysis": self._generate_weather_impact_analysis(game_data)
        }

    elif prompt_number == 11:
        # Return Game, Special Teams - Recent Performance
        recent_stats = game_data["recent_performance"]
        return {
            **base_vars,
            "return_trend_analysis": self._generate_return_trend_analysis(recent_stats),
            "special_teams_trend_analysis": self._generate_special_teams_trend_analysis(recent_stats),
            "impact_player_analysis": self._generate_impact_player_analysis(recent_stats),
            "momentum_analysis": self._generate_momentum_analysis(recent_stats)
        }
    
    elif prompt_number == 12:
        # Team Defense Analysis
        def_stats = game_data["defensive_stats"]
        return {
            **base_vars,
            "defensive_efficiency_analysis": self._compare_defensive_efficiency(def_stats),
            "pass_defense_analysis": self._generate_pass_defense_analysis(def_stats),
            "run_defense_analysis": self._generate_run_defense_analysis(def_stats),
            "turnover_analysis": self._generate_turnover_analysis(def_stats)
        }

    elif prompt_number == 13:
        # Pass Rush and Tackle Analysis
        def_stats = game_data["defensive_stats"]
        return {
            **base_vars,
            "pass_rush_analysis": self._generate_pass_rush_analysis(def_stats),
            "pressure_impact_analysis": self._generate_pressure_impact_analysis(def_stats),
            "tackling_analysis": self._generate_tackling_analysis(def_stats),
            "impact_projection": self._generate_impact_projection(def_stats)
        }

    elif prompt_number == 14:
        # Team Stats Analysis
        team_stats = game_data["team_stats"]
        return {
            **base_vars,
            "penalty_analysis": self._generate_penalty_analysis(team_stats),
            "rushing_tendency_analysis": self._generate_rushing_tendency_analysis(team_stats),
            "third_down_analysis": self._generate_third_down_analysis(team_stats),
            "red_zone_analysis": self._generate_red_zone_analysis(team_stats)
        }

    elif prompt_number == 15:
        # Protection and Scramble Analysis
        team_stats = game_data["team_stats"]
        return {
            **base_vars,
            "protection_analysis": self._generate_protection_analysis(team_stats),
            "scramble_analysis": self._generate_scramble_analysis(team_stats),
            "pressure_management_analysis": self._generate_pressure_management_analysis(team_stats),
            "impact_assessment": self._generate_protection_impact_assessment(team_stats)
        }

    elif prompt_number == 16:
        # Final Betting Analysis
        betting_lines = game_data["betting_lines"]
        return {
            **base_vars,
            "home_spread": betting_lines["spread"],
            "game_total": betting_lines["total"],
            "home_ml_prob": self._calculate_win_probability(betting_lines["spread"]),
            "away_ml_prob": self._calculate_win_probability(-betting_lines["spread"]),
            "home_spread_prob": self._calculate_spread_probability(betting_lines["spread"]),
            "away_spread_prob": self._calculate_spread_probability(-betting_lines["spread"]),
            "over_prob": self._calculate_total_probability(betting_lines["total"], "over"),
            "under_prob": self._calculate_total_probability(betting_lines["total"], "under"),
            "home_team_total": betting_lines["home_team_total"],
            "away_team_total": betting_lines["away_team_total"],
            "home_over_prob": self._calculate_team_total_probability(betting_lines["home_team_total"], "over"),
            "home_under_prob": self._calculate_team_total_probability(betting_lines["home_team_total"], "under"),
            "away_over_prob": self._calculate_team_total_probability(betting_lines["away_team_total"], "over"),
            "away_under_prob": self._calculate_team_total_probability(betting_lines["away_team_total"], "under"),
            "key_factor_1": self._generate_key_factor(game_data, 1),
            "key_factor_2": self._generate_key_factor(game_data, 2),
            "key_factor_3": self._generate_key_factor(game_data, 3),
            "value_bets": self._identify_value_bets(game_data, betting_lines),
            "risk_assessment": self._generate_risk_assessment(game_data),
            "final_recommendations": self._generate_final_recommendations(game_data, betting_lines)
        }

def main():
    """Main function to generate and save the dataset"""
    generator = NFLTrainingDatasetGenerator()
    dataset = generator.generate_dataset(num_examples=1000)
    generator.save_dataset(dataset)
    print(f"Generated {len(dataset)} training examples")

if __name__ == "__main__":
    main()