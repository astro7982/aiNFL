from llama_cpp import Llama
import aiohttp
import asyncio
import json
import time
import requests

class NHLAnalyzer:
   def __init__(self):
       print("\nInitializing NHL Analyzer with Ollama...")
       self.ollama_url = "http://localhost:11434/api/generate"
       self.api_base = "https://sportsstatsgather.com/api"
       self.model = "llama3.2"
       self.model_params = {
           "context_length": 65536,
           "num_ctx": 65536,
           "num_gpu": 1,
           "num_thread": 4,
           "gpu_layers": 35
       }
       self.analyses = {}
       
       self.nhl_teams = [
           "Utah Hockey Club", "Boston Bruins", "Buffalo Sabres", 
           "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks",
           "Colorado Avalanche", "Columbus Blue Jackets", "Dallas Stars",
           "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers",
           "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens",
           "Nashville Predators", "New Jersey Devils", "New York Islanders",
           "New York Rangers", "Ottawa Senators", "Philadelphia Flyers",
           "Pittsburgh Penguins", "San Jose Sharks", "Seattle Kraken",
           "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs",
           "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals",
           "Winnipeg Jets"
       ]

   def validate_team(self, team: str) -> str:
       team = team.lower()
       for valid_team in self.nhl_teams:
           if team in valid_team.lower():
               return valid_team
       raise ValueError(f"Invalid team name: {team}")

   async def get_data(self, endpoint: str, params: dict):
       url = f"{self.api_base}/nhl/data/{endpoint}"
       print(f"Fetching data from: {url}")
       print(f"Parameters: {params}")
       start_time = time.time()
       
       async with aiohttp.ClientSession() as session:
           async with session.get(url, params=params) as response:
               data = await response.json()
               elapsed = time.time() - start_time
               print(f"✓ Data received in {elapsed:.2f} seconds")
               return data

   async def analyze_team_performance(self, team1: str, team2: str):
       print("\nAnalyzing team performance...")
       tasks = [
           self.get_data("teams", {"team": team1, "situation": "5on5"}),
           self.get_data("teams", {"team": team2, "situation": "5on5"}),
           self.get_data("teams", {"team": team1, "situation": "all"}),
           self.get_data("teams", {"team": team2, "situation": "all"})
       ]
       
       team1_5v5, team2_5v5, team1_all, team2_all = await asyncio.gather(*tasks)
       
       prompt = f"""# Team Analysis: {team1} vs {team2}
Review 5v5 and overall stats:

{team1} Stats:
5v5: {json.dumps(team1_5v5)}
All: {json.dumps(team1_all)}

{team2} Stats:
5v5: {json.dumps(team2_5v5)}
All: {json.dumps(team2_all)}

Analyze:
1. Scoring efficiency
2. Possession metrics
3. Shot quality
4. Defensive performance
5. Key advantages
"""
       
       response = requests.post(self.ollama_url, json={
           "model": self.model,
           "prompt": prompt,
           "stream": False,
           **self.model_params
       })
       
       analysis = response.json()['response']
       self.analyses['team_performance'] = analysis
       return analysis

   async def analyze_special_teams(self, team1: str, team2: str):
       print("\nAnalyzing special teams...")
       tasks = [
           self.get_data("teams", {"team": team1, "situation": "5on4"}),
           self.get_data("teams", {"team": team2, "situation": "5on4"}),
           self.get_data("teams", {"team": team1, "situation": "4on5"}),
           self.get_data("teams", {"team": team2, "situation": "4on5"})
       ]
       
       team1_pp, team2_pp, team1_pk, team2_pk = await asyncio.gather(*tasks)
       
       prompt = f"""# Special Teams Analysis: {team1} vs {team2}
Review PP and PK performance:

{team1}:
PP: {json.dumps(team1_pp)}
PK: {json.dumps(team1_pk)}

{team2}:
PP: {json.dumps(team2_pp)}
PK: {json.dumps(team2_pk)}

Analyze:
1. Power play efficiency
2. Penalty kill success
3. Special teams impact
4. Key matchups
"""
       
       response = requests.post(self.ollama_url, json={
           "model": self.model,
           "prompt": prompt,
           "stream": False,
           **self.model_params
       })
       
       analysis = response.json()['response']
       self.analyses['special_teams'] = analysis
       return analysis

   async def analyze_goalies(self, team1: str, team2: str):
       print("\nAnalyzing goalies...")
       tasks = [
           self.get_data("goalies", {"team": team1, "position": "G"}),
           self.get_data("goalies", {"team": team2, "position": "G"})
       ]
       
       team1_goalies, team2_goalies = await asyncio.gather(*tasks)
       
       prompt = f"""# Goalie Analysis: {team1} vs {team2}

{team1} Goalies:
{json.dumps(team1_goalies)}

{team2} Goalies:
{json.dumps(team2_goalies)}

Analyze:
1. Save percentages
2. Goals against
3. High-danger saves
4. Recent form
5. Starting matchup
"""
       
       response = requests.post(self.ollama_url, json={
           "model": self.model,
           "prompt": prompt,
           "stream": False,
           **self.model_params
       })
       
       analysis = response.json()['response']
       self.analyses['goalies'] = analysis
       return analysis

   async def analyze_recent_performance(self, team1: str, team2: str):
       print("\nAnalyzing recent performance...")
       tasks = [
           self.get_data("gamestats", {"team": team1}),
           self.get_data("gamestats", {"team": team2})
       ]
       
       team1_recent, team2_recent = await asyncio.gather(*tasks)
       
       prompt = f"""# Recent Performance: {team1} vs {team2}

{team1} Games:
{json.dumps(team1_recent)}

{team2} Games:
{json.dumps(team2_recent)}

Analyze:
1. Recent trends
2. Scoring patterns
3. Win/loss streaks
4. Home/away splits
5. Key injuries impact
"""
       
       response = requests.post(self.ollama_url, json={
           "model": self.model,
           "prompt": prompt,
           "stream": False,
           **self.model_params
       })
       
       analysis = response.json()['response']
       self.analyses['recent_performance'] = analysis
       return analysis

   async def get_betting_recommendations(self, team1: str, team2: str):
       prompt = f"""# Betting Analysis: {team1} vs {team2}

Previous Analyses:
1. Team Performance:
{self.analyses['team_performance']}

2. Special Teams:
{self.analyses['special_teams']}

3. Goalies:
{self.analyses['goalies']}

4. Recent Form:
{self.analyses['recent_performance']}

Provide:
1. Moneyline prediction
2. Over/under assessment
3. Key prop recommendations
4. Risk factors
"""

       print("\nGetting final betting recommendations...")
       response = requests.post(self.ollama_url, json={
           "model": self.model,
           "prompt": prompt,
           "stream": False,
           **self.model_params
       })

       recommendations = response.json().get('response', "No recommendations received.")
       self.analyses['betting_recommendations'] = recommendations
       return recommendations

async def main():
   print("\n🏒 NHL Betting Analyzer 🏒")
   print("=========================")
   
   analyzer = NHLAnalyzer()
   
   print("\nAvailable Teams:")
   for i, team in enumerate(analyzer.nhl_teams, 1):
       print(f"{i}. {team}")
   
   while True:
       try:
           team1 = input("\nEnter first team name (or number): ")
           if team1.isdigit() and 1 <= int(team1) <= len(analyzer.nhl_teams):
               team1 = analyzer.nhl_teams[int(team1) - 1]
           
           team2 = input("Enter second team name (or number): ")
           if team2.isdigit() and 1 <= int(team2) <= len(analyzer.nhl_teams):
               team2 = analyzer.nhl_teams[int(team2) - 1]
           
           team1 = analyzer.validate_team(team1)
           team2 = analyzer.validate_team(team2)
           
           if team1 == team2:
               print("⚠️  Please select two different teams.")
               continue
               
           break
       except ValueError as e:
           print(f"❌ Error: {e}")
           print("Please try again.")
   
   try:
       print(f"\nStarting comprehensive analysis of {team1} vs {team2}...")
       
       await analyzer.analyze_team_performance(team1, team2)
       await analyzer.analyze_special_teams(team1, team2)
       await analyzer.analyze_goalies(team1, team2)
       await analyzer.analyze_recent_performance(team1, team2)
       
       recommendations = await analyzer.get_betting_recommendations(team1, team2)
       
       print("\n📊 Betting Recommendations:")
       print("=======================")
       print(recommendations)
       
   except Exception as e:
       print(f"\n❌ Error during analysis: {e}")
       print("Please try again or contact support if the issue persists.")

if __name__ == "__main__":
   asyncio.run(main())
