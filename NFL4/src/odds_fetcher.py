import aiohttp
from typing import Dict, Optional
import json
import asyncio

class NFLOddsFetcher:
    """Handle fetching and processing of NFL odds data with enhanced error handling"""
    
    def __init__(self):
        self.espn_odds_base = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    async def get_odds(self, game_id: str) -> Optional[Dict]:
        """Fetch current odds for a game from ESPN with retry logic"""
        url = f"{self.espn_odds_base}/events/{game_id}/competitions/{game_id}/odds"
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            return self._process_odds_data(data)
                            
                        if attempt == self.max_retries - 1:
                            print(f"Failed to fetch odds: Status {response.status}")
                            
                        if attempt < self.max_retries - 1:
                            await asyncio.sleep(self.retry_delay)
                            continue
                            
                        return None
                        
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"Error fetching odds data: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                return None
        
        return None

    def _process_odds_data(self, data: Dict) -> Optional[Dict]:
        """Process raw odds data from ESPN with validation"""
        try:
            # Find ESPN BET provider (primary source)
            espn_bet_odds = next(
                (item for item in data.get('items', [])
                 if item.get('provider', {}).get('name') == "ESPN BET"),
                None
            )

            # If ESPN BET not found, try any available provider
            if not espn_bet_odds and data.get('items'):
                espn_bet_odds = data['items'][0]

            if not espn_bet_odds:
                return None

            # Extract and validate odds data
            processed_odds = {
                'overUnder': espn_bet_odds.get('overUnder'),
                'spread': {
                    'home': self._safe_get_spread(espn_bet_odds, 'homeTeamOdds'),
                    'away': self._safe_get_spread(espn_bet_odds, 'awayTeamOdds')
                },
                'moneyline': {
                    'home': self._safe_get_value(espn_bet_odds, ['homeTeamOdds', 'moneyLine']),
                    'away': self._safe_get_value(espn_bet_odds, ['awayTeamOdds', 'moneyLine'])
                }
            }
            
            # Validate essential fields
            if all(v is None for v in [
                processed_odds['overUnder'],
                processed_odds['spread']['home'],
                processed_odds['spread']['away'],
                processed_odds['moneyline']['home'],
                processed_odds['moneyline']['away']
            ]):
                return None
                
            return processed_odds
            
        except Exception as e:
            print(f"Error processing odds data: {str(e)}")
            return None

    def _safe_get_spread(self, odds_data: Dict, team_key: str) -> Optional[float]:
        """Safely extract spread value with validation"""
        try:
            spread = odds_data.get(team_key, {}).get('pointSpread', {}).get('american')
            return float(spread) if spread is not None else None
        except (ValueError, TypeError):
            return None

    def _safe_get_value(self, data: Dict, keys: list) -> Optional[float]:
        """Safely navigate nested dictionary with validation"""
        try:
            value = data
            for key in keys:
                value = value.get(key)
                if value is None:
                    return None
            return float(value)
        except (ValueError, TypeError, AttributeError):
            return None

    def format_odds_for_analysis(self, odds_data: Optional[Dict]) -> str:
        """Format odds data for prompt inclusion with default handling"""
        if not odds_data:
            return "Odds data unavailable"
            
        try:
            spread_home = odds_data['spread']['home']
            spread_away = odds_data['spread']['away']
            total = odds_data['overUnder']
            ml_home = odds_data['moneyline']['home']
            ml_away = odds_data['moneyline']['away']
            
            # Format with appropriate handling of None values
            lines = [
                f"Spread: Home {spread_home if spread_home is not None else 'N/A'}, "
                f"Away {spread_away if spread_away is not None else 'N/A'}",
                f"Total: {total if total is not None else 'N/A'}",
                f"Moneyline: Home {ml_home if ml_home is not None else 'N/A'}, "
                f"Away {ml_away if ml_away is not None else 'N/A'}"
            ]
            
            return "\n".join(lines)
            
        except Exception as e:
            print(f"Error formatting odds data: {str(e)}")
            return "Error formatting odds data"

    async def fetch_odds_with_timeout(self, game_id: str, timeout: int = 10) -> Optional[Dict]:
        """Fetch odds with timeout protection"""
        try:
            odds_data = await asyncio.wait_for(self.get_odds(game_id), timeout)
            return odds_data
        except asyncio.TimeoutError:
            print(f"Timeout fetching odds for game {game_id}")
            return None
        except Exception as e:
            print(f"Error fetching odds with timeout: {str(e)}")
            return None