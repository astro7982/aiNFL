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
    """Enhanced NFL game analyzer with complete prompt handling"""
    
    def __init__(self):
        self.api_client = NFLApiClient()
        self.data_processor = NFLDataProcessor()
        self.odds_fetcher = NFLOddsFetcher()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"
        self.model_params = {
            "context_length": 4096,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["</analysis>"]
        }
        
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
        """Get analysis from local LLM with enhanced context"""
        system_context = (
            f"You are analyzing NFL game: {context.home_team} vs {context.away_team}\n"
            f"Venue: {context.venue}\nDate: {context.date}\n"
            "Provide specific, data-driven analysis based only on the statistics provided.\n"
            "Focus on clear, actionable insights supported by the data.\n"
            "When discussing betting implications, provide specific reasoning based on the data."
        )
        
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
                timeout=30
            )
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            print(f"Error getting LLM response: {str(e)}")
            return "Error: Unable to get analysis"

    async def analyze_game(self, game_data: Dict, progress_callback: Optional[Callable] = None) -> Dict[str, str]:
        """Complete game analysis with all 14 prompts"""
        try:
            # Initialize game context
            game_context = GameContext(
                game_id=game_data['id'],
                home_team=game_data['competitions'][0]['competitors'][0]['team']['displayName'],
                away_team=game_data['competitions'][0]['competitors'][1]['team']['displayName'],
                venue=game_data['competitions'][0]['venue']['fullName'],
                date=game_data['date']
            )

            # Fetch all required data
            if progress_callback:
                progress_callback("Fetching game data...")
            raw_data = await self.api_client.fetch_all_game_data(game_data)
            
            # Process all data
            processed_data = self.data_processor.combine_analysis_data(raw_data, game_context)
            analyses = {}

            # Run analyses with progress tracking
            analysis_steps = [
                ("Analyzing depth charts...", self._analyze_depth_charts),
                ("Analyzing weather and injuries...", self._analyze_weather_injuries),
                ("Analyzing home team 4-week performance...", 
                 lambda d, c: self._analyze_team_performance(d, 'home', 'Last 4 Weeks', c)),
                ("Analyzing home team 2-week performance...", 
                 lambda d, c: self._analyze_team_performance(d, 'home', 'Last 2 Weeks', c)),
                ("Analyzing away team 4-week performance...", 
                 lambda d, c: self._analyze_team_performance(d, 'away', 'Last 4 Weeks', c)),
                ("Analyzing away team 2-week performance...", 
                 lambda d, c: self._analyze_team_performance(d, 'away', 'Last 2 Weeks', c)),
                ("Analyzing home team defense...", 
                 lambda d, c: self._analyze_team_defense(d, 'home', c)),
                ("Analyzing away team defense...", 
                 lambda d, c: self._analyze_team_defense(d, 'away', c)),
                ("Analyzing team defense comparison...", self._analyze_defense_comparison),
                ("Analyzing pass rush...", self._analyze_pass_rush),
                ("Analyzing team stats...", self._analyze_team_stats),
                ("Analyzing pass protection...", self._analyze_pass_protection),
                ("Analyzing game logs...", self._analyze_game_logs),
                ("Generating final analysis...", 
                 lambda d, c: self._generate_final_analysis(d, analyses, c))
            ]

            for step_message, analysis_func in analysis_steps:
                if progress_callback:
                    progress_callback(step_message)
                    
                key = step_message.replace("Analyzing ", "").replace("Generating ", "").replace("...", "")
                key = key.lower().replace(" ", "_")
                analyses[key] = await analysis_func(processed_data, game_context)

            return analyses
            
        except Exception as e:
            error_msg = f"Error in game analysis: {str(e)}"
            print(error_msg)
            return {"error": error_msg}

    async def _analyze_depth_charts(self, data: Dict, context: GameContext) -> str:
        """Prompt 1: Depth chart analysis"""
        prompt = self.prompt_templates["prompt_1"].format(
            home_team=context.home_team,
            away_team=context.away_team,
            home_depth=json.dumps(data["depth_charts"]["home"], indent=2),
            away_depth=json.dumps(data["depth_charts"]["away"], indent=2),
            venue=context.venue
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_weather_injuries(self, data: Dict, context: GameContext) -> str:
        """Prompt 2: Weather and injuries analysis"""
        prompt = self.prompt_templates["prompt_2"].format(
            weather=json.dumps(data["game_info"]["weather"], indent=2),
            home_team=context.home_team,
            away_team=context.away_team,
            home_injuries=json.dumps(data["injuries"]["home"], indent=2),
            away_injuries=json.dumps(data["injuries"]["away"], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_team_performance(
        self, data: Dict, team_type: str, timeframe: str, context: GameContext
    ) -> str:
        """Prompts 3-6: Team performance analysis"""
        prompt_num = {
            ('home', 'Last 4 Weeks'): "prompt_3",
            ('home', 'Last 2 Weeks'): "prompt_4",
            ('away', 'Last 4 Weeks'): "prompt_5",
            ('away', 'Last 2 Weeks'): "prompt_6"
        }[(team_type, timeframe)]
        
        team = context.home_team if team_type == 'home' else context.away_team

        # Map timeframe to data structure key
        stats_key = "2_weeks" if timeframe == "Last 2 Weeks" else "4_weeks"
        
        prompt = self.prompt_templates[prompt_num].format(
            team=team,
            passing=json.dumps(data["player_stats"][team_type]["passing"][stats_key], indent=2),
            rushing=json.dumps(data["player_stats"][team_type]["rushing"][stats_key], indent=2),
            receiving=json.dumps(data["player_stats"][team_type]["receiving"][stats_key], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_team_defense(
        self, data: Dict, team_type: str, context: GameContext
    ) -> str:
        """Prompts 7-8: Team defense analysis"""
        prompt_num = "prompt_7" if team_type == 'home' else "prompt_8"
        team = context.home_team if team_type == 'home' else context.away_team
        
        prompt = self.prompt_templates[prompt_num].format(
            team=team,
            defense_2wk=json.dumps(data["player_stats"][team_type]["defense"]["2_weeks"], indent=2),
            defense_4wk=json.dumps(data["player_stats"][team_type]["defense"]["4_weeks"], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_defense_comparison(self, data: Dict, context: GameContext) -> str:
        """Prompt 9: Defense comparison"""
        prompt = self.prompt_templates["prompt_9"].format(
            home_team=context.home_team,
            away_team=context.away_team,
            home_defense=json.dumps(data["defense"]["home"], indent=2),
            away_defense=json.dumps(data["defense"]["away"], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_pass_rush(self, data: Dict, context: GameContext) -> str:
        """Prompt 10: Pass rush analysis"""
        prompt = self.prompt_templates["prompt_10"].format(
            home_team=context.home_team,
            away_team=context.away_team,
            home_pressure=json.dumps(data["pressure"]["home"], indent=2),
            away_pressure=json.dumps(data["pressure"]["away"], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_team_stats(self, data: Dict, context: GameContext) -> str:
        """Prompt 11: Team stats analysis"""
        prompt = self.prompt_templates["prompt_11"].format(
            home_team=context.home_team,
            away_team=context.away_team,
            home_stats=json.dumps(data["team_stats"]["home"], indent=2),
            away_stats=json.dumps(data["team_stats"]["away"], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_pass_protection(self, data: Dict, context: GameContext) -> str:
        """Prompt 12: Pass protection analysis"""
        prompt = self.prompt_templates["prompt_12"].format(
            home_team=context.home_team,
            away_team=context.away_team,
            home_protection=json.dumps(data["pressure"]["home"], indent=2),  # Using pressure data
            away_protection=json.dumps(data["pressure"]["away"], indent=2)   # Using pressure data
        )
        return await self.get_llm_response(prompt, context)

    async def _analyze_game_logs(self, data: Dict, context: GameContext) -> str:
        """Prompt 13: Game logs analysis"""
        prompt = self.prompt_templates["prompt_13"].format(
            home_team=context.home_team,
            away_team=context.away_team,
            home_logs=json.dumps(data["game_logs"]["home"], indent=2),
            away_logs=json.dumps(data["game_logs"]["away"], indent=2),
            home_opp=json.dumps(data["opponent_logs"]["home"], indent=2),
            away_opp=json.dumps(data["opponent_logs"]["away"], indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def _generate_final_analysis(
        self, data: Dict, analyses: Dict[str, str], context: GameContext
    ) -> str:
        """Prompt 14: Final comprehensive analysis"""
        prompt = self.prompt_templates["prompt_14"].format(
            game_info=json.dumps(data["game_info"], indent=2),
            analyses=json.dumps(analyses, indent=2)
        )
        return await self.get_llm_response(prompt, context)

    async def analyze_week(self, week: int, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Analyze all games for a specific week"""
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
        
        # Analyze each game
        for i, game in enumerate(games, 1):
            try:
                if progress_callback:
                    progress_callback(f"Analyzing game {i}/{total_games}...")
                
                analyses = await self.analyze_game(game, progress_callback)
                
                # Save analysis to file
                filename = (
                    f"{week_dir}/{game['competitions'][0]['competitors'][0]['team']['displayName']}"
                    f"_vs_{game['competitions'][0]['competitors'][1]['team']['displayName']}.json"
                )
                
                with open(filename, 'w') as f:
                    json.dump(analyses, f, indent=2)  # Fixed from json.dumps to json.dump
                
                analyzed_games.append({
                    "game_id": game['id'],
                    "home_team": game['competitions'][0]['competitors'][0]['team']['displayName'],
                    "away_team": game['competitions'][0]['competitors'][1]['team']['displayName'],
                    "analyses": analyses,
                    "file": filename
                })
                
                if progress_callback:
                    progress_callback(f"✓ Analysis saved: {filename}")
                
            except Exception as e:
                error_msg = f"❌ Error analyzing game: {str(e)}"
                print(error_msg)
                if progress_callback:
                    progress_callback(error_msg)
                continue
        
        return analyzed_games