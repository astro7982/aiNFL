"""
NFL Data Processor module for handling all data processing operations
"""
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime

class NFLDataProcessor:
    def __init__(self):
        self.stat_mappings = {
            'Passing': ['ATT', 'CMP', 'YDS', 'TD', 'INT', 'RATE'],
            'Rushing': ['ATT', 'YDS', 'TD', 'AVG'],
            'Receiving': ['REC', 'TGT', 'YDS', 'TD', 'AVG']
        }

    def process_depth_chart(self, raw_data: List[Dict]) -> Dict[str, Dict]:
        """Process depth chart data into organized structure"""
        processed = {}
        for entry in raw_data:
            position = entry.get('Position', '')
            if position:
                processed[position] = {
                    'starter': entry.get('Starter', ''),
                    'second_string': entry.get('2ND', ''),
                    'third_string': entry.get('3RD', ''),
                    'fourth_string': entry.get('4TH', ''),
                    'section': entry.get('Section', '')
                }
        return processed

    def process_weather(self, raw_data: List[Dict]) -> Dict:
        """Process weather data"""
        if not raw_data:
            return {}
            
        weather = raw_data[0]
        return {
            'temperature': weather.get('Temperature', 'N/A'),
            'precipitation': weather.get('Precipitation Chance', '0%'),
            'wind_speed': weather.get('Wind Speed', 0),
            'wind_direction': weather.get('Wind Direction', 'N/A'),
            'conditions': weather.get('Weather Condition', 'N/A')
        }

    def process_injuries(self, raw_data: List[Dict]) -> Dict[str, List]:
        """Process injury report data"""
        processed = {'OUT': [], 'QUESTIONABLE': [], 'DOUBTFUL': [], 'IR': []}
        
        for injury in raw_data:
            status = injury.get('Status', 'UNKNOWN')
            player_info = {
                'name': injury.get('Name', ''),
                'position': injury.get('Pos', ''),
                'injury': injury.get('Injury', ''),
                'details': injury.get('Details', ''),
                'updated': injury.get('Updated', '')
            }
            
            if status in processed:
                processed[status].append(player_info)
                
        return processed

    def process_player_stats(self, raw_data: List[Dict], stat_type: str) -> Dict[str, Dict]:
        """Process player statistics for passing, rushing, or receiving"""
        processed = {}
        for player in raw_data:
            if pd.isna(player.get(f'{stat_type} Last 4 Weeks ATT', 0)):
                continue
                
            name = player.get('Name', '')
            if name:
                stats = {}
                for metric in self.stat_mappings.get(stat_type, []):
                    stat_key = f'{stat_type} Last 4 Weeks {metric}'
                    stats[metric] = player.get(stat_key, 0)
                    
                processed[name] = {
                    'position': player.get('Position', ''),
                    'stats': stats
                }
                
        return processed

    def process_team_defense(self, raw_data: List[Dict]) -> Dict:
        """Process team defense statistics"""
        if not raw_data:
            return {}
            
        defense = raw_data[0]
        return {
            'points_against': defense.get('Points_Against', 0),
            'total_yards': defense.get('Total_Yards', 0),
            'passing_yards': defense.get('Passing_Yards', 0),
            'rushing_yards': defense.get('Rushing_Yards', 0),
            'turnovers': defense.get('Tot_Yds_TO_Turnovers', 0),
            'sacks': defense.get('Passing_Sacks', 0)
        }

    def process_pass_pressure(self, raw_data: List[Dict]) -> Dict:
        """Process pass pressure statistics"""
        if not raw_data:
            return {}
            
        pressure = raw_data[0]
        return {
            'blitzes': pressure.get('Passing Bltz', 0),
            'hits': pressure.get('Passing Hits', 0),
            'hurries': pressure.get('Passing Hrry', 0),
            'pressure_pct': pressure.get('Passing Prss%', '0%'),
            'pocket_time': pressure.get('Passing PktTime', 0)
        }

    def process_game_logs(self, raw_data: List[Dict]) -> List[Dict]:
        """Process game logs into analyzable format"""
        processed = []
        for game in raw_data:
            processed.append({
                'date': game.get('Date', ''),
                'opponent': game.get('Opp', ''),
                'location': game.get('Location', ''),
                'score': {
                    'team': game.get('Score_Tm', 0),
                    'opponent': game.get('Score_Opp', 0)
                },
                'stats': {
                    'passing_yards': game.get('Passing_Yds', 0),
                    'rushing_yards': game.get('Rushing_Yds', 0),
                    'third_down': {
                        'attempts': game.get('Downs_3DAtt', 0),
                        'conversions': game.get('Downs_3DConv', 0)
                    },
                    'time_of_possession': game.get('ToP', '00:00')
                }
            })
        return processed

    def process_team_stats(self, raw_data: List[Dict]) -> Dict:
        """Process team statistics"""
        processed = {}
        for stat in raw_data:
            scenario = stat.get('Stat Scenario', '')
            if scenario:
                processed[scenario] = {
                    'current': stat.get('2024', '0'),
                    'previous': stat.get('2023', '0'),
                    'home': stat.get('Home', '0'),
                    'away': stat.get('Away', '0'),
                    'last_game': stat.get('Last 1', '0'),
                    'last_three': stat.get('Last 3', '0'),
                    'rank': stat.get('Rank', 0)
                }
        return processed

    def clean_numeric(self, value: Any) -> float:
        """Clean numeric values from API responses"""
        if pd.isna(value):
            return 0.0
        if isinstance(value, str):
            try:
                return float(value.strip('%')) if '%' in value else float(value)
            except ValueError:
                return 0.0
        return float(value) if value else 0.0

    def calculate_efficiency_metrics(self, stats: Dict) -> Dict:
        """Calculate efficiency metrics from raw statistics"""
        metrics = {}
        
        # Passing efficiency
        att = self.clean_numeric(stats.get('ATT', 0))
        if att > 0:
            metrics['completion_pct'] = (self.clean_numeric(stats.get('CMP', 0)) / att) * 100
            metrics['yards_per_attempt'] = self.clean_numeric(stats.get('YDS', 0)) / att
            
        # Rushing efficiency
        rush_att = self.clean_numeric(stats.get('Rushing_ATT', 0))
        if rush_att > 0:
            metrics['yards_per_carry'] = self.clean_numeric(stats.get('Rushing_YDS', 0)) / rush_att
            
        return metrics