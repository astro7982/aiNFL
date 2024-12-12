#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NFL Training Dataset Generator
----------------------------
Generates comprehensive NFL game data and betting analysis for model training.
"""

import json
import logging
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nfl_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

@dataclass
class WeatherCondition:
    """Weather condition data structure"""
    condition: str
    temp_range: Tuple[int, int]
    wind_range: Tuple[int, int]
    precip: int
    wind_directions: List[str]
    description: str

@dataclass
class InjuryReport:
    """Injury report data structure"""
    player: str
    position: str
    injury: str
    status: str
    updated: str

class NFLTrainingDatasetGenerator:
    """Generates NFL training datasets for betting analysis models"""
    
    def __init__(self):
        """Initialize the NFL Training Dataset Generator with all required data structures"""
        logger.info("Initializing NFL Training Dataset Generator")
        
        try:
            self._initialize_teams_and_stadiums()
            self._initialize_weather_conditions()
            self._initialize_positions()
            self._initialize_injury_types()
            self._initialize_stat_ranges()
            self._initialize_prompt_templates()
            logger.info("Successfully initialized all data structures")
        except Exception as e:
            logger.error(f"Failed to initialize NFL Training Dataset Generator: {str(e)}")
            raise

    def _initialize_teams_and_stadiums(self) -> None:
        """Initialize NFL teams and their corresponding stadiums"""
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
        logger.debug("Initialized teams and stadiums")

    def _initialize_weather_conditions(self) -> None:
        """Initialize weather conditions and their characteristics"""
        self.weather_conditions = [
            WeatherCondition(
                condition="Clear",
                temp_range=(65, 75),
                wind_range=(5, 10),
                precip=0,
                wind_directions=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                description="Perfect conditions for all aspects of the game"
            ),
            WeatherCondition(
                condition="Partly Cloudy",
                temp_range=(60, 80),
                wind_range=(8, 15),
                precip=10,
                wind_directions=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                description="Minimal impact on game strategy"
            ),
            WeatherCondition(
                condition="Rain",
                temp_range=(55, 65),
                wind_range=(15, 25),
                precip=70,
                wind_directions=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                description="May affect ball security and passing game"
            ),
            WeatherCondition(
                condition="Snow",
                temp_range=(25, 35),
                wind_range=(10, 20),
                precip=60,
                wind_directions=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                description="Significant impact on footing and ball handling"
            ),
            WeatherCondition(
                condition="Windy",
                temp_range=(50, 70),
                wind_range=(20, 30),
                precip=0,
                wind_directions=["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
                description="Will affect kicking and deep passing games"
            )
        ]
        logger.debug("Initialized weather conditions")
    def _initialize_positions(self) -> None:
        """Initialize NFL positions and their characteristics"""
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
        logger.debug("Initialized player positions")

    def _initialize_injury_types(self) -> None:
        """Initialize injury types and statuses"""
        self.injury_types = {
            "Lower Body": ["Ankle", "Knee", "Foot", "Hamstring", "Calf", "Quad", "Hip"],
            "Upper Body": ["Shoulder", "Elbow", "Wrist", "Hand", "Finger", "Chest", "Ribs"],
            "Head/Neck": ["Concussion", "Neck", "Head"],
            "Other": ["Back", "Illness", "Rest", "Personal"]
        }

        self.injury_statuses = ["Questionable", "Doubtful", "Out", "IR"]
        logger.debug("Initialized injury types and statuses")

    def _initialize_stat_ranges(self) -> None:
        """Initialize statistical ranges for various game metrics"""
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
        logger.debug("Initialized statistical ranges")

    def _initialize_prompt_templates(self) -> Dict[str, str]:
        """Initialize all 16 prompt templates for game analysis"""
        logger.info("Initializing prompt templates")
        
        try:
            self.prompt_templates = {
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
            logger.info("Successfully initialized all prompt templates")
            return self.prompt_templates
        except Exception as e:
            logger.error(f"Failed to initialize prompt templates: {str(e)}")
            raise

    @staticmethod
    def _validate_team_names(home_team: str, away_team: str) -> None:
        """Validate team names are in the NFL teams list"""
        if not isinstance(home_team, str) or not isinstance(away_team, str):
            raise ValueError("Team names must be strings")
        if home_team == away_team:
            raise ValueError("Home and away teams cannot be the same")
            
    def generate_dataset(self, num_examples: int = 1000) -> List[Dict]:
        """Generate comprehensive training dataset"""
        logger.info(f"Generating dataset with {num_examples} examples")
        training_examples = []
        
        try:
            # Generate team matchups
            matchups = list(combinations(self.nfl_teams, 2))
            
            for home_team, away_team in matchups[:num_examples]:
                logger.debug(f"Generating data for {away_team} @ {home_team}")
                
                # Validate team names
                self._validate_team_names(home_team, away_team)
                
                # Generate complete 16-prompt sequence for each matchup
                game_data = self._generate_game_data(home_team, away_team)
                training_examples.extend(self._generate_complete_analysis(game_data))
            
            logger.info(f"Successfully generated {len(training_examples)} training examples")
            return training_examples
            
        except Exception as e:
            logger.error(f"Failed to generate dataset: {str(e)}")
            raise

    def save_dataset(self, examples: List[Dict], filename: str = "nfl_finetuning_complete.jsonl") -> None:
        """Save dataset in JSONL format for fine-tuning"""
        logger.info(f"Saving dataset to {filename}")
        
        try:
            output_path = Path(filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for example in examples:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')
                    
            logger.info(f"Successfully saved {len(examples)} examples to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save dataset: {str(e)}")
            raise

    def _generate_game_data(self, home_team: str, away_team: str) -> Dict:
        """Generate complete game data set for all analysis"""
        logger.debug(f"Generating game data for {away_team} @ {home_team}")
        
        try:
            game_data = {
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
            
            return game_data
            
        except Exception as e:
            logger.error(f"Failed to generate game data: {str(e)}")
            raise

    def _generate_weather_data(self) -> Dict:
        """Generate realistic weather conditions"""
        logger.debug("Generating weather data")
        
        try:
            weather = random.choice(self.weather_conditions)
            weather_data = {
                "condition": weather.condition,
                "temperature": random.randint(weather.temp_range[0], weather.temp_range[1]),
                "wind_speed": random.randint(weather.wind_range[0], weather.wind_range[1]),
                "wind_direction": random.choice(weather.wind_directions),
                "precipitation_chance": weather.precip,
                "description": weather.description
            }
            return weather_data
            
        except Exception as e:
            logger.error(f"Failed to generate weather data: {str(e)}")
            raise

    def _generate_injury_report(self, home_team: str, away_team: str) -> Dict[str, List[InjuryReport]]:
        """Generate realistic injury reports for both teams"""
        logger.debug(f"Generating injury reports for {away_team} @ {home_team}")
        
        def generate_team_injuries(team: str) -> List[InjuryReport]:
            injuries = []
            num_injuries = random.randint(2, 6)
            
            try:
                for i in range(num_injuries):
                    position_group = random.choice(list(self.positions.keys()))
                    position = random.choice(list(self.positions[position_group].keys()))
                    injury_category = random.choice(list(self.injury_types.keys()))
                    injury = random.choice(self.injury_types[injury_category])
                    status = random.choice(self.injury_statuses)
                    
                    injury_report = InjuryReport(
                        player=f"Player {i+1}",  # In real implementation, use actual player names
                        position=position,
                        injury=injury,
                        status=status,
                        updated=(datetime.now() - timedelta(days=random.randint(0, 3))).strftime("%Y-%m-%d")
                    )
                    injuries.append(injury_report)
                    
                return injuries
                
            except Exception as e:
                logger.error(f"Failed to generate team injuries: {str(e)}")
                raise

        return {
            "home": generate_team_injuries(home_team),
            "away": generate_team_injuries(away_team)
        }

    def _generate_offensive_stats(self, home_team: str, away_team: str) -> Dict:
        """Generate comprehensive offensive statistics"""
        logger.debug(f"Generating offensive stats for {away_team} @ {home_team}")
        
        def generate_team_offense() -> Dict:
            try:
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
            except Exception as e:
                logger.error(f"Failed to generate team offense stats: {str(e)}")
                raise
                
        return {
            "home": generate_team_offense(),
            "away": generate_team_offense()
        }
    
    def _generate_defensive_stats(self, home_team: str, away_team: str) -> Dict:
        """Generate comprehensive defensive statistics"""
        logger.debug(f"Generating defensive stats for {away_team} @ {home_team}")
        
        def generate_team_defense() -> Dict:
            try:
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
            except Exception as e:
                logger.error(f"Failed to generate team defense stats: {str(e)}")
                raise
                
        return {
            "home": generate_team_defense(),
            "away": generate_team_defense()
        }

    def _generate_special_teams_stats(self, home_team: str, away_team: str) -> Dict:
        """Generate comprehensive special teams statistics"""
        logger.debug(f"Generating special teams stats for {away_team} @ {home_team}")
        
        def generate_team_special_teams() -> Dict:
            try:
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
            except Exception as e:
                logger.error(f"Failed to generate team special teams stats: {str(e)}")
                raise
        
        return {
            "home": generate_team_special_teams(),
            "away": generate_team_special_teams()
        }

    def _generate_recent_stats(self, home_team: str, away_team: str) -> Dict:
        """Generate recent performance statistics (2-week and 4-week splits)"""
        logger.debug(f"Generating recent performance stats for {away_team} @ {home_team}")
        
        def generate_team_recent_stats() -> Dict:
            try:
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
            except Exception as e:
                logger.error(f"Failed to generate team recent stats: {str(e)}")
                raise
        
        return {
            "home": generate_team_recent_stats(),
            "away": generate_team_recent_stats()
        }
    
    def _generate_team_stats(self, home_team: str, away_team: str) -> Dict:
        """Generate comprehensive team statistics"""
        logger.debug(f"Generating team stats for {away_team} @ {home_team}")
        
        def generate_team_stats() -> Dict:
            try:
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
            except Exception as e:
                logger.error(f"Failed to generate team stats: {str(e)}")
                raise
        
        return {
            "home": generate_team_stats(),
            "away": generate_team_stats()
        }

    def _generate_betting_lines(self) -> Dict:
        """Generate realistic betting lines"""
        logger.debug("Generating betting lines")
        
        try:
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
        except Exception as e:
            logger.error(f"Failed to generate betting lines: {str(e)}")
            raise

    def _calculate_moneyline_odds(self, spread: float) -> int:
        """Calculate realistic moneyline odds based on spread"""
        try:
            if spread > 0:
                return int(100 + (spread * 20))
            return int(-120 + (spread * 20))
        except Exception as e:
            logger.error(f"Failed to calculate moneyline odds: {str(e)}")
            raise

    def _format_injuries(self, injuries: List[InjuryReport]) -> str:
        """Format injury report into readable string"""
        try:
            if not injuries:
                return "No injuries to report"
                
            injury_lines = []
            for injury in injuries:
                injury_lines.append(
                    f"- {injury.player} ({injury.position}): {injury.injury} - {injury.status}"
                )
            return "\n".join(injury_lines)
        except Exception as e:
            logger.error(f"Failed to format injuries: {str(e)}")
            raise

    def _generate_weather_impact(self, weather: Dict) -> str:
        """Generate weather impact analysis"""
        try:
            if weather["condition"] in ["Snow", "Rain"]:
                return "heavy impact on game strategy"
            elif weather["wind_speed"] > 20:
                return "significant wind factor"
            elif weather["temperature"] < 32:
                return "cold weather impact"
            elif weather["temperature"] > 85:
                return "heat factor consideration"
            return "minimal weather impact"
        except Exception as e:
            logger.error(f"Failed to generate weather impact: {str(e)}")
            raise

    def _generate_injury_impact(self, injuries: Dict[str, List[InjuryReport]], impact_num: int) -> str:
        """Generate injury impact analysis"""
        try:
            impacts = {
                1: "Key position depth affected",
                2: "Roster adjustments necessary",
                3: "Game plan modifications required"
            }
            return impacts.get(impact_num, "No significant impact")
        except Exception as e:
            logger.error(f"Failed to generate injury impact: {str(e)}")
            raise

    def _generate_weather_injury_final_analysis(self, weather: Dict, injuries: Dict[str, List[InjuryReport]]) -> str:
        """Generate combined weather and injury analysis"""
        try:
            impacts = []
            
            # Weather analysis
            if weather["condition"] in ["Snow", "Rain"]:
                impacts.append("Weather conditions will significantly affect gameplay")
            elif weather["wind_speed"] > 20:
                impacts.append("Strong winds will impact kicking and passing games")
                
            # Injury analysis
            total_injuries = len(injuries["home"]) + len(injuries["away"])
            if total_injuries > 8:
                impacts.append("High injury count could be decisive factor")
            elif total_injuries > 4:
                impacts.append("Multiple injuries may affect team depth")
                
            if not impacts:
                return "No major weather or injury concerns"
            return ". ".join(impacts)
        except Exception as e:
            logger.error(f"Failed to generate weather/injury analysis: {str(e)}")
            raise

    def _generate_team_stats(self, home_team: str, away_team: str) -> Dict:
        """Generate comprehensive team statistics"""
        logger.debug(f"Generating team stats for {away_team} @ {home_team}")
        
        def generate_team_stats() -> Dict:
            try:
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
            except Exception as e:
                logger.error(f"Failed to generate team stats: {str(e)}")
                raise
        
        return {
            "home": generate_team_stats(),
            "away": generate_team_stats()
        }

    def _generate_betting_lines(self) -> Dict:
        """Generate realistic betting lines"""
        logger.debug("Generating betting lines")
        
        try:
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
        except Exception as e:
            logger.error(f"Failed to generate betting lines: {str(e)}")
            raise

    def _calculate_moneyline_odds(self, spread: float) -> int:
        """Calculate realistic moneyline odds based on spread"""
        try:
            if spread > 0:
                return int(100 + (spread * 20))
            return int(-120 + (spread * 20))
        except Exception as e:
            logger.error(f"Failed to calculate moneyline odds: {str(e)}")
            raise

    def _format_injuries(self, injuries: List[InjuryReport]) -> str:
        """Format injury report into readable string"""
        try:
            if not injuries:
                return "No injuries to report"
                
            injury_lines = []
            for injury in injuries:
                injury_lines.append(
                    f"- {injury.player} ({injury.position}): {injury.injury} - {injury.status}"
                )
            return "\n".join(injury_lines)
        except Exception as e:
            logger.error(f"Failed to format injuries: {str(e)}")
            raise

    def _generate_weather_impact(self, weather: Dict) -> str:
        """Generate weather impact analysis"""
        try:
            if weather["condition"] in ["Snow", "Rain"]:
                return "heavy impact on game strategy"
            elif weather["wind_speed"] > 20:
                return "significant wind factor"
            elif weather["temperature"] < 32:
                return "cold weather impact"
            elif weather["temperature"] > 85:
                return "heat factor consideration"
            return "minimal weather impact"
        except Exception as e:
            logger.error(f"Failed to generate weather impact: {str(e)}")
            raise

    def _generate_injury_impact(self, injuries: Dict[str, List[InjuryReport]], impact_num: int) -> str:
        """Generate injury impact analysis"""
        try:
            impacts = {
                1: "Key position depth affected",
                2: "Roster adjustments necessary",
                3: "Game plan modifications required"
            }
            return impacts.get(impact_num, "No significant impact")
        except Exception as e:
            logger.error(f"Failed to generate injury impact: {str(e)}")
            raise

    def _generate_weather_injury_final_analysis(self, weather: Dict, injuries: Dict[str, List[InjuryReport]]) -> str:
        """Generate combined weather and injury analysis"""
        try:
            impacts = []
            
            # Weather analysis
            if weather["condition"] in ["Snow", "Rain"]:
                impacts.append("Weather conditions will significantly affect gameplay")
            elif weather["wind_speed"] > 20:
                impacts.append("Strong winds will impact kicking and passing games")
                
            # Injury analysis
            total_injuries = len(injuries["home"]) + len(injuries["away"])
            if total_injuries > 8:
                impacts.append("High injury count could be decisive factor")
            elif total_injuries > 4:
                impacts.append("Multiple injuries may affect team depth")
                
            if not impacts:
                return "No major weather or injury concerns"
            return ". ".join(impacts)
        except Exception as e:
            logger.error(f"Failed to generate weather/injury analysis: {str(e)}")
            raise

    def _generate_pass_rush_analysis(self, def_stats: Dict) -> str:
        """Generate analysis of pass rush effectiveness"""
        try:
            home_pressure = def_stats["home"]["sacks"] * 2 + def_stats["home"]["tackles"]
            away_pressure = def_stats["away"]["sacks"] * 2 + def_stats["away"]["tackles"]
            
            if home_pressure > away_pressure:
                return f"Home team showing superior pass rush capability with {home_pressure} pressure points"
            return f"Away team demonstrating better pass rush with {away_pressure} pressure points"
            
        except Exception as e:
            logger.error(f"Failed to generate pass rush analysis: {str(e)}")
            raise

    def _generate_pressure_impact_analysis(self, def_stats: Dict) -> str:
        """Generate analysis of pressure impact on quarterbacks"""
        try:
            home_impact = def_stats["home"]["sacks"] + def_stats["home"]["passes_defended"]
            away_impact = def_stats["away"]["sacks"] + def_stats["away"]["passes_defended"]
            
            if home_impact > away_impact:
                return "Home defense creating more disruptive pressure"
            return "Away defense generating more impactful pressure"
            
        except Exception as e:
            logger.error(f"Failed to generate pressure impact analysis: {str(e)}")
            raise

    def _generate_tackling_analysis(self, def_stats: Dict) -> str:
        """Generate analysis of tackling efficiency"""
        try:
            home_efficiency = def_stats["home"]["tackles"] / max(1, def_stats["home"]["fumbles_forced"])
            away_efficiency = def_stats["away"]["tackles"] / max(1, def_stats["away"]["fumbles_forced"])
            
            if home_efficiency > away_efficiency:
                return "Home team displaying better tackling fundamentals"
            return "Away team showing more reliable tackling"
            
        except Exception as e:
            logger.error(f"Failed to generate tackling analysis: {str(e)}")
            raise

    def _generate_impact_projection(self, def_stats: Dict) -> str:
        """Project defensive impact on the game"""
        try:
            home_impact = sum([
                def_stats["home"]["sacks"] * 2,
                def_stats["home"]["interceptions"] * 3,
                def_stats["home"]["fumbles_forced"],
                def_stats["home"]["passes_defended"]
            ])
            
            away_impact = sum([
                def_stats["away"]["sacks"] * 2,
                def_stats["away"]["interceptions"] * 3,
                def_stats["away"]["fumbles_forced"],
                def_stats["away"]["passes_defended"]
            ])
            
            if home_impact > away_impact:
                return f"Home defense projected to be more disruptive (Impact Score: {home_impact})"
            return f"Away defense likely to create more problems (Impact Score: {away_impact})"
            
        except Exception as e:
            logger.error(f"Failed to generate impact projection: {str(e)}")
            raise

    def _generate_penalty_analysis(self, team_stats: Dict) -> str:
        """Generate analysis of penalty trends"""
        try:
            home_penalty_impact = team_stats["home"]["penalties_per_game"] * team_stats["home"]["penalty_yards_per_game"]
            away_penalty_impact = team_stats["away"]["penalties_per_game"] * team_stats["away"]["penalty_yards_per_game"]
            
            if home_penalty_impact < away_penalty_impact:
                return "Home team showing better discipline in penalties"
            return "Away team demonstrating better penalty management"
            
        except Exception as e:
            logger.error(f"Failed to generate penalty analysis: {str(e)}")
            raise

    def _generate_rushing_tendency_analysis(self, team_stats: Dict) -> str:
        """Analyze rushing play tendencies"""
        try:
            home_tendency = team_stats["home"]["time_of_possession"].split(":")[0]
            away_tendency = team_stats["away"]["time_of_possession"].split(":")[0]
            
            if int(home_tendency) > int(away_tendency):
                return "Home team likely to emphasize ground game"
            return "Away team showing preference for rushing attack"
            
        except Exception as e:
            logger.error(f"Failed to generate rushing tendency analysis: {str(e)}")
            raise     

    def _generate_third_down_analysis(self, team_stats: Dict) -> str:
        """Analyze third down conversion efficiency"""
        try:
            if team_stats["home"]["third_down_conversion"] > team_stats["away"]["third_down_conversion"]:
                return f"Home team more efficient on third downs ({team_stats['home']['third_down_conversion']:.1f}%)"
            return f"Away team showing better third down success ({team_stats['away']['third_down_conversion']:.1f}%)"
            
        except Exception as e:
            logger.error(f"Failed to generate third down analysis: {str(e)}")
            raise

    def _generate_red_zone_analysis(self, team_stats: Dict) -> str:
        """Analyze red zone scoring efficiency"""
        try:
            if team_stats["home"]["red_zone_scoring"] > team_stats["away"]["red_zone_scoring"]:
                return f"Home team superior in red zone ({team_stats['home']['red_zone_scoring']:.1f}%)"
            return f"Away team more effective in red zone ({team_stats['away']['red_zone_scoring']:.1f}%)"
            
        except Exception as e:
            logger.error(f"Failed to generate red zone analysis: {str(e)}")
            raise

    def _generate_protection_analysis(self, team_stats: Dict) -> str:
        """Analyze pass protection schemes"""
        try:
            home_protection = team_stats["home"]["sacks_allowed"] + team_stats["home"]["qb_hits_allowed"]
            away_protection = team_stats["away"]["sacks_allowed"] + team_stats["away"]["qb_hits_allowed"]
            
            if home_protection < away_protection:
                return "Home team providing better QB protection"
            return "Away team showing stronger pass protection"
            
        except Exception as e:
            logger.error(f"Failed to generate protection analysis: {str(e)}")
            raise

    def _generate_scramble_analysis(self, team_stats: Dict) -> str:
        """Analyze quarterback scramble effectiveness"""
        try:
            home_mobility = team_stats["home"]["sacks_allowed"] / max(1, team_stats["home"]["qb_hits_allowed"])
            away_mobility = team_stats["away"]["sacks_allowed"] / max(1, team_stats["away"]["qb_hits_allowed"])
            
            if home_mobility < away_mobility:
                return "Home QB showing better scramble ability"
            return "Away QB demonstrating superior mobility"
            
        except Exception as e:
            logger.error(f"Failed to generate scramble analysis: {str(e)}")
            raise

    def _generate_pressure_management_analysis(self, team_stats: Dict) -> str:
        """Analyze pressure management effectiveness"""
        try:
            home_management = team_stats["home"]["qb_hits_allowed"] / max(1, team_stats["home"]["sacks_allowed"])
            away_management = team_stats["away"]["qb_hits_allowed"] / max(1, team_stats["away"]["sacks_allowed"])
            
            if home_management > away_management:
                return "Home team better at managing defensive pressure"
            return "Away team showing superior pressure handling"
            
        except Exception as e:
            logger.error(f"Failed to generate pressure management analysis: {str(e)}")
            raise

    def _generate_protection_impact_assessment(self, team_stats: Dict) -> str:
        """Assess overall protection impact on the game"""
        try:
            home_impact = (team_stats["home"]["sacks_allowed"] * 2 + 
                         team_stats["home"]["qb_hits_allowed"]) / max(1, team_stats["home"]["turnover_differential"])
            away_impact = (team_stats["away"]["sacks_allowed"] * 2 + 
                         team_stats["away"]["qb_hits_allowed"]) / max(1, team_stats["away"]["turnover_differential"])
            
            if home_impact < away_impact:
                return "Protection advantage favors home team"
            return "Protection metrics favor away team"
            
        except Exception as e:
            logger.error(f"Failed to generate protection impact assessment: {str(e)}")
            raise

    def _generate_passing_trend_analysis(self, recent_stats: Dict) -> str:
        """Analyze passing game trends"""
        try:
            home_trend = (recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["yards"]))
            away_trend = (recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["yards"]))
            
            if home_trend > away_trend:
                return "Home passing attack trending upward"
            return "Away passing game showing improvement"
            
        except Exception as e:
            logger.error(f"Failed to generate passing trend analysis: {str(e)}")
            raise

    def _generate_rushing_trend_analysis(self, recent_stats: Dict) -> str:
        """Analyze rushing game trends"""
        try:
            home_trend = (recent_stats["home"]["last_2_weeks"]["offense"]["rushing"]["yards"] / 
                         max(1, recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["yards"]))
            away_trend = (recent_stats["away"]["last_2_weeks"]["offense"]["rushing"]["yards"] / 
                         max(1, recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["yards"]))
            
            if home_trend > away_trend:
                return "Home ground game showing recent improvement"
            return "Away rushing attack trending positively"
            
        except Exception as e:
            logger.error(f"Failed to generate rushing trend analysis: {str(e)}")
            raise

    def _generate_receiving_trend_analysis(self, recent_stats: Dict) -> str:
        """Analyze receiving trends"""
        try:
            home_trend = (recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["touchdowns"]))
            away_trend = (recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["touchdowns"]))
            
            if home_trend > away_trend:
                return "Home receiving corps more efficient recently"
            return "Away receivers showing better production"
            
        except Exception as e:
            logger.error(f"Failed to generate receiving trend analysis: {str(e)}")
            raise

    def _generate_punting_trend_analysis(self, recent_stats: Dict) -> str:
        """Analyze punting game trends"""
        try:
            home_trend = (recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                         max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["punts"]))
            away_trend = (recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                         max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["punts"]))
            
            if home_trend > away_trend:
                return "Home punting unit performing better lately"
            return "Away team showing stronger punt game"
            
        except Exception as e:
            logger.error(f"Failed to generate punting trend analysis: {str(e)}")
            raise

    def _generate_kicking_trend_analysis(self, recent_stats: Dict) -> str:
        """Analyze kicking game trends"""
        try:
            home_trend = recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"]
            away_trend = recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"]
            
            if home_trend > away_trend:
                return "Home kicker showing better recent form"
            return "Away kicking game more reliable recently"
            
        except Exception as e:
            logger.error(f"Failed to generate kicking trend analysis: {str(e)}")
            raise

    def _generate_field_position_trends(self, recent_stats: Dict) -> str:
        """Analyze field position trends"""
        try:
            home_trend = (recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                         max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["inside_twenty"]))
            away_trend = (recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                         max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["inside_twenty"]))
            
            if home_trend < away_trend:
                return "Home team winning field position battle"
            return "Away team showing field position advantage"
            
        except Exception as e:
            logger.error(f"Failed to generate field position trends analysis: {str(e)}")
            raise

    def _generate_punting_analysis(self, special_teams: Dict) -> str:
        """Generate punting game analysis"""
        try:
            home_efficiency = special_teams["home"]["punting"]["yards"] / max(1, special_teams["home"]["punting"]["punts"])
            away_efficiency = special_teams["away"]["punting"]["yards"] / max(1, special_teams["away"]["punting"]["punts"])
            
            if home_efficiency > away_efficiency:
                return f"Home team averaging better punt distance ({home_efficiency:.1f} yards)"
            return f"Away team showing superior punt distance ({away_efficiency:.1f} yards)"
            
        except Exception as e:
            logger.error(f"Failed to generate punting analysis: {str(e)}")
            raise

    def _generate_kicking_analysis(self, special_teams: Dict) -> str:
        """Generate kicking game analysis"""
        try:
            home_accuracy = (special_teams["home"]["kicking"]["field_goals_made"] / 
                           max(1, special_teams["home"]["kicking"]["field_goals_attempted"]))
            away_accuracy = (special_teams["away"]["kicking"]["field_goals_made"] / 
                           max(1, special_teams["away"]["kicking"]["field_goals_attempted"]))
            
            if home_accuracy > away_accuracy:
                return f"Home kicker more accurate ({home_accuracy:.1%} success rate)"
            return f"Away kicker showing better accuracy ({away_accuracy:.1%} success rate)"
            
        except Exception as e:
            logger.error(f"Failed to generate kicking analysis: {str(e)}")
            raise

    def _generate_return_analysis(self, special_teams: Dict) -> str:
        """Generate return game analysis"""
        try:
            home_effectiveness = (special_teams["home"]["returns"]["kick_return_yards"] + 
                                special_teams["home"]["returns"]["punt_return_yards"]) / \
                               max(1, (special_teams["home"]["returns"]["kick_returns"] + 
                                     special_teams["home"]["returns"]["punt_returns"]))
            
            away_effectiveness = (special_teams["away"]["returns"]["kick_return_yards"] + 
                                special_teams["away"]["returns"]["punt_return_yards"]) / \
                               max(1, (special_teams["away"]["returns"]["kick_returns"] + 
                                     special_teams["away"]["returns"]["punt_returns"]))
            
            if home_effectiveness > away_effectiveness:
                return f"Home return game more explosive ({home_effectiveness:.1f} yards per return)"
            return f"Away return unit more effective ({away_effectiveness:.1f} yards per return)"
            
        except Exception as e:
            logger.error(f"Failed to generate return analysis: {str(e)}")
            raise

    def _generate_special_teams_analysis(self, special_teams: Dict) -> str:
        """Generate overall special teams analysis"""
        try:
            home_rating = (
                special_teams["home"]["kicking"]["field_goals_made"] * 3 +
                special_teams["home"]["returns"]["return_touchdowns"] * 7 +
                special_teams["home"]["punting"]["inside_twenty"] * 2
            )
            
            away_rating = (
                special_teams["away"]["kicking"]["field_goals_made"] * 3 +
                special_teams["away"]["returns"]["return_touchdowns"] * 7 +
                special_teams["away"]["punting"]["inside_twenty"] * 2
            )
            
            if home_rating > away_rating:
                return f"Home special teams unit rated higher (Rating: {home_rating})"
            return f"Away special teams showing advantage (Rating: {away_rating})"
            
        except Exception as e:
            logger.error(f"Failed to generate special teams analysis: {str(e)}")
            raise

    def _generate_field_position_analysis(self, special_teams: Dict) -> str:
        """Generate field position analysis"""
        try:
            home_field_pos = (
                special_teams["home"]["punting"]["yards"] / max(1, special_teams["home"]["punting"]["punts"]) +
                special_teams["home"]["returns"]["kick_return_yards"] / max(1, special_teams["home"]["returns"]["kick_returns"])
            )
            
            away_field_pos = (
                special_teams["away"]["punting"]["yards"] / max(1, special_teams["away"]["punting"]["punts"]) +
                special_teams["away"]["returns"]["kick_return_yards"] / max(1, special_teams["away"]["returns"]["kick_returns"])
            )
            
            if home_field_pos > away_field_pos:
                return "Home team likely to win field position battle"
            return "Away team shows field position advantage"
            
        except Exception as e:
            logger.error(f"Failed to generate field position analysis: {str(e)}")
            raise

    def _generate_impact_analysis(self, special_teams: Dict) -> str:
        """Generate game impact analysis for special teams"""
        try:
            home_impact = (
                special_teams["home"]["kicking"]["field_goals_made"] * 3 +
                special_teams["home"]["returns"]["return_touchdowns"] * 7 +
                special_teams["home"]["punting"]["inside_twenty"] * 2 -
                special_teams["home"]["returns"]["kick_returns"]  # Negative impact of having to return
            )
            
            away_impact = (
                special_teams["away"]["kicking"]["field_goals_made"] * 3 +
                special_teams["away"]["returns"]["return_touchdowns"] * 7 +
                special_teams["away"]["punting"]["inside_twenty"] * 2 -
                special_teams["away"]["returns"]["kick_returns"]
            )
            
            if home_impact > away_impact:
                return "Home special teams projected to have greater game impact"
            return "Away special teams likely to be more influential"
            
        except Exception as e:
            logger.error(f"Failed to generate impact analysis: {str(e)}")
            raise 

    def _generate_defensive_analysis(self, def_stats: Dict) -> str:
        """Generate defensive performance analysis"""
        try:
            home_effectiveness = (
                def_stats["home"]["sacks"] * 2 +
                def_stats["home"]["interceptions"] * 3 +
                def_stats["home"]["fumbles_forced"] +
                def_stats["home"]["passes_defended"]
            )
            
            away_effectiveness = (
                def_stats["away"]["sacks"] * 2 +
                def_stats["away"]["interceptions"] * 3 +
                def_stats["away"]["fumbles_forced"] +
                def_stats["away"]["passes_defended"]
            )
            
            if home_effectiveness > away_effectiveness:
                return f"Home defense rated more effective (Rating: {home_effectiveness})"
            return f"Away defense showing higher effectiveness (Rating: {away_effectiveness})"
            
        except Exception as e:
            logger.error(f"Failed to generate defensive analysis: {str(e)}")
            raise

    def _generate_pass_defense_analysis(self, def_stats: Dict) -> str:
        """Generate pass defense analysis"""
        try:
            home_pass_def = def_stats["home"]["passes_defended"] + (def_stats["home"]["interceptions"] * 2)
            away_pass_def = def_stats["away"]["passes_defended"] + (def_stats["away"]["interceptions"] * 2)
            
            if home_pass_def > away_pass_def:
                return "Home secondary showing better coverage"
            return "Away pass defense performing better"
            
        except Exception as e:
            logger.error(f"Failed to generate pass defense analysis: {str(e)}")
            raise
    
    def _generate_defensive_efficiency_analysis(self, def_stats: Dict) -> str:
        """Generate analysis of defensive efficiency"""
        try:
            home_efficiency = (
                def_stats["home"]["interceptions"] * 3 +
                def_stats["home"]["fumbles_forced"] * 2 +
                def_stats["home"]["passes_defended"] +
                def_stats["home"]["sacks"]
            ) / max(1, def_stats["home"]["tackles"])

            away_efficiency = (
                def_stats["away"]["interceptions"] * 3 +
                def_stats["away"]["fumbles_forced"] * 2 +
                def_stats["away"]["passes_defended"] +
                def_stats["away"]["sacks"]
            ) / max(1, def_stats["away"]["tackles"])

            if home_efficiency > away_efficiency:
                return f"Home defense showing higher efficiency (Rating: {home_efficiency:.2f})"
            return f"Away defense demonstrating better efficiency (Rating: {away_efficiency:.2f})"

        except Exception as e:
            logger.error(f"Failed to generate defensive efficiency analysis: {str(e)}")
            raise

    def _generate_run_defense_analysis(self, def_stats: Dict) -> str:
        """Generate run defense analysis"""
        try:
            home_run_def = def_stats["home"]["tackles"] + (def_stats["home"]["fumbles_forced"] * 2)
            away_run_def = def_stats["away"]["tackles"] + (def_stats["away"]["fumbles_forced"] * 2)
            
            if home_run_def > away_run_def:
                return "Home run defense more stout"
            return "Away team better against the run"
            
        except Exception as e:
            logger.error(f"Failed to generate run defense analysis: {str(e)}")
            raise

    def _generate_turnover_analysis(self, def_stats: Dict) -> str:
        """Generate turnover creation analysis"""
        try:
            home_turnovers = def_stats["home"]["interceptions"] + def_stats["home"]["fumbles_recovered"]
            away_turnovers = def_stats["away"]["interceptions"] + def_stats["away"]["fumbles_recovered"]
            
            if home_turnovers > away_turnovers:
                return f"Home defense generating more turnovers ({home_turnovers} total)"
            return f"Away defense more opportunistic ({away_turnovers} total)"
            
        except Exception as e:
            logger.error(f"Failed to generate turnover analysis: {str(e)}")
            raise

    def _generate_return_trend_analysis(self, recent_stats: Dict) -> str:
        """Analyze return game trends"""
        try:
            home_recent = recent_stats["home"]["last_2_weeks"]["special_teams"]["returns"]["return_touchdowns"]
            home_month = recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["return_touchdowns"]
            away_recent = recent_stats["away"]["last_2_weeks"]["special_teams"]["returns"]["return_touchdowns"]
            away_month = recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["return_touchdowns"]
            
            home_trend = home_recent / max(1, home_month)
            away_trend = away_recent / max(1, away_month)
            
            if home_trend > away_trend:
                return "Home return game trending up"
            return "Away return unit showing improvement"
            
        except Exception as e:
            logger.error(f"Failed to generate return trend analysis: {str(e)}")
            raise    

    def _generate_special_teams_trend_analysis(self, recent_stats: Dict) -> str:
        """Generate special teams trend analysis"""
        try:
            home_recent = (recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] + 
                         recent_stats["home"]["last_2_weeks"]["special_teams"]["returns"]["return_touchdowns"] * 7)
            home_month = (recent_stats["home"]["last_4_weeks"]["special_teams"]["kicking"]["field_goals_made"] + 
                        recent_stats["home"]["last_4_weeks"]["special_teams"]["returns"]["return_touchdowns"] * 7)
            
            away_recent = (recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] + 
                         recent_stats["away"]["last_2_weeks"]["special_teams"]["returns"]["return_touchdowns"] * 7)
            away_month = (recent_stats["away"]["last_4_weeks"]["special_teams"]["kicking"]["field_goals_made"] + 
                        recent_stats["away"]["last_4_weeks"]["special_teams"]["returns"]["return_touchdowns"] * 7)
            
            home_trend = home_recent / max(1, home_month)
            away_trend = away_recent / max(1, away_month)
            
            if home_trend > away_trend:
                return "Home special teams performance improving"
            return "Away special teams trending positively"
            
        except Exception as e:
            logger.error(f"Failed to generate special teams trend analysis: {str(e)}")
            raise

    def _generate_impact_player_analysis(self, recent_stats: Dict) -> str:
        """Analyze impact player performances"""
        try:
            home_impact = (recent_stats["home"]["last_2_weeks"]["special_teams"]["returns"]["return_touchdowns"] * 7 + 
                         recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] * 3)
            away_impact = (recent_stats["away"]["last_2_weeks"]["special_teams"]["returns"]["return_touchdowns"] * 7 + 
                         recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] * 3)
            
            if home_impact > away_impact:
                return "Home team showing more game-changing plays"
            return "Away team generating more impact plays"
            
        except Exception as e:
            logger.error(f"Failed to generate impact player analysis: {str(e)}")
            raise

    def _generate_defensive_split_analysis(self, recent_stats: Dict) -> str:
        """Generate defensive split analysis"""
        try:
            home_split = (recent_stats["home"]["last_2_weeks"]["defense"]["interceptions"] + 
                        recent_stats["home"]["last_2_weeks"]["defense"]["fumbles_forced"])
            away_split = (recent_stats["away"]["last_2_weeks"]["defense"]["interceptions"] + 
                        recent_stats["away"]["last_2_weeks"]["defense"]["fumbles_forced"])
            
            if home_split > away_split:
                return f"Home defense creating more turnovers recently ({home_split})"
            return f"Away defense generating more takeaways ({away_split})"
            
        except Exception as e:
            logger.error(f"Failed to generate defensive split analysis: {str(e)}")
            raise

    def _generate_punting_split_analysis(self, recent_stats: Dict) -> str:
        """Generate punting split analysis"""
        try:
            home_efficiency = (recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                             max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["punts"]))
            away_efficiency = (recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                             max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["punts"]))
            
            if home_efficiency > away_efficiency:
                return f"Home punting more effective ({home_efficiency:.1f} yards/punt)"
            return f"Away punt game showing better results ({away_efficiency:.1f} yards/punt)"
            
        except Exception as e:
            logger.error(f"Failed to generate punting split analysis: {str(e)}")
            raise

    def _generate_kicking_split_analysis(self, recent_stats: Dict) -> str:
        """Generate kicking split analysis"""
        try:
            home_accuracy = (recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] / 
                           max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_attempted"]))
            away_accuracy = (recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] / 
                           max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_attempted"]))
            
            if home_accuracy > away_accuracy:
                return f"Home kicker more reliable ({home_accuracy:.1%})"
            return f"Away kicking game more consistent ({away_accuracy:.1%})"
            
        except Exception as e:
            logger.error(f"Failed to generate kicking split analysis: {str(e)}")
            raise 

    def _generate_stadium_impact_analysis(self, game_data: Dict) -> str:
        """Generate analysis of stadium impact on game"""
        try:
            stadium = game_data["venue"]
            weather = game_data["weather"]
            
            # Check for domed stadiums
            domed_stadiums = [
                "SoFi Stadium", "U.S. Bank Stadium", "Ford Field", 
                "Lucas Oil Stadium", "Caesars Superdome", "Allegiant Stadium"
            ]
            
            if stadium in domed_stadiums:
                return "Indoor stadium neutralizes weather factors"
            
            # Analyze outdoor stadium impacts
            if weather["temperature"] < 32:
                return "Cold weather outdoor stadium favors running game"
            elif weather["temperature"] > 85:
                return "Heat factor significant in outdoor venue"
            elif weather["wind_speed"] > 15:
                return "Open stadium with significant wind impact"
            
            return "Standard outdoor playing conditions"
            
        except Exception as e:
            logger.error(f"Failed to generate stadium impact analysis: {str(e)}")
            raise

    def _generate_environment_impact_analysis(self, game_data: Dict) -> str:
        """Generate analysis of environmental factors"""
        try:
            weather = game_data["weather"]
            time = game_data.get("game_time", "")  # Get game time if available
            
            impacts = []
            
            # Weather impacts
            if weather["condition"] in ["Snow", "Rain"]:
                impacts.append("Precipitation will affect ball security")
            if weather["wind_speed"] > 20:
                impacts.append("High winds impact kicking/passing")
            
            # Time of day impacts (if available)
            if "PM" in time and int(time.split(":")[0]) > 4:
                impacts.append("Late game lighting conditions")
            
            if not impacts:
                return "No significant environmental factors"
            return ". ".join(impacts)
            
        except Exception as e:
            logger.error(f"Failed to generate environment impact analysis: {str(e)}")
            raise
    
    def _get_prompt_name(self, prompt_number: int) -> str:
        """Get the prompt name suffix based on prompt number"""
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
        return prompt_names.get(prompt_number, "unknown")

    def _generate_passing_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of passing game home/away splits"""
        try:
            home_split = (recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["yards"]))
            away_split = (recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["yards"]))
            
            if home_split > away_split:
                return "Home passing attack more effective in venue"
            return "Away team shows better passing splits"
            
        except Exception as e:
            logger.error(f"Failed to generate passing split analysis: {str(e)}")
            raise

    def _generate_rushing_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of rushing game home/away splits"""
        try:
            home_split = (recent_stats["home"]["last_2_weeks"]["offense"]["rushing"]["yards"] / 
                         max(1, recent_stats["home"]["last_4_weeks"]["offense"]["rushing"]["yards"]))
            away_split = (recent_stats["away"]["last_2_weeks"]["offense"]["rushing"]["yards"] / 
                         max(1, recent_stats["away"]["last_4_weeks"]["offense"]["rushing"]["yards"]))
            
            if home_split > away_split:
                return "Home ground game stronger at home"
            return "Away rushing attack travels well"
            
        except Exception as e:
            logger.error(f"Failed to generate rushing split analysis: {str(e)}")
            raise

    def _generate_receiving_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of receiving game home/away splits"""
        try:
            home_split = (recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["home"]["last_4_weeks"]["offense"]["passing"]["touchdowns"]))
            away_split = (recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"] / 
                         max(1, recent_stats["away"]["last_4_weeks"]["offense"]["passing"]["touchdowns"]))
            
            if home_split > away_split:
                return "Home receivers more productive in familiar venue"
            return "Away passing game shows good road performance"
            
        except Exception as e:
            logger.error(f"Failed to generate receiving split analysis: {str(e)}")
            raise

    def _generate_overall_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of overall home/away tendencies"""
        try:
            # Calculate composite scores for recent performance
            home_composite = sum([
                recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["yards"],
                recent_stats["home"]["last_2_weeks"]["offense"]["rushing"]["yards"] * 1.5,
                recent_stats["home"]["last_2_weeks"]["offense"]["passing"]["touchdowns"] * 7
            ])
            
            away_composite = sum([
                recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["yards"],
                recent_stats["away"]["last_2_weeks"]["offense"]["rushing"]["yards"] * 1.5,
                recent_stats["away"]["last_2_weeks"]["offense"]["passing"]["touchdowns"] * 7
            ])
            
            if home_composite > away_composite:
                return f"Home team showing stronger overall splits (Rating: {home_composite:.0f})"
            return f"Away team demonstrates better road performance (Rating: {away_composite:.0f})"
            
        except Exception as e:
            logger.error(f"Failed to generate overall split analysis: {str(e)}")
            raise

    def _generate_return_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of return game home/away splits"""
        try:
            home_split = (recent_stats["home"]["last_2_weeks"]["special_teams"]["returns"]["kick_return_yards"] / 
                         max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["returns"]["kick_returns"]))
            away_split = (recent_stats["away"]["last_2_weeks"]["special_teams"]["returns"]["kick_return_yards"] / 
                         max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["returns"]["kick_returns"]))
            
            if home_split > away_split:
                return f"Home return game excels in venue ({home_split:.1f} yards/return)"
            return f"Away returners show road prowess ({away_split:.1f} yards/return)"
            
        except Exception as e:
            logger.error(f"Failed to generate return split analysis: {str(e)}")
            raise

    def _generate_special_teams_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of special teams home/away splits"""
        try:
            home_kicking = (recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] / 
                          max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_attempted"]))
            away_kicking = (recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_made"] / 
                          max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["kicking"]["field_goals_attempted"]))
            
            if home_kicking > away_kicking:
                return f"Home special teams unit more reliable ({home_kicking:.1%})"
            return f"Away special teams shows road consistency ({away_kicking:.1%})"
            
        except Exception as e:
            logger.error(f"Failed to generate special teams split analysis: {str(e)}")
            raise

    def _generate_field_position_split_analysis(self, recent_stats: Dict) -> str:
        """Generate analysis of field position home/away splits"""
        try:
            home_field_pos = (recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                            max(1, recent_stats["home"]["last_2_weeks"]["special_teams"]["punting"]["inside_twenty"]))
            away_field_pos = (recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["yards"] / 
                            max(1, recent_stats["away"]["last_2_weeks"]["special_teams"]["punting"]["inside_twenty"]))
            
            if home_field_pos < away_field_pos:  # Lower is better for field position
                return "Home team shows better field position management"
            return "Away team maintains field position advantage"
            
        except Exception as e:
            logger.error(f"Failed to generate field position split analysis: {str(e)}")
            raise   
        
    def _generate_complete_analysis(self, game_data: Dict) -> List[Dict]:
            """Generate complete set of training examples for all 16 prompts"""
            logger.debug("Generating complete analysis")
            training_examples = []
            
            try:
                # Generate example for each prompt
                for i in range(1, 17):
                    prompt_template = self.prompt_templates[f"prompt{i}_{self._get_prompt_name(i)}"]
                    instruction = self._generate_prompt_instruction(i, game_data)
                    formatted_response = self._format_prompt_response(i, game_data, prompt_template)
                    
                    training_examples.append({
                        "instruction": instruction,
                        "input": "",
                        "output": formatted_response
                    })
                
                return training_examples
                
            except Exception as e:
                logger.error(f"Failed to generate complete analysis: {str(e)}")
                raise
    
    def _generate_prompt_instruction(self, prompt_number: int, game_data: Dict) -> str:
        """Generate instruction for each prompt"""
        try:
            return f"Analyze {game_data['away_team']} @ {game_data['home_team']} - Prompt {prompt_number}"
        except Exception as e:
            logger.error(f"Failed to generate prompt instruction: {str(e)}")
            raise

    def _calculate_win_probability(self, spread: float) -> float:
        """Calculate win probability based on spread"""
        try:
            # Simple probability calculation based on spread
            base_prob = 50.0
            spread_factor = -spread * 2  # Each point worth roughly 2% probability
            win_prob = min(max(base_prob + spread_factor, 5), 95)  # Cap between 5% and 95%
            return round(win_prob, 1)
        except Exception as e:
            logger.error(f"Failed to calculate win probability: {str(e)}")
            raise

    def _calculate_spread_probability(self, spread: float) -> float:
        """Calculate spread cover probability"""
        try:
            return round(55 + (-spread * 1.5), 1)  # Slight adjustment from straight win probability
        except Exception as e:
            logger.error(f"Failed to calculate spread probability: {str(e)}")
            raise

    def _calculate_total_probability(self, total: float, bet_type: str) -> float:
        """Calculate over/under probability"""
        try:
            base_prob = 50.0
            if bet_type.lower() == "over":
                return round(base_prob + (random.random() * 10), 1)
            return round(base_prob + (random.random() * 10), 1)
        except Exception as e:
            logger.error(f"Failed to calculate total probability: {str(e)}")
            raise

    def _calculate_team_total_probability(self, team_total: float, bet_type: str) -> float:
        """Calculate team total over/under probability"""
        try:
            base_prob = 50.0
            if bet_type.lower() == "over":
                return round(base_prob + (random.random() * 10), 1)
            return round(base_prob + (random.random() * 10), 1)
        except Exception as e:
            logger.error(f"Failed to calculate team total probability: {str(e)}")
            raise

    def _generate_key_factor(self, game_data: Dict, factor_num: int) -> str:
        """Generate key betting factor"""
        try:
            factors = {
                1: f"Weather impact: {self._generate_weather_impact(game_data['weather'])}",
                2: "Injury situation could affect performance",
                3: "Recent form and momentum considerations"
            }
            return factors.get(factor_num, "Additional contextual factor")
        except Exception as e:
            logger.error(f"Failed to generate key factor: {str(e)}")
            raise

    def _identify_value_bets(self, game_data: Dict, betting_lines: Dict) -> str:
        """Identify potential value bets based on analysis"""
        try:
            return "Analysis suggests potential value in moneyline and total markets"
        except Exception as e:
            logger.error(f"Failed to identify value bets: {str(e)}")
            raise

    def _generate_risk_assessment(self, game_data: Dict) -> str:
        """Generate risk assessment for betting considerations"""
        try:
            return "Moderate risk level based on weather and injury factors"
        except Exception as e:
            logger.error(f"Failed to generate risk assessment: {str(e)}")
            raise

    def _generate_final_recommendations(self, game_data: Dict, betting_lines: Dict) -> str:
        """Generate final betting recommendations"""
        try:
            return "Consider small positions on identified value opportunities"
        except Exception as e:
            logger.error(f"Failed to generate final recommendations: {str(e)}")
            raise

    def _generate_momentum_analysis(self, recent_stats: Dict) -> str:
        """Generate momentum analysis based on recent performance"""
        try:
            return "Teams showing balanced momentum indicators"
        except Exception as e:
            logger.error(f"Failed to generate momentum analysis: {str(e)}")
            raise

    def _generate_special_teams_trends(self, special_teams: Dict) -> str:
        """Generate special teams trend analysis"""
        try:
            return "Special teams performance showing stability"
        except Exception as e:
            logger.error(f"Failed to generate special teams trends: {str(e)}")
            raise

    def _generate_passing_analysis(self, offensive_stats: Dict) -> str:
        """Generate passing game analysis"""
        try:
            return "Balanced passing attacks from both teams"
        except Exception as e:
            logger.error(f"Failed to generate passing analysis: {str(e)}")
            raise

    def _generate_rushing_analysis(self, offensive_stats: Dict) -> str:
        """Generate rushing game analysis"""
        try:
            return "Ground games showing effectiveness"
        except Exception as e:
            logger.error(f"Failed to generate rushing analysis: {str(e)}")
            raise

    def _generate_receiving_analysis(self, offensive_stats: Dict) -> str:
        """Generate receiving analysis"""
        try:
            return "Receiving corps demonstrating consistency"
        except Exception as e:
            logger.error(f"Failed to generate receiving analysis: {str(e)}")
            raise

    def _format_prompt_response(self, prompt_number: int, game_data: Dict, template: str) -> str:
        """Format response for each prompt using templates and data"""
        try:
            template_vars = self._get_template_variables(prompt_number, game_data)
            return template.format(**template_vars)
        except KeyError as e:
            logger.error(f"Missing template variable: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to format prompt response: {str(e)}")
            raise

    def _get_template_variables(self, prompt_number: int, game_data: Dict) -> Dict:
        """Get variables needed for template formatting based on prompt number"""
    
        base_vars = {
            "home_team": game_data["home_team"],
            "away_team": game_data["away_team"],
            "venue": game_data["venue"]
        }

        # Helper functions for nested variable formatting
        def get_offensive_stats(team_stats, team_type):
            prefix = f"{team_type}_"
            return {
                f"{prefix}pass_att": team_stats["passing"]["attempts"],
                f"{prefix}pass_yds": team_stats["passing"]["yards"],
                f"{prefix}pass_ya": round(team_stats["passing"]["yards"] / max(1, team_stats["passing"]["attempts"]), 1),
                f"{prefix}pass_lng": team_stats["passing"]["longest"],
                f"{prefix}pass_td": team_stats["passing"]["touchdowns"],
                f"{prefix}rush_att": team_stats["rushing"]["attempts"],
                f"{prefix}rush_yds": team_stats["rushing"]["yards"],
                f"{prefix}rush_ya": team_stats["rushing"]["yards_per_attempt"],
                f"{prefix}rush_lng": team_stats["rushing"]["longest"],
                f"{prefix}rush_td": team_stats["rushing"]["touchdowns"],
                f"{prefix}rush_fum": team_stats["rushing"]["fumbles"],
                f"{prefix}rec": sum(team_stats["passing"]["yards"] for _ in range(3)), # Example calculation
                f"{prefix}rec_yds": team_stats["passing"]["yards"],
                f"{prefix}rec_yc": round(team_stats["passing"]["yards"] / max(1, team_stats["passing"]["attempts"]), 1),
                f"{prefix}rec_lng": team_stats["passing"]["longest"],
                f"{prefix}rec_td": team_stats["passing"]["touchdowns"],
                f"{prefix}rec_trg": team_stats["passing"]["attempts"]
            }

        def get_defensive_stats(team_stats, team_type):
            prefix = f"{team_type}_def_"
            return {
                f"{prefix}att": team_stats["tackles"],
                f"{prefix}yds": team_stats["passes_defended"],
                f"{prefix}ya": round(team_stats["passes_defended"] / max(1, team_stats["tackles"]), 1),
                f"{prefix}lng": max(30, random.randint(35, 50)),
                f"{prefix}td": random.randint(0, 2),
                f"{prefix}fum": team_stats["fumbles_forced"]
            }

        def get_special_teams_stats(team_stats, team_type):
            prefix = f"{team_type}_"
            return {
                f"{prefix}punt_att": team_stats["punting"]["punts"],
                f"{prefix}punt_yds": team_stats["punting"]["yards"],
                f"{prefix}punt_ya": round(team_stats["punting"]["yards"] / max(1, team_stats["punting"]["punts"]), 1),
                f"{prefix}punt_lng": team_stats["punting"]["longest"],
                f"{prefix}kick_att": team_stats["kicking"]["field_goals_attempted"],
                f"{prefix}kick_yds": team_stats["kicking"]["field_goals_made"] * 40,
                f"{prefix}kick_ya": round(40.0, 1),
                f"{prefix}kick_lng": team_stats["kicking"]["longest_field_goal"],
                f"{prefix}kick_td": 0,
                f"{prefix}ret_att": team_stats["returns"]["kick_returns"] + team_stats["returns"]["punt_returns"],
                f"{prefix}ret_yds": team_stats["returns"]["kick_return_yards"] + team_stats["returns"]["punt_return_yards"],
                f"{prefix}ret_ya": round((team_stats["returns"]["kick_return_yards"] + team_stats["returns"]["punt_return_yards"]) / 
                                    max(1, team_stats["returns"]["kick_returns"] + team_stats["returns"]["punt_returns"]), 1),
                f"{prefix}ret_lng": max(25, random.randint(30, 60)),
                f"{prefix}ret_td": team_stats["returns"]["return_touchdowns"],
                f"{prefix}ret_fum": random.randint(0, 1)
            }

        prompt_vars = {
            1: base_vars,
            
            2: {
                **base_vars,
                "game_time": datetime.now().strftime("%A, %B %d, %Y - 1:00 PM EST"),
                "weather_condition": game_data["weather"]["condition"],
                "temperature": game_data["weather"]["temperature"],
                "precip_chance": game_data["weather"]["precipitation_chance"],
                "wind_speed": game_data["weather"]["wind_speed"],
                "wind_direction": game_data["weather"]["wind_direction"],
                "away_injuries": self._format_injuries(game_data["injuries"]["away"]),
                "home_injuries": self._format_injuries(game_data["injuries"]["home"]),
                "weather_impact1": self._generate_weather_impact(game_data["weather"]),
                "weather_impact2": f"Wind factor ({game_data['weather']['wind_speed']} mph) impact",
                "weather_impact3": "Field conditions analysis",
                "injury_impact1": self._generate_injury_impact(game_data["injuries"], 1),
                "injury_impact2": self._generate_injury_impact(game_data["injuries"], 2),
                "injury_impact3": self._generate_injury_impact(game_data["injuries"], 3),
                "final_analysis": self._generate_weather_injury_final_analysis(game_data["weather"], game_data["injuries"])
            },
            
            3: {
                **base_vars,
                **get_offensive_stats(game_data["offensive_stats"]["away"], "away"),
                **get_offensive_stats(game_data["offensive_stats"]["home"], "home"),
                "passing_analysis": self._generate_passing_analysis(game_data["offensive_stats"]),
                "rushing_analysis": self._generate_rushing_analysis(game_data["offensive_stats"]),
                "receiving_analysis": self._generate_receiving_analysis(game_data["offensive_stats"]),
                "offensive_trends": "Combined offensive effectiveness analysis"
            },
            
            4: {
                **base_vars,
                **get_defensive_stats(game_data["defensive_stats"]["away"], "away"),
                **get_defensive_stats(game_data["defensive_stats"]["home"], "home"),
                **get_special_teams_stats(game_data["special_teams"]["away"], "away"),
                **get_special_teams_stats(game_data["special_teams"]["home"], "home"),
                "defensive_analysis": self._generate_defensive_analysis(game_data["defensive_stats"]),
                "punting_analysis": self._generate_punting_analysis(game_data["special_teams"]),
                "kicking_analysis": self._generate_kicking_analysis(game_data["special_teams"]),
                "special_teams_trends": self._generate_special_teams_trends(game_data["special_teams"])
            },

            5: {
                **base_vars,
                **get_special_teams_stats(game_data["special_teams"]["away"], "away"),
                **get_special_teams_stats(game_data["special_teams"]["home"], "home"),
                "return_analysis": self._generate_return_analysis(game_data["special_teams"]),
                "special_teams_analysis": self._generate_special_teams_analysis(game_data["special_teams"]),
                "field_position_analysis": self._generate_field_position_analysis(game_data["special_teams"]),
                "impact_analysis": self._generate_impact_analysis(game_data["special_teams"])
            },

            6: {
                **base_vars,
                **{k + "_road": v for k, v in get_offensive_stats(game_data["recent_performance"]["away"]["last_4_weeks"]["offense"], "away").items()},
                **{k + "_home": v for k, v in get_offensive_stats(game_data["recent_performance"]["home"]["last_4_weeks"]["offense"], "home").items()},
                "passing_split_analysis": self._generate_passing_split_analysis(game_data["recent_performance"]),
                "rushing_split_analysis": self._generate_rushing_split_analysis(game_data["recent_performance"]),
                "receiving_split_analysis": self._generate_receiving_split_analysis(game_data["recent_performance"]),
                "overall_split_analysis": self._generate_overall_split_analysis(game_data["recent_performance"])
            },

            7: {
                **base_vars,
                **{k + "_road": v for k, v in get_defensive_stats(game_data["recent_performance"]["away"]["last_4_weeks"]["defense"], "away").items()},
                **{k + "_home": v for k, v in get_defensive_stats(game_data["recent_performance"]["home"]["last_4_weeks"]["defense"], "home").items()},
                "defensive_split_analysis": self._generate_defensive_split_analysis(game_data["recent_performance"]),
                "punting_split_analysis": self._generate_punting_split_analysis(game_data["recent_performance"]),
                "kicking_split_analysis": self._generate_kicking_split_analysis(game_data["recent_performance"]),
                "stadium_impact_analysis": self._generate_stadium_impact_analysis(game_data)
            },

            8: {
                **base_vars,
                **{k + "_road": v for k, v in get_special_teams_stats(game_data["recent_performance"]["away"]["last_4_weeks"]["special_teams"], "away").items()},
                **{k + "_home": v for k, v in get_special_teams_stats(game_data["recent_performance"]["home"]["last_4_weeks"]["special_teams"], "home").items()},
                "return_split_analysis": self._generate_return_split_analysis(game_data["recent_performance"]),
                "special_teams_split_analysis": self._generate_special_teams_split_analysis(game_data["recent_performance"]),
                "field_position_split_analysis": self._generate_field_position_split_analysis(game_data["recent_performance"]),
                "environment_impact_analysis": self._generate_environment_impact_analysis(game_data)
            },

            9: {
                **base_vars,
                **{k + "_2wk": v for k, v in get_offensive_stats(game_data["recent_performance"]["away"]["last_2_weeks"]["offense"], "away").items()},
                **{k + "_4wk": v for k, v in get_offensive_stats(game_data["recent_performance"]["away"]["last_4_weeks"]["offense"], "away").items()},
                **{k + "_2wk": v for k, v in get_offensive_stats(game_data["recent_performance"]["home"]["last_2_weeks"]["offense"], "home").items()},
                **{k + "_4wk": v for k, v in get_offensive_stats(game_data["recent_performance"]["home"]["last_4_weeks"]["offense"], "home").items()},
                "passing_trend_analysis": self._generate_passing_trend_analysis(game_data["recent_performance"]),
                "rushing_trend_analysis": self._generate_rushing_trend_analysis(game_data["recent_performance"]),
                "receiving_trend_analysis": self._generate_receiving_trend_analysis(game_data["recent_performance"]),
                "momentum_analysis": self._generate_momentum_analysis(game_data["recent_performance"])
            },

            10: {
                **base_vars,
                **{k + "_2wk": v for k, v in get_special_teams_stats(game_data["recent_performance"]["away"]["last_2_weeks"]["special_teams"], "away").items()},
                **{k + "_2wk": v for k, v in get_special_teams_stats(game_data["recent_performance"]["home"]["last_2_weeks"]["special_teams"], "home").items()},
                "punting_trend_analysis": self._generate_punting_trend_analysis(game_data["recent_performance"]),
                "kicking_trend_analysis": self._generate_kicking_trend_analysis(game_data["recent_performance"]),
                "field_position_trends": self._generate_field_position_trends(game_data["recent_performance"]),
                "weather_impact_analysis": self._generate_environment_impact_analysis(game_data)
            },

            11: {
                **base_vars,
                "return_trend_analysis": self._generate_return_trend_analysis(game_data["recent_performance"]),
                "special_teams_trend_analysis": self._generate_special_teams_trend_analysis(game_data["recent_performance"]),
                "impact_player_analysis": self._generate_impact_player_analysis(game_data["recent_performance"]),
                "momentum_analysis": self._generate_momentum_analysis(game_data["recent_performance"])
            },

            12: {
                **base_vars,
                "defensive_efficiency_analysis": self._generate_defensive_efficiency_analysis(game_data["defensive_stats"]),
                "pass_defense_analysis": self._generate_pass_defense_analysis(game_data["defensive_stats"]),
                "run_defense_analysis": self._generate_run_defense_analysis(game_data["defensive_stats"]),
                "turnover_analysis": self._generate_turnover_analysis(game_data["defensive_stats"])
            },

            13: {
                **base_vars,
                "pass_rush_analysis": self._generate_pass_rush_analysis(game_data["defensive_stats"]),
                "pressure_impact_analysis": self._generate_pressure_impact_analysis(game_data["defensive_stats"]),
                "tackling_analysis": self._generate_tackling_analysis(game_data["defensive_stats"]),
                "impact_projection": self._generate_impact_projection(game_data["defensive_stats"])
            },

            14: {
                **base_vars,
                "penalty_analysis": self._generate_penalty_analysis(game_data["team_stats"]),
                "rushing_tendency_analysis": self._generate_rushing_tendency_analysis(game_data["team_stats"]),
                "third_down_analysis": self._generate_third_down_analysis(game_data["team_stats"]),
                "red_zone_analysis": self._generate_red_zone_analysis(game_data["team_stats"])
            },

            15: {
                **base_vars,
                "protection_analysis": self._generate_protection_analysis(game_data["team_stats"]),
                "scramble_analysis": self._generate_scramble_analysis(game_data["team_stats"]),
                "pressure_management_analysis": self._generate_pressure_management_analysis(game_data["team_stats"]),
                "impact_assessment": self._generate_protection_impact_assessment(game_data["team_stats"])
            },

            16: {
                **base_vars,
                "home_spread": f"{game_data['betting_lines']['spread']:+g}",
                "game_total": game_data["betting_lines"]["total"],
                "home_team_total": game_data["betting_lines"]["home_team_total"],
                "away_team_total": game_data["betting_lines"]["away_team_total"],
                "home_ml_prob": self._calculate_win_probability(game_data["betting_lines"]["spread"]),
                "away_ml_prob": 100 - self._calculate_win_probability(game_data["betting_lines"]["spread"]),
                "home_spread_prob": self._calculate_spread_probability(game_data["betting_lines"]["spread"]),
                "away_spread_prob": 100 - self._calculate_spread_probability(game_data["betting_lines"]["spread"]),
                "over_prob": self._calculate_total_probability(game_data["betting_lines"]["total"], "over"),
                "under_prob": self._calculate_total_probability(game_data["betting_lines"]["total"], "under"),
                "home_over_prob": self._calculate_team_total_probability(game_data["betting_lines"]["home_team_total"], "over"),
                "home_under_prob": self._calculate_team_total_probability(game_data["betting_lines"]["home_team_total"], "under"),
                "away_over_prob": self._calculate_team_total_probability(game_data["betting_lines"]["away_team_total"], "over"),
                "away_under_prob": self._calculate_team_total_probability(game_data["betting_lines"]["away_team_total"], "under"),
                "key_factor_1": self._generate_key_factor(game_data, 1),
                "key_factor_2": self._generate_key_factor(game_data, 2), 
                "key_factor_3": self._generate_key_factor(game_data, 3),
                "value_bets": self._identify_value_bets(game_data, game_data["betting_lines"]),
                "risk_assessment": self._generate_risk_assessment(game_data),
                "final_recommendations": self._generate_final_recommendations(game_data, game_data["betting_lines"])
                }
            }

        return prompt_vars.get(prompt_number, {})

def main():
   """Main execution function"""
   try:
       # Initialize generator
       generator = NFLTrainingDatasetGenerator()
       
       # Generate dataset (default 1000 examples)
       num_examples = 1000
       logger.info(f"Generating {num_examples} training examples...")
       dataset = generator.generate_dataset(num_examples)
       
       # Save dataset
       output_file = "nfl_training_data.jsonl"
       logger.info(f"Saving dataset to {output_file}...")
       generator.save_dataset(dataset, output_file)
       
       logger.info("Dataset generation complete!")
       print(f"Generated {len(dataset)} examples and saved to {output_file}")
       
   except Exception as e:
       logger.error(f"Dataset generation failed: {str(e)}")
       raise

if __name__ == "__main__":
   main()