import asyncio
import json
import os
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime
from pathlib import Path
import requests
from .api_client import NFLApiClient
from .data_processor import NFLDataProcessor, GameContext
from .odds_fetcher import NFLOddsFetcher

class NFLAnalyzer:
    """Enhanced NFL game analyzer with sequential prompt handling"""
    
    def __init__(self):
        self.api_client = NFLApiClient()
        self.data_processor = NFLDataProcessor()
        self.odds_fetcher = NFLOddsFetcher()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "command-r:latest"  # Changed to more common model name
        self.model_params = {
            "context_length": 131072,
            "num_ctx": 131072,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["</analysis>"],
         #   "raw": True,  # Ensure raw mode for clean context
            "session_key": None  # Will be regenerated for each call
        }
        
        # Verify Ollama is running and model exists
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                if self.model not in models:
                    print(f"⚠️ Warning: Model {self.model} not found. Available models: {', '.join(models)}")
            else:
                print("⚠️ Warning: Could not connect to Ollama service")
        except Exception as e:
            print(f"⚠️ Warning: Could not verify Ollama models: {str(e)}")
        
        # Load prompts from data directory
        try:
            prompt_path = Path('data/nfl_prompts.json')
            with open(prompt_path, 'r') as f:
                self.prompt_templates = json.load(f)
            print("✓ Loaded prompt templates")
        except Exception as e:
            print(f"❌ Error loading prompts from {prompt_path}: {str(e)}")
            raise

    async def get_llm_response(self, prompt: str, context: GameContext) -> str:
        """Get analysis from local LLM with enhanced debugging and fresh context"""
        system_context = (
            f"You are analyzing NFL game: {context.away_team} @ {context.home_team}\n"
            f"Venue: {context.venue}\nDate: {context.date}\n"
            "Provide specific, data-driven analysis based only on the statistics provided.\n"
            "Focus on clear, actionable insights supported by the data.\n"
            "When discussing betting implications, provide specific reasoning based on the data."
        )
        
        # Generate new session key for fresh context
        self.model_params['session_key'] = f"nfl_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Debug: Print what we're sending to the LLM
        print("\n=== LLM Request Debug ===")
        print(f"Sending request to: {self.ollama_url}")
        print(f"Model: {self.model}")
        print(f"Session Key: {self.model_params['session_key']}")
        print("System Context:")
        print(system_context)
        print("\nPrompt:")
        print(prompt)
        print("=== End Request Debug ===\n")
        
        # Add delay between LLM calls to prevent overwhelming
        await asyncio.sleep(1)
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system_context,
                    "stream": False,
                    **self.model_params
                },
                timeout=3000
            )
            
            # Debug: Print raw response
            print("\n=== LLM Response Debug ===")
            print(f"Status Code: {response.status_code}")
            print("Raw Response:")
            print(response.text)
            print("=== End Response Debug ===\n")
            
            response.raise_for_status()
            llm_response = response.json()['response']
            
            # Debug: Print processed response
            print("\n=== Processed Response ===")
            print(llm_response)
            print("=== End Processed Response ===\n")
            
            return llm_response
            
        except requests.exceptions.ConnectionError:
            error_msg = "Error: Cannot connect to LLM. Is Ollama running on port 11434?"
            print(f"\n❌ {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"Error getting LLM response: {str(e)}"
            print(f"\n❌ {error_msg}")
            return error_msg

    async def analyze_game(self, game_data: Dict, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """Analyze single game sequentially through all prompts"""
        try:
            # Initialize game context
            context = GameContext(
                game_id=game_data['id'],
                home_team=game_data['competitions'][0]['competitors'][0]['team']['displayName'],
                away_team=game_data['competitions'][0]['competitors'][1]['team']['displayName'],
                venue=game_data['competitions'][0]['venue']['fullName'],
                date=game_data['date']
            )
            
            if progress_callback:
                progress_callback(f"Starting analysis: {context.away_team} @ {context.home_team}")
                
            # Initialize results dictionary
            analyses = {}
            
            # 1. Depth Charts Analysis
            if progress_callback:
                progress_callback("Analyzing depth charts...")
            home_depth = await self.api_client.get_depth_chart(context.home_team)
            away_depth = await self.api_client.get_depth_chart(context.away_team)
            prompt = self.prompt_templates["prompt_1"].format(
                home_team=context.home_team,
                away_team=context.away_team,
                home_depth=json.dumps(home_depth, indent=2),
                away_depth=json.dumps(away_depth, indent=2),
                venue=context.venue
            )
            analyses['depth_charts'] = await self.get_llm_response(prompt, context)

            # 2. Weather and Injuries Analysis
            if progress_callback:
                progress_callback("Analyzing weather and injuries...")
            weather = await self.api_client.get_weather()
            home_injuries = await self.api_client.get_injuries(context.home_team)
            away_injuries = await self.api_client.get_injuries(context.away_team)
            prompt = self.prompt_templates["prompt_2"].format(
                weather=json.dumps(weather, indent=2),
                home_team=context.home_team,
                away_team=context.away_team,
                home_injuries=json.dumps(home_injuries, indent=2),
                away_injuries=json.dumps(away_injuries, indent=2)
            )
            analyses['weather_injuries'] = await self.get_llm_response(prompt, context)

            # 3. Home Team 4-Week Performance
            if progress_callback:
                progress_callback("Analyzing home team 4-week performance...")
            home_passing = await self.api_client.get_player_stats(context.home_team, "passing", "Last 4 Weeks")
            home_rushing = await self.api_client.get_player_stats(context.home_team, "rushing", "Last 4 Weeks")
            home_receiving = await self.api_client.get_player_stats(context.home_team, "receiving", "Last 4 Weeks")
            prompt = self.prompt_templates["prompt_3"].format(
                home_team=context.home_team,  # Fixed parameter name
                passing=json.dumps(home_passing, indent=2),
                rushing=json.dumps(home_rushing, indent=2),
                receiving=json.dumps(home_receiving, indent=2)
            )
            analyses['home_4_weeks'] = await self.get_llm_response(prompt, context)

            # 4. Home Team 2-Week Performance
            if progress_callback:
                progress_callback("Analyzing home team 2-week performance...")
            home_passing_2wk = await self.api_client.get_player_stats(context.home_team, "passing", "Last 2 Weeks")
            home_rushing_2wk = await self.api_client.get_player_stats(context.home_team, "rushing", "Last 2 Weeks")
            home_receiving_2wk = await self.api_client.get_player_stats(context.home_team, "receiving", "Last 2 Weeks")
            prompt = self.prompt_templates["prompt_4"].format(
                home_team=context.home_team,  # Fixed parameter name
                passing=json.dumps(home_passing_2wk, indent=2),
                rushing=json.dumps(home_rushing_2wk, indent=2),
                receiving=json.dumps(home_receiving_2wk, indent=2)
            )
            analyses['home_2_weeks'] = await self.get_llm_response(prompt, context)

            # 5. Away Team 4-Week Performance
            if progress_callback:
                progress_callback("Analyzing away team 4-week performance...")
            away_passing = await self.api_client.get_player_stats(context.away_team, "passing", "Last 4 Weeks")
            away_rushing = await self.api_client.get_player_stats(context.away_team, "rushing", "Last 4 Weeks")
            away_receiving = await self.api_client.get_player_stats(context.away_team, "receiving", "Last 4 Weeks")
            prompt = self.prompt_templates["prompt_5"].format(
                away_team=context.away_team,  # Fixed parameter name
                passing=json.dumps(away_passing, indent=2),
                rushing=json.dumps(away_rushing, indent=2),
                receiving=json.dumps(away_receiving, indent=2)
            )
            analyses['away_4_weeks'] = await self.get_llm_response(prompt, context)

            # 6. Away Team 2-Week Performance
            if progress_callback:
                progress_callback("Analyzing away team 2-week performance...")
            away_passing_2wk = await self.api_client.get_player_stats(context.away_team, "passing", "Last 2 Weeks")
            away_rushing_2wk = await self.api_client.get_player_stats(context.away_team, "rushing", "Last 2 Weeks")
            away_receiving_2wk = await self.api_client.get_player_stats(context.away_team, "receiving", "Last 2 Weeks")
            prompt = self.prompt_templates["prompt_6"].format(
                away_team=context.away_team,  # Fixed parameter name
                passing=json.dumps(away_passing_2wk, indent=2),
                rushing=json.dumps(away_rushing_2wk, indent=2),
                receiving=json.dumps(away_receiving_2wk, indent=2)
            )
            analyses['away_2_weeks'] = await self.get_llm_response(prompt, context)

            # 7. Home Team Defense
            if progress_callback:
                progress_callback("Analyzing home team defense...")
            home_defense = await self.api_client.get_team_defense(context.home_team)
            prompt = self.prompt_templates["prompt_7"].format(
                home_team=context.home_team,  # Fixed parameter name
                defense_2wk=json.dumps(home_defense, indent=2),  # Use same data for both timeframes
                defense_4wk=json.dumps(home_defense, indent=2)   # since API doesn't support timeframes
            )
            analyses['home_defense'] = await self.get_llm_response(prompt, context)

            # 8. Away Team Defense
            if progress_callback:
                progress_callback("Analyzing away team defense...")
            away_defense = await self.api_client.get_team_defense(context.away_team)
            prompt = self.prompt_templates["prompt_8"].format(
                away_team=context.away_team,  # Fixed parameter name
                defense_2wk=json.dumps(away_defense, indent=2),  # Use same data for both timeframes
                defense_4wk=json.dumps(away_defense, indent=2)   # since API doesn't support timeframes
            )
            analyses['away_defense'] = await self.get_llm_response(prompt, context)

            # 9. Defense Comparison
            if progress_callback:
                progress_callback("Analyzing team defense comparison...")
            prompt = self.prompt_templates["prompt_9"].format(
                home_team=context.home_team,
                away_team=context.away_team,
                home_defense=json.dumps(home_defense, indent=2),  # Reuse defense data from above
                away_defense=json.dumps(away_defense, indent=2)   # Reuse defense data from above
            )
            analyses['defense_comparison'] = await self.get_llm_response(prompt, context)

            # 10. Pass Rush Analysis
            if progress_callback:
                progress_callback("Analyzing pass rush...")
            home_pressure = await self.api_client.get_pass_pressure(context.home_team)
            away_pressure = await self.api_client.get_pass_pressure(context.away_team)
            prompt = self.prompt_templates["prompt_10"].format(
                home_team=context.home_team,
                away_team=context.away_team,
                home_pressure=json.dumps(home_pressure, indent=2),
                away_pressure=json.dumps(away_pressure, indent=2)
            )
            analyses['pass_rush'] = await self.get_llm_response(prompt, context)

            # 11. Team Stats Analysis
            if progress_callback:
                progress_callback("Analyzing team stats...")
            home_stats = await self.api_client.get_team_stats(context.home_team)
            away_stats = await self.api_client.get_team_stats(context.away_team)
            prompt = self.prompt_templates["prompt_11"].format(
                home_team=context.home_team,
                away_team=context.away_team,
                home_stats=json.dumps(home_stats, indent=2),
                away_stats=json.dumps(away_stats, indent=2)
            )
            analyses['team_stats'] = await self.get_llm_response(prompt, context)

            # 12. Pass Protection Analysis
            if progress_callback:
                progress_callback("Analyzing pass protection...")
            prompt = self.prompt_templates["prompt_12"].format(
                home_team=context.home_team,
                away_team=context.away_team,
                home_protection=json.dumps(home_pressure, indent=2),  # Reuse pressure data from above
                away_protection=json.dumps(away_pressure, indent=2)   # Reuse pressure data from above
            )
            analyses['pass_protection'] = await self.get_llm_response(prompt, context)

            # 13. Game Logs Analysis
            if progress_callback:
                progress_callback("Analyzing game logs...")
            home_logs = await self.api_client.get_game_logs(context.home_team)
            away_logs = await self.api_client.get_game_logs(context.away_team)
            home_opp = await self.api_client.get_opponent_logs(context.home_team)
            away_opp = await self.api_client.get_opponent_logs(context.away_team)
            prompt = self.prompt_templates["prompt_13"].format(
                home_team=context.home_team,
                away_team=context.away_team,
                home_logs=json.dumps(home_logs, indent=2),
                away_logs=json.dumps(away_logs, indent=2),
                home_opp=json.dumps(home_opp, indent=2),
                away_opp=json.dumps(away_opp, indent=2)
            )
            analyses['game_logs'] = await self.get_llm_response(prompt, context)

            # 14. Final Analysis
            if progress_callback:
                progress_callback("Generating final analysis...")
            odds = await self.api_client.get_odds(context.game_id)
            game_info = {
                "id": context.game_id,
                "home_team": context.home_team,
                "away_team": context.away_team,
                "venue": context.venue,
                "date": context.date,
                "odds": odds
            }
            prompt = self.prompt_templates["prompt_14"].format(
                game_info=json.dumps(game_info, indent=2),
                analyses=json.dumps(analyses, indent=2)
            )
            analyses['final_analysis'] = await self.get_llm_response(prompt, context)

            return analyses

        except Exception as e:
            error_msg = f"Error in game analysis: {str(e)}"
            print(error_msg)
            return {"error": error_msg}

    async def analyze_week(self, week: int, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Analyze all games for a specific week sequentially"""
        analyzed_games = []
        
        # Create weekly directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        week_dir = f"Week_{week}_{timestamp}"
        os.makedirs(week_dir, exist_ok=True)
        
        # Get games for the week
        games = await self.api_client.get_games(week)
        total_games = len(games)
        
        if progress_callback:
            progress_callback(f"Found {total_games} games for Week {week}")
        
        # Process each game sequentially
        for i, game in enumerate(games, 1):
            try:
                if progress_callback:
                    progress_callback(f"\nStarting analysis of game {i}/{total_games}:")
                    progress_callback(f"{game['competitions'][0]['competitors'][1]['team']['displayName']} @ "
                                   f"{game['competitions'][0]['competitors'][0]['team']['displayName']}")
                
                # Analyze one game at a time
                analyses = await self.analyze_game(game, progress_callback)
                
                # Save analysis to file
                filename = (
                    f"{week_dir}/{game['competitions'][0]['competitors'][0]['team']['displayName']}"
                    f"_vs_{game['competitions'][0]['competitors'][1]['team']['displayName']}.json"
                )
                
                with open(filename, 'w') as f:
                    json.dump(analyses, f, indent=2)
                
                analyzed_games.append({
                    "game_id": game['id'],
                    "home_team": game['competitions'][0]['competitors'][0]['team']['displayName'],
                    "away_team": game['competitions'][0]['competitors'][1]['team']['displayName'],
                    "analyses": analyses,
                    "file": filename
                })
                
                if progress_callback:
                    progress_callback(f"✓ Completed game {i}/{total_games} - Analysis saved to: {filename}")
                    progress_callback("----------------------------------------")
                
                # Add delay between games to avoid overwhelming the LLM
                await asyncio.sleep(2)
                
            except Exception as e:
                error_msg = f"❌ Error analyzing game {i}/{total_games}: {str(e)}"
                print(error_msg)
                if progress_callback:
                    progress_callback(error_msg)
                continue
        
        return analyzed_games