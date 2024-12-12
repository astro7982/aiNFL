import aiohttp
import asyncio
import json
import time
import requests
from typing import List, Dict, Any, Tuple
from datetime import datetime

class NFLAnalyzer:
    def __init__(self):
        print("\nInitializing NFL Analyzer with Ollama...")
        self.ollama_url = "http://localhost:11434/api/generate"
        self.api_base = "https://sportsstatsgather.com/api"
        self.espn_api = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
        self.model = "llama3.2"
        self.model_params = {
            "context_length": 65536,
            "num_ctx": 65536,
            "num_gpu": 1,
            "num_thread": 4,
            "gpu_layers": 35
        }
        self.analyses = {}
        
        # Load prompts from JSON file
        try:
            with open('nfl_prompts.json', 'r') as f:
                self.prompts = json.load(f)
            print("✓ Prompts loaded successfully")
        except FileNotFoundError:
            print("❌ Error: nfl_prompts.json not found in current directory")
            raise
        except json.JSONDecodeError:
            print("❌ Error: Invalid JSON in nfl_prompts.json")
            raise

    async def get_data(self, endpoint: str, params: dict = None) -> Dict:
        """Fetch data from the NFL API"""
        url = f"{self.api_base}/nfl/data/{endpoint}"
        print(f"Fetching data from: {url}")
        print(f"Parameters: {params}")
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                elapsed = time.time() - start_time
                print(f"✓ Data received in {elapsed:.2f} seconds")
                return data

    async def get_weeks(self) -> List[Dict]:
        """Get available NFL weeks from ESPN API"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.espn_api}/scoreboard"
            async with session.get(url) as response:
                data = await response.json()
                return list(range(1, 19))  # Regular season weeks 1-18

    async def get_games(self, week: int) -> List[Dict]:
        """Get games for specified week from ESPN API"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.espn_api}/scoreboard?week={week}&seasontype=2"
            async with session.get(url) as response:
                data = await response.json()
                return data.get('events', [])

    async def get_game_odds(self, game_data: Dict) -> Dict:
        """Extract odds from game data"""
        try:
            competitions = game_data.get('competitions', [{}])[0]
            odds = competitions.get('odds', [{}])[0] if competitions.get('odds') else {}
            
            return {
                "spread_home": odds.get('homeTeamOdds', {}).get('pointSpread', {}).get('american', 'N/A'),
                "spread_away": odds.get('awayTeamOdds', {}).get('pointSpread', {}).get('american', 'N/A'),
                "total": odds.get('overUnder', 'N/A')
            }
        except (IndexError, ValueError, TypeError):
            print("⚠️  Warning: Could not retrieve odds data")
            return {
                "spread_home": "N/A",
                "spread_away": "N/A",
                "total": "N/A"
            }

    async def analyze_depth_charts(self, home_team: str, away_team: str) -> str:
        """Prompt 1: Analyze team depth charts"""
        print("\nAnalyzing depth charts...")
        tasks = [
            self.get_data("depthchart", {"team": home_team}),
            self.get_data("depthchart", {"team": away_team})
        ]
        
        home_depth, away_depth = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_1"].format(
            home_team=home_team,
            away_team=away_team,
            home_depth=json.dumps(home_depth, indent=2),
            away_depth=json.dumps(away_depth, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_weather_injuries(self, home_team: str, away_team: str) -> str:
        """Prompt 2: Analyze weather and injuries"""
        print("\nAnalyzing weather and injuries...")
        tasks = [
            self.get_data("weather", {}),
            self.get_data("injuryreports", {"team": home_team}),
            self.get_data("injuryreports", {"team": away_team})
        ]
        
        weather, home_injuries, away_injuries = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_2"].format(
            home_team=home_team,
            away_team=away_team,
            weather=json.dumps(weather, indent=2),
            home_injuries=json.dumps(home_injuries, indent=2),
            away_injuries=json.dumps(away_injuries, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_team_performance(self, team: str, period: str, is_home: bool) -> str:
        """Prompts 3-6: Analyze team performance"""
        print(f"\nAnalyzing {period} performance for {team}...")
        tasks = [
            self.get_data("playerstats", {
                "team": team,
                "view": view,
                "split": period
            }) for view in ["Passing", "Rushing", "Receiving"]
        ]
        
        passing, rushing, receiving = await asyncio.gather(*tasks)
        prompt_num = "3" if is_home and period == "Last 4 Weeks" else \
                    "4" if is_home and period == "Last 2 Weeks" else \
                    "5" if not is_home and period == "Last 4 Weeks" else "6"
        
        prompt = self.prompts[f"prompt_{prompt_num}"].format(
            team=team,
            passing=json.dumps(passing, indent=2),
            rushing=json.dumps(rushing, indent=2),
            receiving=json.dumps(receiving, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_defense(self, team: str, is_home: bool) -> str:
        """Prompts 7-8: Analyze defensive performance"""
        print(f"\nAnalyzing defensive performance for {team}...")
        tasks = [
            self.get_data("playerstats", {
                "team": team,
                "view": "Defensive",
                "split": period
            }) for period in ["Last 2 Weeks", "Last 4 Weeks"]
        ]
        
        defense_2wk, defense_4wk = await asyncio.gather(*tasks)
        prompt_num = "7" if is_home else "8"
        
        prompt = self.prompts[f"prompt_{prompt_num}"].format(
            team=team,
            defense_2wk=json.dumps(defense_2wk, indent=2),
            defense_4wk=json.dumps(defense_4wk, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_team_defense(self, home_team: str, away_team: str) -> str:
        """Prompt 9: Analyze team defense statistics"""
        print("\nAnalyzing team defense statistics...")
        tasks = [
            self.get_data("teamdefense", {"team": home_team}),
            self.get_data("teamdefense", {"team": away_team})
        ]
        
        home_defense, away_defense = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_9"].format(
            home_team=home_team,
            away_team=away_team,
            home_defense=json.dumps(home_defense, indent=2),
            away_defense=json.dumps(away_defense, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_pass_pressure(self, home_team: str, away_team: str) -> str:
        """Prompt 10: Analyze pass rushing and missed tackles"""
        print("\nAnalyzing pass rushing and missed tackles...")
        tasks = [
            self.get_data("teamdefense", {"team": home_team}),
            self.get_data("teamdefense", {"team": away_team})
        ]
        
        home_pressure, away_pressure = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_10"].format(
            home_team=home_team,
            away_team=away_team,
            home_pressure=json.dumps(home_pressure, indent=2),
            away_pressure=json.dumps(away_pressure, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_team_stats(self, home_team: str, away_team: str) -> str:
        """Prompt 11: Analyze penalties, third down, red zone"""
        print("\nAnalyzing team statistics...")
        tasks = [
            self.get_data("teamstats/team", {"team": home_team}),
            self.get_data("teamstats/team", {"team": away_team})
        ]
        
        home_stats, away_stats = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_11"].format(
            home_team=home_team,
            away_team=away_team,
            home_stats=json.dumps(home_stats, indent=2),
            away_stats=json.dumps(away_stats, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_pass_protection(self, home_team: str, away_team: str) -> str:
        """Prompt 12: Analyze pass protection and scramble"""
        print("\nAnalyzing pass protection and scramble statistics...")
        tasks = [
            self.get_data("teampasspressure", {"team": home_team}),
            self.get_data("teampasspressure", {"team": away_team})
        ]
        
        home_protection, away_protection = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_12"].format(
            home_team=home_team,
            away_team=away_team,
            home_protection=json.dumps(home_protection, indent=2),
            away_protection=json.dumps(away_protection, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def analyze_game_logs(self, home_team: str, away_team: str) -> str:
        """Prompt 13: Analyze game logs"""
        print("\nAnalyzing game logs...")
        tasks = [
            self.get_data("gamelogs", {"team": home_team}),
            self.get_data("gamelogs", {"team": away_team}),
            self.get_data("oppgamelogs", {"team": home_team}),
            self.get_data("oppgamelogs", {"team": away_team})
        ]
        
        home_logs, away_logs, home_opp, away_opp = await asyncio.gather(*tasks)
        prompt = self.prompts["prompt_13"].format(
            home_team=home_team,
            away_team=away_team,
            home_logs=json.dumps(home_logs, indent=2),
            away_logs=json.dumps(away_logs, indent=2),
            home_opp=json.dumps(home_opp, indent=2),
            away_opp=json.dumps(away_opp, indent=2)
        )
        
        return await self.get_llama_response(prompt)

    async def get_llama_response(self, prompt: str) -> str:
        """Get response from Ollama"""
        response = requests.post(self.ollama_url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **self.model_params
        })
        return response.json()['response']

    async def get_final_recommendation(self, analyses: Dict[str, str], game_data: Dict) -> str:
        """Prompt 14: Generate final betting recommendations"""
        try:
            home_team = game_data['competitions'][0]['competitors'][0]['team']['displayName']
            away_team = game_data['competitions'][0]['competitors'][1]['team']['displayName']
            venue = game_data['competitions'][0]['venue']['fullName']
            date = game_data['date']
            
            # Get odds data
            odds = await self.get_game_odds(game_data)
            
            # Create the game info section as it appears in the prompt
            game_info = f"""## Game Information
{home_team} vs {away_team}
Spread: {home_team} {odds['spread_home']}, {away_team} {odds['spread_away']}
Game Total: {odds['total']}
Venue: {venue}
Date: {date}"""
            
            # Format the prompt with game info and analyses
            prompt = self.prompts["prompt_14"].format(
                game_info=game_info,
                analyses=json.dumps(analyses, indent=2)
            )
            
            return await self.get_llama_response(prompt)
        except Exception as e:
            print(f"Error in get_final_recommendation: {str(e)}")
            raise

    async def analyze_game(self, game_data: Dict) -> Dict[str, str]:
        """Run complete game analysis"""
        home_team = game_data['competitions'][0]['competitors'][0]['team']['displayName']
        away_team = game_data['competitions'][0]['competitors'][1]['team']['displayName']
        
        analyses = {}
        
        # Run all analyses
        analyses['depth_charts'] = await self.analyze_depth_charts(home_team, away_team)
        analyses['weather_injuries'] = await self.analyze_weather_injuries(home_team, away_team)
        
        # Team performance analyses
        for period in ["Last 4 Weeks", "Last 2 Weeks"]:
            analyses[f'home_{period.lower().replace(" ", "_")}'] = \
                await self.analyze_team_performance(home_team, period, True)
            analyses[f'away_{period.lower().replace(" ", "_")}'] = \
                await self.analyze_team_performance(away_team, period, False)
        
        # Defense analyses
        analyses['home_defense'] = await self.analyze_defense(home_team, True)
        analyses['away_defense'] = await self.analyze_defense(away_team, False)
        
        # Additional analyses
        analyses['team_defense'] = await self.analyze_team_defense(home_team, away_team)
        analyses['pass_pressure'] = await self.analyze_pass_pressure(home_team, away_team)
        analyses['team_stats'] = await self.analyze_team_stats(home_team, away_team)
        analyses['pass_protection'] = await self.analyze_pass_protection(home_team, away_team)
        analyses['game_logs'] = await self.analyze_game_logs(home_team, away_team)
        
        # Final recommendations
        analyses['final_recommendation'] = await self.get_final_recommendation(
            analyses, game_data
        )
        
        return analyses

async def main():
    print("\n🏈 NFL Game Analyzer 🏈")
    print("=======================")
    
    analyzer = NFLAnalyzer()
    
    # Get available weeks
    weeks = await analyzer.get_weeks()
    print("\nAvailable Weeks:")
    for week in weeks:
        print(f"{week}. Week {week}")
    
    # Get week selection
    while True:
        try:
            week = int(input("\nEnter week number (1-18): "))
            if 1 <= week <= 18:
                break
            print("Please enter a valid week number (1-18)")
        except ValueError:
            print("Please enter a valid number")
    
    # Get games for selected week
    games = await analyzer.get_games(week)
    print("\nAvailable Games:")
    for i, game in enumerate(games, 1):
        home_team = game['competitions'][0]['competitors'][0]['team']['displayName']
        away_team = game['competitions'][0]['competitors'][1]['team']['displayName']
        print(f"{i}. {away_team} @ {home_team}")
    
    # Get game selection
    while True:
        try:
            game_num = int(input("\nEnter game number: "))
            if 1 <= game_num <= len(games):
                selected_game = games[game_num - 1]
                break
            print(f"Please enter a valid game number (1-{len(games)})")
        except ValueError:
            print("Please enter a valid number")
    
    try:
        print(f"\nStarting comprehensive analysis...")
        analyses = await analyzer.analyze_game(selected_game)
        
        print("\n📊 Final Betting Recommendations:")
        print("================================")
        print(analyses['final_recommendation'])
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Please try again or contact support if the issue persists.")

if __name__ == "__main__":
    asyncio.run(main())
