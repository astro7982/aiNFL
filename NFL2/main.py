"""
NFL Game Analysis System - Main Execution Script
"""
import asyncio
from pathlib import Path
from src.analyzer import EnhancedNFLAnalyzer

async def main():
    print("\n🏈 Enhanced NFL Game Analyzer - Version 2.0 🏈")
    print("============================================")
    
    try:
        analyzer = EnhancedNFLAnalyzer()
        
        # Get week selection
        while True:
            try:
                week = int(input("\nEnter week number (1-18): "))
                if 1 <= week <= 18:
                    break
                print("Please enter a valid week number (1-18)")
            except ValueError:
                print("Please enter a valid number")
        
        print(f"\nStarting enhanced analysis of all games for Week {week}...")
        await analyzer.analyze_all_games_in_week(week)
        print("\n✓ Analysis complete! Check the weekly folder for results.")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Please check the error message and try again.")
        
    finally:
        print("\nAnalysis session completed.")

if __name__ == "__main__":
    asyncio.run(main())