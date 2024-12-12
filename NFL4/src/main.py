import asyncio
from typing import List, Dict, Optional
import sys
import os
from datetime import datetime
from pathlib import Path
from .analyzer import NFLAnalyzer

class AnalysisProgress:
    """Track and display analysis progress"""
    
    def __init__(self):
        self.current_step = 0
        self.total_steps = 14  # Total number of analysis steps per game
        self.current_game = 0
        self.total_games = 0
        
    def set_total_games(self, total: int):
        """Set total number of games to analyze"""
        self.total_games = total
        self.current_game = 0
        print(f"\nPreparing to analyze {total} games...")
        
    def next_game(self):
        """Move to next game"""
        self.current_game += 1
        self.current_step = 0
        print(f"\nStarting Game {self.current_game}/{self.total_games}")
        
    def update(self, step: str):
        """Update progress display with enhanced details"""
        self.current_step += 1
        game_progress = f"Game {self.current_game}/{self.total_games}: " if self.total_games > 0 else ""
        print(f"[{self.current_step}/{self.total_steps}] {game_progress}{step}")
        
    def complete(self):
        """Mark analysis as complete"""
        print("\n✓ Analysis complete!")

class NFLAnalysisManager:
    """Manage NFL game analysis process"""
    
    def __init__(self):
        self.analyzer = NFLAnalyzer()
        self.progress = AnalysisProgress()
        
    async def get_week_selection(self) -> int:
        """Get week selection from user with validation"""
        while True:
            try:
                print("\nAvailable Weeks:")
                for week in range(1, 19):
                    print(f"{week}. Week {week}")
                    
                week = int(input("\nEnter week number (1-18): "))
                if 1 <= week <= 18:
                    return week
                print("Please enter a valid week number (1-18)")
            except ValueError:
                print("Please enter a valid number")

    def create_output_directory(self, week: int) -> str:
        """Create and return output directory path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"Week_{week}_{timestamp}")
        output_dir.mkdir(parents=True, exist_ok=True)
        return str(output_dir)

    def print_analysis_summary(self, week: int, output_dir: str, analyzed_games: List[Dict]):
        """Print summary of completed analysis"""
        print(f"\nAnalysis Summary:")
        print(f"{'='*50}")
        print(f"Week {week} Analysis Complete")
        print(f"Games Analyzed: {len(analyzed_games)}")
        print(f"Output Directory: {output_dir}")
        print(f"\nProcessed Games:")
        for game in analyzed_games:
            print(f"\n- {game['away_team']} @ {game['home_team']}")
            print(f"  File: {game['file']}")
            if "error" in game['analyses']:
                print(f"  ⚠️  Analysis completed with errors")
        print(f"\nAnalysis files include:")
        print("- Team depth charts and personnel analysis")
        print("- Weather and injury impact assessment")
        print("- Team performance metrics (2-week and 4-week)")
        print("- Defensive analysis and comparisons")
        print("- Game logs and historical performance")
        print("- Comprehensive betting analysis")

    def print_game_summary(self, game: Dict):
        """Print summary for individual game"""
        print(f"\nGame Analysis Complete:")
        print(f"{'='*30}")
        print(f"Matchup: {game['away_team']} @ {game['home_team']}")
        print(f"Analysis File: {game['file']}")
        if "error" not in game['analyses']:
            print("Status: ✓ Complete")
        else:
            print(f"Status: ⚠️  Completed with errors")
            print(f"Error details: {game['analyses']['error']}")

    async def run_analysis(self):
        """Run the complete NFL analysis process"""
        print("\n🏈 NFL Game Analyzer - Enhanced Analysis Mode")
        print("=" * 50)
        print("\nThis analyzer will:")
        print("1. Analyze depth charts and personnel")
        print("2. Evaluate weather and injury impacts")
        print("3. Analyze team performance (2-week and 4-week)")
        print("4. Assess defensive capabilities")
        print("5. Generate comprehensive betting analysis")
        
        try:
            # Get week selection
            week = await self.get_week_selection()
            
            # Create output directory
            output_dir = self.create_output_directory(week)
            print(f"\nAnalyzing Week {week} games...")
            print(f"Results will be saved to: {output_dir}")
            
            # Run analysis with progress tracking
            analyzed_games = await self.analyzer.analyze_week(
                week, 
                progress_callback=self.progress.update
            )
            
            # Print comprehensive summary
            self.print_analysis_summary(week, output_dir, analyzed_games)
            
            # Print individual game summaries
            for game in analyzed_games:
                self.print_game_summary(game)
            
            self.progress.complete()
            print("\nAnalysis complete. Check the output directory for detailed analysis files.")
            
        except KeyboardInterrupt:
            print("\n\nAnalysis interrupted by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please check your connection and try again.")
            sys.exit(1)

async def main():
    """Main entry point"""
    try:
        manager = NFLAnalysisManager()
        await manager.run_analysis()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)