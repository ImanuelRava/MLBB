import json

class MLBBDraftAnalyzer:
    def __init__(self):
        # Mock Database: In a real app, this would come from a CSV or SQL DB.
        # Structure: Hero Name -> Attributes
        self.hero_db = {
            # MARKSMEN
            "Wanwan": {"role": "Gold", "type": "Marksman", "hard_cc": True, "mobility": "High", "counters": ["Khufra", "Sabert"], "synergies": ["Ruby", "Khufra"], "power_spike": "Mid"},
            "Claude": {"role": "Gold", "type": "Marksman", "hard_cc": False, "mobility": "High", "counters": ["Khufra"], "synergies": ["Estes", "Angela"], "power_spike": "Mid"},
            "Miya": {"role": "Gold", "type": "Marksman", "hard_cc": False, "mobility": "Medium", "counters": ["Saber", "Eudora"], "synergies": ["Estes"], "power_spike": "Late"},
            # MAGES
            "Lylia": {"role": "Mid", "type": "Mage", "hard_cc": True, "mobility": "Medium", "counters": ["Esmeralda"], "synergies": ["Khufra", "Chou"], "power_spike": "Early"},
            "Kagura": {"role": "Mid", "type": "Mage", "hard_cc": True, "mobility": "High", "counters": ["Chou"], "synergies": [], "power_spike": "Mid"},
            "Valentina": {"role": "Mid", "type": "Mage", "hard_cc": True, "mobility": "Medium", "counters": ["Uranus", "Esmeralda"], "synergies": ["Chou"], "power_spike": "Early"},
            # FIGHTERS/EXP
            "Yu Zhong": {"role": "Exp", "type": "Fighter", "hard_cc": True, "mobility": "High", "counters": ["Ruby"], "synergies": ["Pharsa"], "power_spike": "Mid"},
            "Paquito": {"role": "Exp", "type": "Fighter", "hard_cc": True, "mobility": "High", "counters": ["Chou"], "synergies": [], "power_spike": "Early"},
            "Uranus": {"role": "Exp", "type": "Fighter", "hard_cc": False, "mobility": "Medium", "counters": ["Karrie", "Valentina"], "synergies": ["Estes"], "power_spike": "Late"},
            # TANKS/ROAM
            "Khufra": {"role": "Roam", "type": "Tank", "hard_cc": True, "mobility": "Medium", "counters": ["Wanwan", "Claude", "Ling"], "synergies": [], "power_spike": "Early"},
            "Atlas": {"role": "Roam", "type": "Tank", "hard_cc": True, "mobility": "Medium", "counters": [], "synergies": ["Pharsa", "Kagura"], "power_spike": "Early"},
            "Ruby": {"role": "Roam", "type": "Tank", "hard_cc": True, "mobility": "Medium", "counters": [], "synergies": ["Wanwan"], "power_spike": "Early"},
            # JUNGLE
            "Ling": {"role": "Jungle", "type": "Assassin", "hard_cc": False, "mobility": "Very High", "counters": ["Khufra"], "synergies": [], "power_spike": "Mid"},
            "Martis": {"role": "Jungle", "type": "Fighter", "hard_cc": True, "mobility": "Medium", "counters": [], "synergies": [], "power_spike": "Early"},
        }

    def get_hero_data(self, name):
        return self.hero_db.get(name)

    def analyze_draft(self, team_draft, enemy_draft):
        """
        Main AI Analysis Function.
        Returns a dictionary containing scores and detailed breakdown.
        """
        report = {
            "team_composition_score": 0,
            "enemy_composition_score": 0,
            "counter_analysis": [],
            "synergy_analysis": [],
            "lane_dynamics": {},
            "final_verdict": ""
        }

        # 1. Validate Drafts
        if len(team_draft) != 5 or len(enemy_draft) != 5:
            return {"error": "Drafts must contain exactly 5 heroes."}

        # 2. Analyze Team Composition (Role Balance)
        team_comp_score = self._evaluate_composition(team_draft)
        enemy_comp_score = self._evaluate_composition(enemy_draft)
        report["team_composition_score"] = team_comp_score
        report["enemy_composition_score"] = enemy_comp_score

        # 3. Analyze Counters (AI Logic: Check Intersections)
        counters_found = []
        for ally_hero in team_draft:
            ally_data = self.get_hero_data(ally_hero)
            if not ally_data: continue
            
            # Check if ally counters enemies
            for enemy_hero in enemy_draft:
                if enemy_hero in ally_data.get("counters", []):
                    counters_found.append(f"✅ {ally_hero} hard counters {enemy_hero}")
        
        for enemy_hero in enemy_draft:
            enemy_data = self.get_hero_data(enemy_hero)
            if not enemy_data: continue
            
            # Check if enemies counter allies
            for ally_hero in team_draft:
                if ally_hero in enemy_data.get("counters", []):
                    counters_found.append(f"⚠️ {enemy_hero} hard counters {ally_hero}")
        
        report["counter_analysis"] = counters_found

        # 4. Analyze Synergy
        synergies = self._check_synergies(team_draft)
        report["synergy_analysis"] = synergies

        # 5. Final Verdict Calculation
        # Base score is comp balance. +10 for every good synergy, -5 for getting countered.
        final_score = team_comp_score - enemy_comp_score
        
        positive_count = len([x for x in counters_found if x.startswith("✅")])
        negative_count = len([x for x in counters_found if x.startswith("⚠️")])
        
        final_score += (positive_count * 15)
        final_score -= (negative_count * 15)
        final_score += (len(synergies) * 10)

        if final_score > 20:
            report["final_verdict"] = "ADVANTAGE: Your draft is significantly better."
        elif final_score < -20:
            report["final_verdict"] = "DISADVANTAGE: Enemy draft counters you heavily."
        else:
            report["final_verdict"] = "EVEN: Drafts are balanced. Skill will decide the outcome."
            
        report["score_diff"] = final_score
        return report

    def _evaluate_composition(self, draft):
        """
        AI Logic: Checks if the team has a balanced role distribution.
        Ideal: 1 Tank, 1 Mage, 1 Marksman, 1 Jungle, 1 Fighter
        """
        score = 50 # Base score
        roles_present = {"Tank": 0, "Mage": 0, "Marksman": 0, "Fighter": 0, "Assassin": 0, "Support": 0}
        
        for hero in draft:
            data = self.get_hero_data(hero)
            if data:
                role_type = data.get("type")
                if role_type in roles_present:
                    roles_present[role_type] += 1
        
        # Penalties for missing key roles
        if roles_present["Marksman"] == 0: score -= 15 # Lack of tower push/late game
        if roles_present["Tank"] == 0: score -= 15 # Lack of frontline
        if roles_present["Mage"] == 0: score -= 10 # Lack of magic damage
        
        # Bonus for standard meta
        if roles_present["Tank"] >= 1 and roles_present["Marksman"] >= 1:
            score += 10
            
        return score

    def _check_synergies(self, draft):
        synergies = []
        for hero_a in draft:
            data_a = self.get_hero_data(hero_a)
            if not data_a: continue
            
            for target in data_a.get("synergies", []):
                if target in draft:
                    synergies.append(f"🔥 Strong Combo: {hero_a} + {target}")
        return synergies

# ==========================================
# EXECUTION EXAMPLE
# ==========================================

# Initialize AI
ai = MLBBDraftAnalyzer()

# Define Drafts (User Input)
# Scenario: My Team has a Wanwan + Ruby combo, Enemy has a Khufra (Counter to Wanwan)
my_team = ["Wanwan", "Lylia", "Yu Zhong", "Khufra", "Ling"]
enemy_team = ["Claude", "Valentina", "Uranus", "Atlas", "Martis"]

print(f"Analyzing Draft:\nMy Team: {my_team}\nEnemy Team: {enemy_team}\n")

# Run Analysis
result = ai.analyze_draft(my_team, enemy_team)

# Print Report
print(f"--- COMPOSITION SCORE ---")
print(f"My Team Balance: {result['team_composition_score']}/100")
print(f"Enemy Team Balance: {result['enemy_composition_score']}/100")

print(f"\n--- COUNTER ANALYSIS ---")
for item in result['counter_analysis']:
    print(item)

print(f"\n--- SYNERGY ANALYSIS ---")
for item in result['synergy_analysis']:
    print(item)

print(f"\n--- FINAL VERDICT ---")
print(result['final_verdict'])