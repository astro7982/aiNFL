"""
NFL API Client for handling all API requests with enhanced error handling and retry logic
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
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    async def get_data(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make API request with proper URL encoding and retry logic"""
        # Construct base URL with properly encoded parameters
        base_url = f"{self.api_base}/{endpoint}"
        
        # Build query string manually
        if params:
            query_parts = []
            for key, value in params.items():
                if value is not None:
                    encoded_value = quote(str(value), safe='')
                    query_parts.append(f"{key}={encoded_value}")
            url = f"{base_url}?{'&'.join(query_parts)}" if query_parts else base_url
        else:
            url = base_url
        
        print(f"Fetching: {url}")

        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 404:
                            # Return appropriate empty structure based on endpoint
                            if 'depthchart' in endpoint or 'gamelogs' in endpoint:
                                return []
                            return {}
                        else:
                            if attempt == self.max_retries - 1:
                                print(f"API call failed: {url} - Status: {response.status}")
                                print(f"Response: {await response.text()}")
                            
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(self.retry_delay)
                                continue
                            
                            return [] if 'depthchart' in endpoint or 'gamelogs' in endpoint else {}
                            
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"Error making request to {url}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                return [] if 'depthchart' in endpoint or 'gamelogs' in endpoint else {}

    async def get_games(self, week: int) -> List[Dict]:
        """Get games for a specific week"""
        url = f"{self.espn_api}/scoreboard"
        params = {"week": week, "seasontype": 2}
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            return data.get('events', [])
                        
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(self.retry_delay)
                            continue
                            
                        print(f"Failed to fetch games: Status {response.status}")
                        return []
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"Error fetching games: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                return []
        
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
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                        
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(self.retry_delay)
                            continue
                            
                        return None
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"Error fetching odds: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                return None
        
        return None

    async def fetch_all_game_data(self, game_data: Dict) -> Dict:
        """Fetch all data needed for game analysis"""
        home_team = game_data['competitions'][0]['competitors'][0]['team']['displayName']
        away_team = game_data['competitions'][0]['competitors'][1]['team']['displayName']

        # Sequential fetching with delay between requests
        results = {}
        
        async def fetch_with_delay(key: str, coro):
            """Helper to fetch data with delay"""
            try:
                results[key] = await coro
            except Exception as e:
                print(f"Error fetching {key}: {str(e)}")
                results[key] = [] if 'logs' in key or key.endswith('_depth') or key.endswith('injuries') else {}
            await asyncio.sleep(0.5)  # Delay between requests

        # Fetch data sequentially
        await fetch_with_delay('home_depth', self.get_depth_chart(home_team))
        await fetch_with_delay('away_depth', self.get_depth_chart(away_team))
        await fetch_with_delay('weather', self.get_weather())
        await fetch_with_delay('home_injuries', self.get_injuries(home_team))
        await fetch_with_delay('away_injuries', self.get_injuries(away_team))
        await fetch_with_delay('home_defense', self.get_team_defense(home_team))
        await fetch_with_delay('away_defense', self.get_team_defense(away_team))
        await fetch_with_delay('home_pressure', self.get_pass_pressure(home_team))
        await fetch_with_delay('away_pressure', self.get_pass_pressure(away_team))
        await fetch_with_delay('home_stats', self.get_team_stats(home_team))
        await fetch_with_delay('away_stats', self.get_team_stats(away_team))
        await fetch_with_delay('home_logs', self.get_game_logs(home_team))
        await fetch_with_delay('away_logs', self.get_game_logs(away_team))
        await fetch_with_delay('home_opp_logs', self.get_opponent_logs(home_team))
        await fetch_with_delay('away_opp_logs', self.get_opponent_logs(away_team))
        await fetch_with_delay('odds', self.get_odds(game_data['id']))

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