"""
NFL Statistics Analyzer module for statistical analysis and trend identification
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class NFLStatisticsAnalyzer:
    def __init__(self):
        self.sample_size_threshold = 3  # Minimum games for trend analysis

    def analyze_qb_performance(self, stats: Dict) -> Dict:
        """Analyze quarterback performance metrics"""
        analysis = {
            'efficiency': self._calculate_qb_efficiency(stats),
            'trends': self._analyze_qb_trends(stats),
            'pressure_performance': self._analyze_pressure_impact(stats),
            'situational': self._analyze_situational_performance(stats)
        }
        return analysis

    def _calculate_qb_efficiency(self, stats: Dict) -> Dict:
        """Calculate QB efficiency metrics"""
        if not stats:
            return {}

        try:
            attempts = float(stats.get('ATT', 0))
            if attempts == 0:
                return {}

            return {
                'completion_pct': (float(stats.get('CMP', 0)) / attempts) * 100,
                'yards_per_attempt': float(stats.get('YDS', 0)) / attempts,
                'touchdown_rate': (float(stats.get('TD', 0)) / attempts) * 100,
                'interception_rate': (float(stats.get('INT', 0)) / attempts) * 100
            }
        except (ValueError, TypeError, ZeroDivisionError):
            return {}

    def analyze_rushing_attack(self, stats: Dict) -> Dict:
        """Analyze rushing attack effectiveness"""
        analysis = {
            'efficiency': self._calculate_rushing_efficiency(stats),
            'trends': self._analyze_rushing_trends(stats),
            'situational': self._analyze_rushing_situations(stats)
        }
        return analysis

    def analyze_defensive_performance(self, stats: Dict) -> Dict:
        """Analyze defensive performance metrics"""
        analysis = {
            'overall': self._analyze_overall_defense(stats),
            'situational': self._analyze_defensive_situations(stats),
            'pressure': self._analyze_pressure_generation(stats)
        }
        return analysis

    def analyze_game_trends(self, game_logs: List[Dict]) -> Dict:
        """Analyze team performance trends from game logs"""
        if len(game_logs) < self.sample_size_threshold:
            return {'error': 'Insufficient game data for trend analysis'}

        df = pd.DataFrame(game_logs)
        
        trends = {
            'scoring': self._analyze_scoring_trends(df),
            'yardage': self._analyze_yardage_trends(df),
            'efficiency': self._analyze_efficiency_trends(df),
            'situational': self._analyze_situational_trends(df)
        }
        return trends

    def _analyze_scoring_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze scoring patterns and trends"""
        try:
            recent_scores = df['score.team'].tail(3).tolist()
            avg_score = df['score.team'].mean()
            score_trend = self._calculate_trend(recent_scores)
            
            return {
                'recent_scores': recent_scores,
                'average_score': round(avg_score, 2),
                'trend': score_trend,
                'consistency': self._calculate_consistency(df['score.team'])
            }
        except Exception:
            return {}

    def _analyze_yardage_trends(self, df: pd.DataFrame) -> Dict:
        """Analyze yardage production trends"""
        try:
            passing_yards = df['stats.passing_yards'].tolist()
            rushing_yards = df['stats.rushing_yards'].tolist()
            
            return {
                'passing': {
                    'trend': self._calculate_trend(passing_yards),
                    'average': round(np.mean(passing_yards), 2),
                    'consistency': self._calculate_consistency(passing_yards)
                },
                'rushing': {
                    'trend': self._calculate_trend(rushing_yards),
                    'average': round(np.mean(rushing_yards), 2),
                    'consistency': self._calculate_consistency(rushing_yards)
                }
            }
        except Exception:
            return {}

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from recent values"""
        if len(values) < 2:
            return 'insufficient_data'
            
        diffs = [values[i] - values[i-1] for i in range(1, len(values))]
        avg_diff = np.mean(diffs)
        
        if avg_diff > 5:
            return 'strongly_increasing'
        elif avg_diff > 0:
            return 'slightly_increasing'
        elif avg_diff < -5:
            return 'strongly_decreasing'
        elif avg_diff < 0:
            return 'slightly_decreasing'
        else:
            return 'stable'

    def _calculate_consistency(self, values: List[float]) -> str:
        """Calculate consistency rating based on variance"""
        if len(values) < 2:
            return 'insufficient_data'
            
        cv = np.std(values) / np.mean(values) if np.mean(values) != 0 else float('inf')
        
        if cv < 0.1:
            return 'very_consistent'
        elif cv < 0.2:
            return 'consistent'
        elif cv < 0.3:
            return 'moderately_consistent'
        else:
            return 'inconsistent'

    def analyze_matchup_advantages(self, team_stats: Dict, opponent_stats: Dict) -> Dict:
        """Analyze statistical matchup advantages"""
        advantages = {
            'passing_game': self._compare_passing_matchup(team_stats, opponent_stats),
            'rushing_game': self._compare_rushing_matchup(team_stats, opponent_stats),
            'defense': self._compare_defensive_matchup(team_stats, opponent_stats),
            'special_teams': self._compare_special_teams(team_stats, opponent_stats)
        }
        return advantages

    def analyze_weather_impact(self, weather_data: Dict, team_stats: Dict) -> Dict:
        """Analyze potential weather impacts on team performance"""
        impacts = {
            'passing_game': self._analyze_weather_passing_impact(weather_data, team_stats),
            'rushing_game': self._analyze_weather_rushing_impact(weather_data, team_stats),
            'kicking_game': self._analyze_weather_kicking_impact(weather_data, team_stats)
        }
        return impacts

    def _analyze_weather_passing_impact(self, weather: Dict, stats: Dict) -> Dict:
        """Analyze weather impact on passing game"""
        wind_speed = float(weather.get('wind_speed', 0))
        precipitation = float(weather.get('precipitation', '0').strip('%'))
        
        impact = {
            'wind_impact': 'high' if wind_speed > 15 else 'moderate' if wind_speed > 10 else 'low',
            'precipitation_impact': 'high' if precipitation > 50 else 'moderate' if precipitation > 30 else 'low'
        }
        return impact

    def calculate_win_probability(self, team_stats: Dict, opponent_stats: Dict, 
                                conditions: Dict) -> float:
        """Calculate win probability based on comprehensive analysis"""
        try:
            # Base probability from historical performance
            base_prob = self._calculate_base_probability(team_stats, opponent_stats)
            
            # Adjust for conditions
            weather_adj = self._calculate_weather_adjustment(conditions.get('weather', {}))
            injury_adj = self._calculate_injury_adjustment(conditions.get('injuries', {}))
            
            # Final probability
            final_prob = base_prob * weather_adj * injury_adj
            
            # Ensure probability is between 0 and 1
            return max(min(final_prob, 1.0), 0.0)
        except Exception:
            return 0.5  # Return 50% if calculation fails

    def _calculate_base_probability(self, team: Dict, opponent: Dict) -> float:
        """Calculate base win probability from team statistics"""
        try:
            team_score = (
                float(team.get('points_per_game', 0)) * 0.3 +
                float(team.get('yards_per_game', 0)) * 0.2 +
                float(team.get('defensive_rating', 0)) * 0.3 +
                float(team.get('turnover_margin', 0)) * 0.2
            )
            
            opp_score = (
                float(opponent.get('points_per_game', 0)) * 0.3 +
                float(opponent.get('yards_per_game', 0)) * 0.2 +
                float(opponent.get('defensive_rating', 0)) * 0.3 +
                float(opponent.get('turnover_margin', 0)) * 0.2
            )
            
            return team_score / (team_score + opp_score)
        except Exception:
            return 0.5