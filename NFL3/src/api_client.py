"""
NFL API Client for handling all API requests
"""
import asyncio
from typing import Dict, List, Optional
import aiohttp
from urllib.parse import quote

class NFLApiClient:
    """Client for handling NFL API requests"""
    
    def __init__(self):
        self.api_base = "https://sportsstatsgather.com/api/nfl/data"
        self.espn_api = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"

    async def get_data(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with proper URL encoding"""
        # Construct URL with proper encoding
        url = f"{self.api_base}/{endpoint}"
        
        # URL encode any team names in params
        if params and 'team' in params:
            params = params.copy()  # Don't modify original
            params['team'] = quote(params['team'])
        
        print(f"Fetching: {url}")
        if params:
            print(f"With params: {params}")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"API call failed: {url} - Status: {response.status}")
                        text = await response.text()
                        print(f"Response: {text}")
                        return {}
            except Exception as e:
                print(f"Error making request to {url}: {str(e)}")
                return {}

    async def get_games(self, week: int) -> List[Dict]:
        """Get games for a specific week"""
        url = f"{self.espn_api}/scoreboard"
        params = {"week": week, "seasontype": 2}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('events', [])
                    print(f"Failed to fetch games: Status {response.status}")
                    return []
            except Exception as e:
                print(f"Error fetching games: {str(e)}")
                return []

    async def get_player_stats(self, team: str, view: str, split: str) -> List[Dict]:
        """Get player statistics"""
        data = await self.get_data("playerstats", {
            "team": team,
            "view": view,
            "split": split
        })
        return data if isinstance(data, list) else []

    async def get_team_stats(self, team: str) -> Dict:
        """Get team statistics"""
        return await self.get_data("teamstats/team", {"team": team})

    async def get_depth_chart(self, team: str) -> List[Dict]:
        """Get team depth chart"""
        data = await self.get_data("depthchart", {"team": team})
        return data if isinstance(data, list) else []

    async def get_injuries(self, team: str) -> List[Dict]:
        """Get team injury report"""
        data = await self.get_data("injuryreports", {"team": team})
        return data if isinstance(data, list) else []

    async def get_weather(self) -> List[Dict]:
        """Get weather data"""
        data = await self.get_data("weather")
        return data if isinstance(data, list) else []

    async def get_team_defense(self, team: str) -> Dict:
        """Get team defense statistics"""
        return await self.get_data("teamdefense", {"team": team})

    async def get_pass_pressure(self, team: str) -> Dict:
        """Get team pass pressure statistics"""
        return await self.get_data("teampasspressure", {"team": team})

    async def get_game_logs(self, team: str) -> List[Dict]:
        """Get team game logs"""
        data = await self.get_data("gamelogs", {"team": team})
        return data if isinstance(data, list) else []

    async def get_opponent_logs(self, team: str) -> List[Dict]:
        """Get team opponent game logs"""
        data = await self.get_data("oppgamelogs", {"team": team})
        return data if isinstance(data, list) else []

    async def get_odds(self, game_id: str) -> Optional[Dict]:
        """Get game odds from ESPN"""
        url = f"{self.espn_api}/scoreboard/{game_id}/odds"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    return None
            except Exception as e:
                print(f"Error fetching odds: {str(e)}")
                return None

    async def fetch_all_game_data(self, game_data: Dict) -> Dict:
        """Fetch all data needed for game analysis"""
        home_team = game_data['competitions'][0]['competitors'][0]['team']['displayName']
        away_team = game_data['competitions'][0]['competitors'][1]['team']['displayName']

        # Create tasks for parallel fetching
        tasks = {
            'home_depth': self.get_depth_chart(home_team),
            'away_depth': self.get_depth_chart(away_team),
            'weather': self.get_weather(),
            'home_injuries': self.get_injuries(home_team),
            'away_injuries': self.get_injuries(away_team),
            'home_defense': self.get_team_defense(home_team),
            'away_defense': self.get_team_defense(away_team),
            'home_pressure': self.get_pass_pressure(home_team),
            'away_pressure': self.get_pass_pressure(away_team),
            'home_stats': self.get_team_stats(home_team),
            'away_stats': self.get_team_stats(away_team),
            'home_logs': self.get_game_logs(home_team),
            'away_logs': self.get_game_logs(away_team),
            'home_opp_logs': self.get_opponent_logs(home_team),
            'away_opp_logs': self.get_opponent_logs(away_team),
            'odds': self.get_odds(game_data['id'])
        }

        # Execute all tasks
        results = {}
        for key, task in tasks.items():
            try:
                results[key] = await task
            except Exception as e:
                print(f"Error fetching {key}: {str(e)}")
                results[key] = [] if 'logs' in key or key.endswith('_depth') or key.endswith('injuries') else {}

        # Organize results
        return {
            "depth_charts": {
                "home": results['home_depth'],
                "away": results['away_depth']
            },
            "weather": results['weather'],
            "injuries": {
                "home": results['home_injuries'],
                "away": results['away_injuries']
            },
            "defense": {
                "home": results['home_defense'],
                "away": results['away_defense']
            },
            "pressure": {
                "home": results['home_pressure'],
                "away": results['away_pressure']
            },
            "team_stats": {
                "home": results['home_stats'],
                "away": results['away_stats']
            },
            "game_logs": {
                "home": results['home_logs'],
                "away": results['away_logs']
            },
            "opponent_logs": {
                "home": results['home_opp_logs'],
                "away": results['away_opp_logs']
            },
            "odds": results['odds']
        }