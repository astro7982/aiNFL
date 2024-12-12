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
    """Process NFL data for analysis with enhanced error handling"""
    
    def process_depth_chart(self, data: List[Dict]) -> Dict:
        """Process depth chart data into structured format with validation"""
        default_chart = {
            "offense": {},
            "defense": {},
            "special_teams": {}
        }
        
        if not data:
            return default_chart
            
        processed = default_chart.copy()
        
        for player in data:
            try:
                section = player.get("Section", "").lower().replace(" positions", "")
                if section not in processed:
                    continue
                    
                position = player.get("Position")
                if not position:
                    continue
                
                processed[section][position] = {
                    "starter": player.get("Starter", "-"),
                    "backup": player.get("2ND", "-"),
                    "third_string": player.get("3RD", "-"),
                    "fourth_string": player.get("4TH", "-")
                }
            except Exception as e:
                print(f"Warning: Error processing depth chart entry: {str(e)}")
                continue
        
        return processed

    def process_player_stats(self, data: List[Dict], stat_type: str, timeframe: str) -> Dict:
        """Process player statistics with enhanced validation"""
        processed = {}
        prefix = f"{stat_type} {timeframe} "
        
        for player in data:
            try:
                if not player.get("Name") or not player.get("Position"):
                    continue
                    
                # Filter stats for the specific timeframe and remove invalid values
                stats = {}
                for k, v in player.items():
                    if k.startswith(prefix) and isinstance(v, (int, float, str)):
                        try:
                            # Convert string numbers to float if possible
                            if isinstance(v, str) and v.replace('.', '').isdigit():
                                v = float(v)
                            if str(v).lower() != 'nan':
                                stats[k.replace(prefix, "")] = v
                        except ValueError:
                            continue
                
                if stats:  # Only include players with valid stats
                    processed[player["Name"]] = {
                        "position": player["Position"],
                        "stats": stats
                    }
            except Exception as e:
                print(f"Warning: Error processing player stats: {str(e)}")
                continue
                
        return processed

    def process_weather(self, data: List[Dict]) -> Dict:
        """Process weather data with defaults"""
        default_weather = {
            "temperature": "N/A",
            "condition": "N/A",
            "wind_speed": "N/A",
            "wind_direction": "N/A",
            "precipitation_chance": "N/A"
        }
        
        if not data:
            return default_weather
            
        try:
            weather = data[0]
            return {
                "temperature": weather.get("Temperature", "N/A"),
                "condition": weather.get("Weather Condition", "N/A"),
                "wind_speed": weather.get("Wind Speed", "N/A"),
                "wind_direction": weather.get("Wind Direction", "N/A"),
                "precipitation_chance": weather.get("Precipitation Chance", "N/A")
            }
        except Exception as e:
            print(f"Warning: Error processing weather data: {str(e)}")
            return default_weather

    def process_injuries(self, data: List[Dict]) -> Dict:
        """Process injury report data with validation"""
        processed = {}
        for player in data:
            try:
                name = player.get("Name")
                if not name:
                    continue
                    
                processed[name] = {
                    "position": player.get("Pos", "N/A"),
                    "injury": player.get("Injury", "N/A"),
                    "status": player.get("Status", "N/A"),
                    "details": player.get("Details", ""),
                    "updated": player.get("Updated", "")
                }
            except Exception as e:
                print(f"Warning: Error processing injury data: {str(e)}")
                continue
        return processed

    def process_team_defense(self, data: Dict) -> Dict:
        """Process team defense statistics with defaults"""
        if not data:
            return {
                "points_against": 0,
                "total_yards": 0,
                "passing_yards": 0,
                "rushing_yards": 0,
                "turnovers_forced": 0,
                "sacks": 0,
                "interceptions": 0,
                "efficiency": {
                    "score_percentage": 0,
                    "turnover_percentage": 0,
                    "expected_points": 0
                }
            }
            
        try:
            return {
                "points_against": float(data.get("Points_Against", 0)),
                "total_yards": float(data.get("Total_Yards", 0)),
                "passing_yards": float(data.get("Passing_Yards", 0)),
                "rushing_yards": float(data.get("Rushing_Yards", 0)),
                "turnovers_forced": float(data.get("Tot_Yds_TO_Turnovers", 0)),
                "sacks": float(data.get("Sacks", 0)),
                "interceptions": float(data.get("Passing_Interceptions", 0)),
                "efficiency": {
                    "score_percentage": float(data.get("Score_Percentage", 0)),
                    "turnover_percentage": float(data.get("Turnover_Percentage", 0)),
                    "expected_points": float(data.get("Expected_Points", 0))
                }
            }
        except Exception as e:
            print(f"Warning: Error processing defense stats: {str(e)}")
            return self.process_team_defense({})  # Return default values

    def process_pressure_stats(self, data: Dict) -> Dict:
        """Process pass pressure and protection statistics with defaults"""
        if not data:
            return {
                "pocket_time": 0,
                "blitzes": 0,
                "hurries": 0,
                "hits": 0,
                "pressures": 0,
                "pressure_percentage": "0%",
                "scrambles": 0,
                "yards_per_scramble": 0
            }
            
        try:
            return {
                "pocket_time": float(data.get("Passing PktTime", 0)),
                "blitzes": int(data.get("Passing Bltz", 0)),
                "hurries": int(data.get("Passing Hrry", 0)),
                "hits": int(data.get("Passing Hits", 0)),
                "pressures": int(data.get("Passing Prss", 0)),
                "pressure_percentage": str(data.get("Passing Prss%", "0%")),
                "scrambles": int(data.get("Passing Scrm", 0)),
                "yards_per_scramble": float(data.get("Passing Yds/Scr", 0))
            }
        except Exception as e:
            print(f"Warning: Error processing pressure stats: {str(e)}")
            return self.process_pressure_stats({})  # Return default values

    def process_game_logs(self, data: List[Dict]) -> List[Dict]:
        """Process game logs data with validation"""
        processed = []
        for game in data:
            try:
                # Only process if we have basic required fields
                if not all(key in game for key in ["Week", "Opp", "Score_Tm", "Score_Opp"]):
                    continue
                    
                processed.append({
                    "week": game["Week"],
                    "opponent": game["Opp"],
                    "location": game.get("Location", "N/A"),
                    "score": {
                        "team": int(game["Score_Tm"]),
                        "opponent": int(game["Score_Opp"])
                    },
                    "stats": {
                        "total_yards": int(game.get("Total_Yards", 0)),
                        "passing_yards": int(game.get("Passing_Yds", 0)),
                        "rushing_yards": int(game.get("Rushing_Yds", 0)),
                        "turnovers": int(game.get("Turnovers", 0)),
                        "third_down": {
                            "attempts": int(game.get("Downs_3DAtt", 0)),
                            "conversions": int(game.get("Downs_3DConv", 0))
                        },
                        "time_of_possession": game.get("ToP", "0:00")
                    }
                })
            except Exception as e:
                print(f"Warning: Error processing game log: {str(e)}")
                continue
                
        return processed

    def process_odds(self, odds_data: Optional[Dict]) -> Dict:
        """Process odds data with defaults"""
        if not odds_data:
            return {
                "spread": {"home": "N/A", "away": "N/A"},
                "total": "N/A",
                "moneyline": {"home": "N/A", "away": "N/A"}
            }
        
        try:    
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
        except Exception as e:
            print(f"Warning: Error processing odds data: {str(e)}")
            return self.process_odds(None)  # Return default values

    def combine_analysis_data(self, raw_data: Dict, game_context: GameContext) -> Dict:
        """Combine all processed data for analysis with enhanced error handling"""
        try:
            return {
                "game_info": {
                    "id": game_context.game_id,
                    "home_team": game_context.home_team,
                    "away_team": game_context.away_team,
                    "venue": game_context.venue,
                    "date": game_context.date,
                    "weather": self.process_weather(raw_data.get("weather", [])),
                    "odds": self.process_odds(raw_data.get("odds"))
                },
                "depth_charts": {
                    "home": self.process_depth_chart(raw_data.get("depth_charts", {}).get("home", [])),
                    "away": self.process_depth_chart(raw_data.get("depth_charts", {}).get("away", []))
                },
                "injuries": {
                    "home": self.process_injuries(raw_data.get("injuries", {}).get("home", [])),
                    "away": self.process_injuries(raw_data.get("injuries", {}).get("away", []))
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