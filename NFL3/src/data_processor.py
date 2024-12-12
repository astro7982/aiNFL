from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GameContext:
    """Store game-specific context"""
    game_id: str
    home_team: str
    away_team: str
    venue: str
    date: str
    weather: Optional[Dict] = None
    odds: Optional[Dict] = None

class NFLDataProcessor:
    """Process NFL data for analysis"""
    
    def process_depth_chart(self, data: List[Dict]) -> Dict:
        """Process depth chart data into structured format"""
        if not data:
            return {"offense": {}, "defense": {}, "special_teams": {}}
            
        processed = {
            "offense": {},
            "defense": {},
            "special_teams": {}
        }
        
        for player in data:
            try:
                section = player["Section"].lower().replace(" positions", "")
                if section not in processed:
                    continue
                    
                processed[section][player["Position"]] = {
                    "starter": player["Starter"],
                    "backup": player["2ND"],
                    "third_string": player.get("3RD", "-"),
                    "fourth_string": player.get("4TH", "-")
                }
            except KeyError as e:
                print(f"Warning: Missing key in depth chart data: {e}")
                continue
        
        return processed

    def process_player_stats(self, data: List[Dict], stat_type: str, timeframe: str) -> Dict:
        """Process player statistics for a specific timeframe"""
        processed = {}
        for player in data:
            try:
                # Filter stats for the specific timeframe and remove NaN values
                prefix = f"{stat_type} {timeframe} "
                stats = {
                    k.replace(prefix, ""): v
                    for k, v in player.items()
                    if k.startswith(prefix)
                    and isinstance(v, (int, float, str))
                    and str(v).lower() != 'nan'
                }
                
                if stats:  # Only include players with valid stats
                    processed[player["Name"]] = {
                        "position": player["Position"],
                        "stats": stats
                    }
            except KeyError:
                continue  # Skip players with missing required fields
                
        return processed

    def process_weather(self, data: List[Dict]) -> Dict:
        """Process weather data"""
        if not data:
            return {
                "temperature": "N/A",
                "condition": "N/A",
                "wind_speed": "N/A",
                "wind_direction": "N/A",
                "precipitation_chance": "N/A"
            }
            
        weather = data[0]
        return {
            "temperature": weather.get("Temperature", "N/A"),
            "condition": weather.get("Weather Condition", "N/A"),
            "wind_speed": weather.get("Wind Speed", "N/A"),
            "wind_direction": weather.get("Wind Direction", "N/A"),
            "precipitation_chance": weather.get("Precipitation Chance", "N/A")
        }

    def process_injuries(self, data: List[Dict]) -> Dict:
        """Process injury report data"""
        processed = {}
        for player in data:
            try:
                processed[player["Name"]] = {
                    "position": player["Pos"],
                    "injury": player["Injury"],
                    "status": player["Status"],
                    "details": player.get("Details", ""),
                    "updated": player.get("Updated", "")
                }
            except KeyError as e:
                print(f"Warning: Missing key in injury data: {e}")
                continue
        return processed

    def process_team_defense(self, data: Dict) -> Dict:
        """Process team defense statistics"""
        if not data:
            return {}
            
        return {
            "points_against": data.get("Points_Against", 0),
            "total_yards": data.get("Total_Yards", 0),
            "passing_yards": data.get("Passing_Yards", 0),
            "rushing_yards": data.get("Rushing_Yards", 0),
            "turnovers_forced": data.get("Tot_Yds_TO_Turnovers", 0),
            "sacks": data.get("Sacks", 0),
            "interceptions": data.get("Passing_Interceptions", 0),
            "efficiency": {
                "score_percentage": data.get("Score_Percentage", 0),
                "turnover_percentage": data.get("Turnover_Percentage", 0),
                "expected_points": data.get("Expected_Points", 0)
            }
        }

    def process_pressure_stats(self, data: Dict) -> Dict:
        """Process pass pressure and protection statistics"""
        if not data:
            return {}
            
        return {
            "pocket_time": data.get("Passing PktTime", 0),
            "blitzes": data.get("Passing Bltz", 0),
            "hurries": data.get("Passing Hrry", 0),
            "hits": data.get("Passing Hits", 0),
            "pressures": data.get("Passing Prss", 0),
            "pressure_percentage": data.get("Passing Prss%", "0%"),
            "scrambles": data.get("Passing Scrm", 0),
            "yards_per_scramble": data.get("Passing Yds/Scr", 0)
        }

    def process_game_logs(self, data: List[Dict]) -> List[Dict]:
        """Process game logs data"""
        processed = []
        for game in data:
            try:
                processed.append({
                    "week": game.get("Week"),
                    "opponent": game.get("Opp"),
                    "location": game.get("Location"),
                    "score": {
                        "team": game.get("Score_Tm"),
                        "opponent": game.get("Score_Opp")
                    },
                    "stats": {
                        "total_yards": game.get("Total_Yards", 0),
                        "passing_yards": game.get("Passing_Yds", 0),
                        "rushing_yards": game.get("Rushing_Yds", 0),
                        "turnovers": game.get("Turnovers", 0),
                        "third_down": {
                            "attempts": game.get("Downs_3DAtt", 0),
                            "conversions": game.get("Downs_3DConv", 0)
                        },
                        "time_of_possession": game.get("ToP", "0:00")
                    }
                })
            except Exception as e:
                print(f"Warning: Error processing game log: {str(e)}")
                continue
                
        return processed

    def process_odds(self, odds_data: Dict) -> Dict:
        """Process odds data"""
        if not odds_data:
            return {
                "spread": {"home": "N/A", "away": "N/A"},
                "total": "N/A",
                "moneyline": {"home": "N/A", "away": "N/A"}
            }
            
        return {
            "spread": {
                "home": odds_data.get("spread", {}).get("home", "N/A"),
                "away": odds_data.get("spread", {}).get("away", "N/A")
            },
            "total": odds_data.get("overUnder", "N/A"),
            "moneyline": {
                "home": odds_data.get("moneyline", {}).get("home", "N/A"),
                "away": odds_data.get("moneyline", {}).get("away", "N/A")
            }
        }

    def combine_analysis_data(self, raw_data: Dict, game_context: GameContext) -> Dict:
        """Combine all processed data for analysis"""
        try:
            return {
                "game_info": {
                    "id": game_context.game_id,
                    "home_team": game_context.home_team,
                    "away_team": game_context.away_team,
                    "venue": game_context.venue,
                    "date": game_context.date,
                    "weather": self.process_weather(raw_data.get("weather", [])),
                    "odds": self.process_odds(raw_data.get("odds", {}))
                },
                "depth_charts": {
                    "home": self.process_depth_chart(raw_data.get("depth_charts", {}).get("home", [])),
                    "away": self.process_depth_chart(raw_data.get("depth_charts", {}).get("away", []))
                },
                "injuries": {
                    "home": self.process_injuries(raw_data.get("injuries", {}).get("home", [])),
                    "away": self.process_injuries(raw_data.get("injuries", {}).get("away", []))
                },
                "player_stats": {
                    "home": raw_data.get("player_stats", {}).get("home", {}),
                    "away": raw_data.get("player_stats", {}).get("away", {})
                },
                "defense": {
                    "home": self.process_team_defense(raw_data.get("defense", {}).get("home", {})),
                    "away": self.process_team_defense(raw_data.get("defense", {}).get("away", {}))
                },
                "pressure": {
                    "home": self.process_pressure_stats(raw_data.get("pressure", {}).get("home", {})),
                    "away": self.process_pressure_stats(raw_data.get("pressure", {}).get("away", {}))
                },
                "team_stats": {
                    "home": raw_data.get("team_stats", {}).get("home", {}),
                    "away": raw_data.get("team_stats", {}).get("away", {})
                },
                "game_logs": {
                    "home": self.process_game_logs(raw_data.get("game_logs", {}).get("home", [])),
                    "away": self.process_game_logs(raw_data.get("game_logs", {}).get("away", []))
                },
                "opponent_logs": {
                    "home": self.process_game_logs(raw_data.get("opponent_logs", {}).get("home", [])),
                    "away": self.process_game_logs(raw_data.get("opponent_logs", {}).get("away", []))
                }
            }
        except Exception as e:
            print(f"Error combining analysis data: {str(e)}")
            raise