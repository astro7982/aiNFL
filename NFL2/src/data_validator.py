"""
NFL Data Validator module for ensuring data quality and completeness
"""
from typing import Dict, List, Any, Optional
import pandas as pd

class NFLDataValidator:
    def __init__(self):
        self.required_fields = {
            'depth_chart': ['Position', 'Section', 'Starter'],
            'weather': ['Temperature', 'Wind Speed', 'Wind Direction'],
            'injuries': ['Name', 'Position', 'Status', 'Updated'],
            'player_stats': ['Name', 'Position', 'Team'],
            'team_defense': ['Team', 'Games', 'Points_Against'],
            'team_pressure': ['Team', 'Passing Bltz', 'Passing Prss%'],
            'game_logs': ['Date', 'Team', 'Opp', 'Score_Tm', 'Score_Opp']
        }
        
        self.expected_ranges = {
            'temperature': (-20, 120),  # Fahrenheit
            'wind_speed': (0, 75),      # MPH
            'points': (0, 100),         # Game points
            'yards': (0, 1000),         # Game yards
            'completion_pct': (0, 100),  # Completion percentage
            'probability': (0, 100)      # Any probability metric
        }

    def validate_api_response(self, data: Any, data_type: str) -> tuple[bool, str]:
        """Validate API response data"""
        if data is None:
            return False, "No data received"
            
        if not isinstance(data, (list, dict)):
            return False, f"Invalid data format: expected list or dict, got {type(data)}"
            
        if isinstance(data, list) and not data:
            return False, "Empty data list received"
            
        required = self.required_fields.get(data_type, [])
        if not self._check_required_fields(data, required):
            return False, f"Missing required fields for {data_type}"
            
        return True, "Data validation successful"

    def _check_required_fields(self, data: Any, required: List[str]) -> bool:
        """Check if all required fields are present"""
        if isinstance(data, list):
            return all(self._check_required_fields(item, required) for item in data)
            
        if isinstance(data, dict):
            return all(field in data for field in required)
            
        return False

    def validate_numeric_range(self, value: Any, metric_type: str) -> tuple[bool, str]:
        """Validate numeric value is within expected range"""
        if not isinstance(value, (int, float)):
            try:
                value = float(value.strip('%')) if isinstance(value, str) and '%' in value else float(value)
            except (ValueError, AttributeError):
                return False, f"Invalid numeric value for {metric_type}"

        expected_range = self.expected_ranges.get(metric_type)
        if expected_range and not (expected_range[0] <= value <= expected_range[1]):
            return False, f"Value {value} for {metric_type} outside expected range {expected_range}"
            
        return True, "Numeric validation successful"

    def validate_depth_chart_data(self, data: List[Dict]) -> tuple[bool, List[str]]:
        """Validate depth chart data structure and content"""
        errors = []
        
        if not isinstance(data, list):
            return False, ["Depth chart data must be a list"]
            
        for entry in data:
            if not isinstance(entry, dict):
                errors.append("Invalid entry format in depth chart")
                continue
                
            if 'Position' not in entry:
                errors.append("Missing Position in depth chart entry")
                
            if 'Section' not in entry:
                errors.append("Missing Section in depth chart entry")
                
            if 'Starter' not in entry:
                errors.append("Missing Starter in depth chart entry")

        return len(errors) == 0, errors

    def validate_weather_data(self, data: Dict) -> tuple[bool, List[str]]:
        """Validate weather data structure and content"""
        errors = []
        
        if not isinstance(data, dict):
            return False, ["Weather data must be a dictionary"]
            
        # Check temperature
        temp = data.get('Temperature', '')
        if not temp or not isinstance(temp, str):
            errors.append("Invalid temperature data")
        elif '°' not in temp:
            errors.append("Temperature missing degree symbol")
            
        # Check wind speed
        wind_speed = data.get('Wind Speed', None)
        if not isinstance(wind_speed, (int, float)):
            errors.append("Invalid wind speed data")
        elif not (0 <= wind_speed <= 100):
            errors.append("Wind speed out of reasonable range")
            
        # Check precipitation
        precip = data.get('Precipitation Chance', '')
        if not precip or not isinstance(precip, str):
            errors.append("Invalid precipitation data")
        elif '%' not in precip:
            errors.append("Precipitation missing percentage symbol")

        return len(errors) == 0, errors

    def validate_injury_data(self, data: List[Dict]) -> tuple[bool, List[str]]:
        """Validate injury report data structure and content"""
        errors = []
        
        if not isinstance(data, list):
            return False, ["Injury data must be a list"]
            
        valid_statuses = {'OUT', 'QUESTIONABLE', 'DOUBTFUL', 'IR'}
        
        for entry in data:
            if not isinstance(entry, dict):
                errors.append("Invalid entry format in injury report")
                continue
                
            if 'Status' not in entry or entry['Status'] not in valid_statuses:
                errors.append(f"Invalid status for player {entry.get('Name', 'Unknown')}")
                
            if not entry.get('Updated'):
                errors.append(f"Missing update date for player {entry.get('Name', 'Unknown')}")
                
            if not entry.get('Name') or not entry.get('Position'):
                errors.append("Missing player name or position in injury report")

        return len(errors) == 0, errors

    def validate_player_stats(self, data: List[Dict], stat_type: str) -> tuple[bool, List[str]]:
        """Validate player statistics data"""
        errors = []
        
        if not isinstance(data, list):
            return False, ["Player stats data must be a list"]
            
        valid_stat_types = {'Passing', 'Rushing', 'Receiving'}
        if stat_type not in valid_stat_types:
            return False, [f"Invalid stat type: {stat_type}"]
            
        for entry in data:
            if not isinstance(entry, dict):
                errors.append("Invalid entry format in player stats")
                continue
                
            if not entry.get('Name') or not entry.get('Position'):
                errors.append("Missing player name or position")
                continue
                
            # Validate specific stat type metrics
            if stat_type == 'Passing':
                if 'ATT' not in entry or 'CMP' not in entry:
                    errors.append(f"Missing key passing stats for {entry.get('Name', 'Unknown')}")
            elif stat_type == 'Rushing':
                if 'ATT' not in entry or 'YDS' not in entry:
                    errors.append(f"Missing key rushing stats for {entry.get('Name', 'Unknown')}")
            elif stat_type == 'Receiving':
                if 'REC' not in entry or 'YDS' not in entry:
                    errors.append(f"Missing key receiving stats for {entry.get('Name', 'Unknown')}")

        return len(errors) == 0, errors

    def validate_game_logs(self, data: List[Dict]) -> tuple[bool, List[str]]:
        """Validate game logs data structure and content"""
        errors = []
        
        if not isinstance(data, list):
            return False, ["Game logs data must be a list"]
            
        required_fields = {'Date', 'Opp', 'Score_Tm', 'Score_Opp', 'Location'}
        
        for entry in data:
            if not isinstance(entry, dict):
                errors.append("Invalid entry format in game logs")
                continue
                
            missing_fields = required_fields - set(entry.keys())
            if missing_fields:
                errors.append(f"Missing required fields in game log: {missing_fields}")
                
            # Validate scores are numeric
            try:
                float(entry.get('Score_Tm', 0))
                float(entry.get('Score_Opp', 0))
            except (ValueError, TypeError):
                errors.append(f"Invalid score format in game log for {entry.get('Date', 'Unknown')}")

        return len(errors) == 0, errors

    def validate_team_stats(self, data: List[Dict]) -> tuple[bool, List[str]]:
        """Validate team statistics data"""
        errors = []
        
        if not isinstance(data, list):
            return False, ["Team stats data must be a list"]
            
        for entry in data:
            if not isinstance(entry, dict):
                errors.append("Invalid entry format in team stats")
                continue
                
            if 'Stat Scenario' not in entry:
                errors.append("Missing Stat Scenario in team stats")
                
            # Validate numeric fields
            numeric_fields = ['2024', '2023', 'Last 1', 'Last 3', 'Rank']
            for field in numeric_fields:
                if field in entry:
                    try:
                        float(entry[field])
                    except (ValueError, TypeError):
                        errors.append(f"Invalid numeric value for {field} in team stats")

        return len(errors) == 0, errors