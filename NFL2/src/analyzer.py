"""
Enhanced NFL Analyzer module - Main orchestrator for NFL game analysis
"""
import aiohttp
import asyncio
import json
import time
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .data_processor import NFLDataProcessor
from .data_validator import NFLDataValidator
from .statistics_analyzer import NFLStatisticsAnalyzer

class EnhancedNFLAnalyzer:
    def __init__(self):
        print("\nInitializing Enhanced NFL Analyzer...")
        self.data_processor = NFLDataProcessor()
        self.data_validator = NFLDataValidator()
        self.stats_analyzer = NFLStatisticsAnalyzer()
        
        # API configuration
        self.api_base = "https://sportsstatsgather.com/api/nfl/data"
        self.espn_api = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Model configuration
        self.model = "llama3.2"
        self.model_params = {
            "context_length": 65536,
            "num_ctx": 65536,
            "num_gpu": 1,
            "num_thread": 4,
            "gpu_layers": 35
        }
        
        # Load configurations
        self.config = self._load_config()
        self.prompts = self._load_prompts()
        self.data_contexts = self._load_data_contexts()

    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(Path('config/config.json'), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            raise

    def _load_prompts(self) -> Dict:
        """Load enhanced prompts from file"""
        try:
            with open(Path('config/enhanced_prompts.json'), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading prompts: {e}")
            raise

    def _load_data_contexts(self) -> Dict:
        """Load data contexts from file"""
        try:
            with open(Path('config/data_contexts.json'), 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data contexts: {e}")
            raise

    async def get_data(self, endpoint: str, params: dict = None) -> Dict:
        """Enhanced data retrieval with validation"""
        url = f"{self.api_base}/{endpoint}"
        print(f"Fetching data from: {url}")
        print(f"Parameters: {params}")
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"API returned status code {response.status}")
                        
                    data = await response.json()
                    
                    # Validate data
                    valid, message = self.data_validator.validate_api_response(data, endpoint)
                    if not valid:
                        raise Exception(f"Data validation failed: {message}")
                        
                    return data
                    
            except Exception as e:
                print(f"Error fetching data from {endpoint}: {str(e)}")
                raise

    async def get_llama_response(self, prompt_template: str, data: Dict, context: Dict) -> str:
        """Enhanced LLM interaction with better context"""
        try:
            # Create enhanced system context
            system_context = {
                "role": "NFL Analysis System",
                "game_context": context,
                "data_structure": self.data_contexts.get(context.get('data_type', ''), {}),
                "analysis_requirements": self.config.get('analysis_requirements', {})
            }

            # Format prompt with all necessary context
            formatted_prompt = prompt_template.format(
                game_context=json.dumps(context, indent=2),
                data_structure=json.dumps(system_context['data_structure'], indent=2),
                data=json.dumps(data, indent=2)
            )

            # Make request to Ollama
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: requests.post(
                    self.ollama_url,
                    json={
                        "model": self.model,
                        "prompt": formatted_prompt,
                        "system": json.dumps(system_context),
                        "stream": False,
                        "context": [],
                        **self.model_params
                    }
                )
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API returned status code {response.status_code}")

            return response.json()['response']

        except Exception as e:
            print(f"Error getting LLM response: {str(e)}")
            raise

    async def analyze_depth_charts(self, context: Dict) -> str:
        """Enhanced depth chart analysis"""
        print("\nAnalyzing depth charts...")
        
        tasks = [
            self.get_data("depthchart", {"team": context['home_team']}),
            self.get_data("depthchart", {"team": context['away_team']})
        ]
        
        home_depth, away_depth = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'home_depth': self.data_processor.process_depth_chart(home_depth),
            'away_depth': self.data_processor.process_depth_chart(away_depth)
        }
        
        # Get analysis from LLM
        analysis = await self.get_llama_response(
            self.prompts["depth_charts"]["template"],
            processed_data,
            {**context, 'data_type': 'depth_chart'}
        )
        
        return analysis

    async def analyze_weather_injuries(self, context: Dict) -> str:
        """Enhanced weather and injuries analysis"""
        print("\nAnalyzing weather and injuries...")
        
        tasks = [
            self.get_data("weather", {}),
            self.get_data("injuryreports", {"team": context['home_team']}),
            self.get_data("injuryreports", {"team": context['away_team']})
        ]
        
        weather, home_injuries, away_injuries = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'weather': self.data_processor.process_weather(weather),
            'home_injuries': self.data_processor.process_injuries(home_injuries),
            'away_injuries': self.data_processor.process_injuries(away_injuries)
        }
        
        # Get analysis
        analysis = await self.get_llama_response(
            self.prompts["weather_injuries"]["template"],
            processed_data,
            {**context, 'data_type': 'weather_injuries'}
        )
        
        return analysis

    async def analyze_team_performance(self, team: str, period: str, is_home: bool, context: Dict) -> str:
        """Enhanced team performance analysis"""
        print(f"\nAnalyzing {period} performance for {team}...")
        
        tasks = [
            self.get_data("playerstats", {
                "team": team,
                "view": view,
                "split": period
            }) for view in ["Passing", "Rushing", "Receiving"]
        ]
        
        passing, rushing, receiving = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'passing': self.data_processor.process_player_stats(passing, 'Passing'),
            'rushing': self.data_processor.process_player_stats(rushing, 'Rushing'),
            'receiving': self.data_processor.process_player_stats(receiving, 'Receiving')
        }
        
        # Analyze trends
        performance_trends = self.stats_analyzer.analyze_team_performance(processed_data)
        
        # Get analysis from LLM
        analysis_context = {
            **context,
            'data_type': 'team_performance',
            'period': period,
            'is_home': is_home,
            'team': team
        }
        
        analysis = await self.get_llama_response(
            self.prompts["team_performance"]["template"],
            {**processed_data, 'trends': performance_trends},
            analysis_context
        )
        
        return analysis

    async def analyze_defense(self, team: str, is_home: bool, context: Dict) -> str:
        """Enhanced defensive analysis"""
        print(f"\nAnalyzing defensive performance for {team}...")
        
        tasks = [
            self.get_data("playerstats", {
                "team": team,
                "view": "Defensive",
                "split": period
            }) for period in ["Last 2 Weeks", "Last 4 Weeks"]
        ]
        
        defense_2wk, defense_4wk = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'recent': self.data_processor.process_player_stats(defense_2wk, 'Defensive'),
            'extended': self.data_processor.process_player_stats(defense_4wk, 'Defensive')
        }
        
        # Analyze trends
        defensive_trends = self.stats_analyzer.analyze_defensive_performance(processed_data)
        
        # Get analysis from LLM
        analysis_context = {
            **context,
            'data_type': 'defense',
            'is_home': is_home,
            'team': team
        }
        
        analysis = await self.get_llama_response(
            self.prompts["defense"]["template"],
            {**processed_data, 'trends': defensive_trends},
            analysis_context
        )
        
        return analysis

    async def analyze_team_defense(self, context: Dict) -> str:
        """Enhanced team defense statistics analysis"""
        print("\nAnalyzing team defense statistics...")
        
        tasks = [
            self.get_data("teamdefense", {"team": context['home_team']}),
            self.get_data("teamdefense", {"team": context['away_team']})
        ]
        
        home_defense, away_defense = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'home_defense': self.data_processor.process_team_defense(home_defense),
            'away_defense': self.data_processor.process_team_defense(away_defense)
        }
        
        # Get analysis
        analysis = await self.get_llama_response(
            self.prompts["team_defense"]["template"],
            processed_data,
            {**context, 'data_type': 'team_defense'}
        )
        
        return analysis

    async def analyze_pass_pressure(self, context: Dict) -> str:
        """Enhanced pass pressure analysis"""
        print("\nAnalyzing pass rushing and pressure...")
        
        tasks = [
            self.get_data("teampasspressure", {"team": context['home_team']}),
            self.get_data("teampasspressure", {"team": context['away_team']})
        ]
        
        home_pressure, away_pressure = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'home_pressure': self.data_processor.process_pass_pressure(home_pressure),
            'away_pressure': self.data_processor.process_pass_pressure(away_pressure)
        }
        
        # Get analysis
        analysis = await self.get_llama_response(
            self.prompts["pass_pressure"]["template"],
            processed_data,
            {**context, 'data_type': 'pass_pressure'}
        )
        
        return analysis

    async def analyze_team_stats(self, context: Dict) -> str:
        """Enhanced team statistics analysis"""
        print("\nAnalyzing team statistics...")
        
        tasks = [
            self.get_data("teamstats/team", {"team": context['home_team']}),
            self.get_data("teamstats/team", {"team": context['away_team']})
        ]
        
        home_stats, away_stats = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'home_stats': self.data_processor.process_team_stats(home_stats),
            'away_stats': self.data_processor.process_team_stats(away_stats)
        }
        
        # Get analysis
        analysis = await self.get_llama_response(
            self.prompts["team_stats"]["template"],
            processed_data,
            {**context, 'data_type': 'team_stats'}
        )
        
        return analysis

    async def analyze_game_logs(self, context: Dict) -> str:
        """Enhanced game logs analysis"""
        print("\nAnalyzing game logs...")
        
        tasks = [
            self.get_data("gamelogs", {"team": context['home_team']}),
            self.get_data("gamelogs", {"team": context['away_team']}),
            self.get_data("oppgamelogs", {"team": context['home_team']}),
            self.get_data("oppgamelogs", {"team": context['away_team']})
        ]
        
        home_logs, away_logs, home_opp, away_opp = await asyncio.gather(*tasks)
        
        # Process data
        processed_data = {
            'home_logs': self.data_processor.process_game_logs(home_logs),
            'away_logs': self.data_processor.process_game_logs(away_logs),
            'home_opp': self.data_processor.process_game_logs(home_opp),
            'away_opp': self.data_processor.process_game_logs(away_opp)
        }
        
        # Analyze trends
        game_trends = self.stats_analyzer.analyze_game_trends(processed_data)
        
        # Get analysis
        analysis = await self.get_llama_response(
            self.prompts["game_logs"]["template"],
            {**processed_data, 'trends': game_trends},
            {**context, 'data_type': 'game_logs'}
        )
        
        return analysis

    async def get_final_recommendation(self, analyses: Dict[str, str], game_data: Dict) -> str:
        """Generate comprehensive final betting recommendations"""
        try:
            context = {
                'game_id': game_data['id'],
                'home_team': game_data['competitions'][0]['competitors'][0]['team']['displayName'],
                'away_team': game_data['competitions'][0]['competitors'][1]['team']['displayName'],
                'venue': game_data['competitions'][0]['venue']['fullName'],
                'date': game_data['date'],
                'data_type': 'final_analysis'
            }

            # Get odds data
            odds = await self._get_game_odds(game_data)
            
            # Structure all analyses
            structured_analyses = {
                "depth_charts": analyses['depth_charts'],
                "weather_injuries": analyses['weather_injuries'],
                "team_performance": {
                    "home": {
                        "last_4_weeks": analyses['home_last_4_weeks'],
                        "last_2_weeks": analyses['home_last_2_weeks']
                    },
                    "away":
                    {
                        "last_4_weeks": analyses['away_last_4_weeks'],
                        "last_2_weeks": analyses['away_last_2_weeks']
                    }
                },
                "defense": {
                    "home": analyses['home_defense'],
                    "away": analyses['away_defense'],
                    "comparison": analyses['team_defense']
                },
                "advanced_stats": {
                    "pass_pressure": analyses['pass_pressure'],
                    "team_stats": analyses['team_stats']
                },
                "game_logs": analyses['game_logs']
            }
            
            # Calculate win probabilities
            win_probs = self.stats_analyzer.calculate_win_probability(
                structured_analyses['team_performance']['home'],
                structured_analyses['team_performance']['away'],
                {'weather': analyses['weather_injuries']}
            )
            
            # Prepare final analysis context
            final_context = {
                **context,
                'odds': odds,
                'win_probability': win_probs,
                'analyses': structured_analyses
            }
            
            # Get final recommendation
            return await self.get_llama_response(
                self.prompts["final_analysis"]["template"],
                final_context,
                context
            )
            
        except Exception as e:
            print(f"Error in final recommendation: {str(e)}")
            raise

    async def analyze_game(self, game_data: Dict) -> Dict[str, str]:
        """Complete enhanced game analysis"""
        try:
            # Extract game context
            context = {
                'game_id': game_data['id'],
                'home_team': game_data['competitions'][0]['competitors'][0]['team']['displayName'],
                'away_team': game_data['competitions'][0]['competitors'][1]['team']['displayName'],
                'venue': game_data['competitions'][0]['venue']['fullName'],
                'date': game_data['date']
            }

            # Run all analyses
            analyses = {}
            
            print(f"\nAnalyzing {context['away_team']} @ {context['home_team']}")
            
            # Core analyses
            analyses['depth_charts'] = await self.analyze_depth_charts(context)
            analyses['weather_injuries'] = await self.analyze_weather_injuries(context)
            
            # Team performance analyses
            analyses['home_last_4_weeks'] = await self.analyze_team_performance(
                context['home_team'], "Last 4 Weeks", True, context
            )
            analyses['home_last_2_weeks'] = await self.analyze_team_performance(
                context['home_team'], "Last 2 Weeks", True, context
            )
            analyses['away_last_4_weeks'] = await self.analyze_team_performance(
                context['away_team'], "Last 4 Weeks", False, context
            )
            analyses['away_last_2_weeks'] = await self.analyze_team_performance(
                context['away_team'], "Last 2 Weeks", False, context
            )
            
            # Defensive analyses
            analyses['home_defense'] = await self.analyze_defense(
                context['home_team'], True, context
            )
            analyses['away_defense'] = await self.analyze_defense(
                context['away_team'], False, context
            )
            analyses['team_defense'] = await self.analyze_team_defense(context)
            
            # Additional analyses
            analyses['pass_pressure'] = await self.analyze_pass_pressure(context)
            analyses['team_stats'] = await self.analyze_team_stats(context)
            analyses['game_logs'] = await self.analyze_game_logs(context)
            
            # Final recommendation
            analyses['final_recommendation'] = await self.get_final_recommendation(
                analyses, game_data
            )
            
            return analyses
            
        except Exception as e:
            print(f"Error analyzing game: {str(e)}")
            raise

    async def analyze_all_games_in_week(self, week: int) -> None:
        """Analyze all games in a week"""
        week_dir = Path(f"Week {week}")
        week_dir.mkdir(exist_ok=True)
        print(f"\nCreated directory: {week_dir}")

        # Get games for the week
        games = await self._get_games(week)
        total_games = len(games)
        
        print(f"\nFound {total_games} games for Week {week}")
        
        for i, game in enumerate(games, 1):
            try:
                print(f"\nAnalyzing game {i}/{total_games}")
                analyses = await self.analyze_game(game)
                
                # Save analyses
                self._save_analysis_to_file(analyses, game, week_dir, i, total_games)
                
            except Exception as e:
                print(f"❌ Error analyzing game {i}: {str(e)}")
                continue

    async def _get_games(self, week: int) -> List[Dict]:
        """Get games for specified week"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.espn_api}/scoreboard"
            params = {"week": week, "seasontype": 2}
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"ESPN API returned status {response.status}")
                    
                data = await response.json()
                return data.get('events', [])

    async def _get_game_odds(self, game_data: Dict) -> Dict:
        """Get odds data for a game"""
        try:
            game_id = game_data['id']
            async with aiohttp.ClientSession() as session:
                url = f"{self.espn_api}/scoreboard/{game_id}/odds"
                
                async with session.get(url) as response:
                    if response.status != 200:
                        return {}
                        
                    data = await response.json()
                    
                    # Process odds data
                    if not data.get('items'):
                        return {}
                        
                    odds = data['items'][0]
                    return {
                        'spread': odds.get('spread', 0),
                        'over_under': odds.get('overUnder', 0),
                        'home_line': odds.get('homeTeamOdds', {}).get('moneyLine', 0),
                        'away_line': odds.get('awayTeamOdds', {}).get('moneyLine', 0)
                    }
                    
        except Exception as e:
            print(f"Error getting odds: {str(e)}")
            return {}

    def _save_analysis_to_file(self, analyses: Dict, game: Dict, 
                             week_dir: Path, game_num: int, total_games: int) -> None:
        """Save analysis results to file"""
        home_team = game['competitions'][0]['competitors'][0]['team']['displayName']
        away_team = game['competitions'][0]['competitors'][1]['team']['displayName']
        
        filename = week_dir / f"{away_team} @ {home_team} Analysis.txt"
        
        with open(filename, 'w') as f:
            f.write(f"NFL Game Analysis - Week {game['week']}\n")
            f.write(f"{away_team} @ {home_team}\n")
            f.write(f"Venue: {game['competitions'][0]['venue']['fullName']}\n")
            f.write(f"Date: {game['date']}\n")
            f.write("=" * 50 + "\n\n")
            
            # Write each analysis section
            sections = [
                ("DEPTH CHARTS ANALYSIS", 'depth_charts'),
                ("WEATHER AND INJURIES ANALYSIS", 'weather_injuries'),
                ("HOME TEAM PERFORMANCE (4 WEEKS)", 'home_last_4_weeks'),
                ("HOME TEAM PERFORMANCE (2 WEEKS)", 'home_last_2_weeks'),
                ("AWAY TEAM PERFORMANCE (4 WEEKS)", 'away_last_4_weeks'),
                ("AWAY TEAM PERFORMANCE (2 WEEKS)", 'away_last_2_weeks'),
                ("HOME TEAM DEFENSE", 'home_defense'),
                ("AWAY TEAM DEFENSE", 'away_defense'),
                ("TEAM DEFENSE COMPARISON", 'team_defense'),
                ("PASS PRESSURE ANALYSIS", 'pass_pressure'),
                ("TEAM STATS ANALYSIS", 'team_stats'),
                ("GAME LOGS ANALYSIS", 'game_logs'),
                ("FINAL BETTING RECOMMENDATION", 'final_recommendation')
            ]
            
            for title, key in sections:
                f.write(f"\n{title}:\n")
                f.write("=" * 30 + "\n")
                f.write(f"{analyses[key]}\n\n")

        print(f"✓ Analysis {game_num}/{total_games} saved to: {filename}")