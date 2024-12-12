import aiohttp
from typing import Dict, Optional
import json

class NFLOddsFetcher:
    """Handle fetching and processing of NFL odds data"""
    
    def __init__(self):
        self.espn_odds_base = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"

    async def get_odds(self, game_id: str) -> Optional[Dict]:
        """Fetch current odds for a game from ESPN"""
        url = f"{self.espn_odds_base}/events/{game_id}/competitions/{game_id}/odds"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_odds_data(data)
                    return None
            except Exception as e:
                print(f"Error fetching odds data: {str(e)}")
                return None

    def _process_odds_data(self, data: Dict) -> Optional[Dict]:
        """Process raw odds data from ESPN"""
        try:
            # Find ESPN BET provider
            espn_bet_odds = next(
                (item for item in data.get('items', [])
                 if item.get('provider', {}).get('name') == "ESPN BET"),
                None
            )

            if not espn_bet_odds:
                return None

            return {
                'overUnder': espn_bet_odds.get('overUnder'),
                'spread': {
                    'home': espn_bet_odds.get('homeTeamOdds', {}).get('pointSpread', {}).get('american'),
                    'away': espn_bet_odds.get('awayTeamOdds', {}).get('pointSpread', {}).get('american')
                },
                'moneyline': {
                    'home': espn_bet_odds.get('homeTeamOdds', {}).get('moneyLine'),
                    'away': espn_bet_odds.get('awayTeamOdds', {}).get('moneyLine')
                }
            }
        except Exception as e:
            print(f"Error processing odds data: {str(e)}")
            return None

    def format_odds_for_analysis(self, odds_data: Optional[Dict]) -> str:
        """Format odds data for prompt inclusion"""
        if not odds_data:
            return "Odds data unavailable"
            
        return (
            f"Spread: Home {odds_data['spread']['home']}, Away {odds_data['spread']['away']}\n"
            f"Total: {odds_data['overUnder']}\n"
            f"Moneyline: Home {odds_data['moneyline']['home']}, Away {odds_data['moneyline']['away']}"
        )