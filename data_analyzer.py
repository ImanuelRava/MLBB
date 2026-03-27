import pandas as pd
import collections
import os

class DataAnalyzer:
    def __init__(self):
        self.matches = [] # Stores detailed data for filtering
        self.hero_win_rates = collections.defaultdict(lambda: {'wins': 0, 'total': 0})
        self.is_loaded = False
        self.load_local_data()

    def load_local_data(self):
        file_path = 'Analyst.xlsx'
        if os.path.exists(file_path):
            print(f"Found {file_path}. Processing tournament data...")
            success, msg = self.process_file(file_path)
            if success:
                print("Tournament data loaded successfully.")
            else:
                print(f"Failed to load tournament data: {msg}")
        else:
            print("Analyst.xlsx not found.")

    def process_file(self, file_path):
        try:
            df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
            
            # Find Header Row
            header_row_idx = None
            for i, row in df_raw.iterrows():
                if 'Ban 1' in row.values:
                    header_row_idx = i
                    break
            
            if header_row_idx is None: return False, "Header row not found."

            # Find Data Start Row
            start_row_idx = None
            for i in range(header_row_idx + 1, len(df_raw)):
                val = str(df_raw.iloc[i, 0]).strip() 
                if val and val != '*' and val != 'nan' and 'Tournament' not in val:
                    start_row_idx = i
                    break
            
            if start_row_idx is None: return False, "Data rows not found."

            df = df_raw.iloc[start_row_idx:].reset_index(drop=True)
            
            # Map Columns
            header_row = df_raw.iloc[header_row_idx]
            header_row_norm = header_row.astype(str).str.strip().str.lower()
            ban1_cols = header_row_norm[header_row_norm == 'ban 1'].index.tolist()
            
            if len(ban1_cols) < 2: return False, "Column mapping failed."

            col_blue_start = ban1_cols[0]
            col_red_start = ban1_cols[1]
            
            # Team Names are usually in the column immediately before the Ban columns
            col_blue_team = col_blue_start - 1
            col_red_team = col_red_start - 1
            
            # Process Data
            def clean_name(name):
                if pd.isna(name): return ""
                return str(name).strip()

            for index, row in df.iterrows():
                try:
                    tournament = str(row.iloc[0]).strip()
                    selected_map = str(row.iloc[1]).strip()
                    
                    # Extract Team Names
                    blue_team = clean_name(row.iloc[col_blue_team])
                    red_team = clean_name(row.iloc[col_red_team])
                    
                    # Blue Side
                    blue_bans = [clean_name(b) for b in row.iloc[col_blue_start : col_blue_start + 5].dropna().tolist()]
                    blue_picks = [clean_name(p) for p in row.iloc[col_blue_start + 5 : col_blue_start + 10].dropna().tolist()]
                    blue_result = str(row.iloc[col_blue_start + 10]).strip().upper()
                    
                    # Red Side
                    red_bans = [clean_name(b) for b in row.iloc[col_red_start : col_red_start + 5].dropna().tolist()]
                    red_picks = [clean_name(p) for p in row.iloc[col_red_start + 5 : col_red_start + 10].dropna().tolist()]
                    red_result = str(row.iloc[col_red_start + 10]).strip().upper()

                    # Store Match Data
                    self.matches.append({
                        'tournament': tournament,
                        'map': selected_map,
                        'blue_team': blue_team,
                        'red_team': red_team,
                        'blue_bans': blue_bans,
                        'blue_picks': blue_picks,
                        'blue_result': blue_result,
                        'red_bans': red_bans,
                        'red_picks': red_picks,
                        'red_result': red_result
                    })
                    
                    # Update Global Win Rates
                    self._update_hero_stats(blue_picks, blue_result)
                    self._update_hero_stats(red_picks, red_result)

                except Exception:
                    continue

            self.is_loaded = True
            return True, "Success"
            
        except Exception as e:
            return False, str(e)

    def _update_hero_stats(self, picks, result):
        for hero in picks:
            self.hero_win_rates[hero]['total'] += 1
            if result == 'WIN':
                self.hero_win_rates[hero]['wins'] += 1

    def get_unique_values(self, column, tournament_filter=None):
        """Returns unique values for a specific column. Supports filtering teams by tournament."""
        if not self.matches: return []
        
        # Special handling for 'team'
        if column == 'team':
            teams = set()
            for m in self.matches:
                # If a tournament is selected, only add teams from that tournament
                if tournament_filter and tournament_filter != "All" and m['tournament'] != tournament_filter:
                    continue
                teams.add(m['blue_team'])
                teams.add(m['red_team'])
            return sorted(list(teams))
            
        return sorted(list(set(m[column] for m in self.matches)))

    def get_top_bans(self, side, phase, n=5, tournament_filter=None, map_filter=None, team_filter=None):
        """Calculates top bans based on filters."""
        data = []
        
        for match in self.matches:
            if tournament_filter and tournament_filter != "All" and match['tournament'] != tournament_filter: continue
            if map_filter and map_filter != "All" and match['map'] != map_filter: continue
            if team_filter and team_filter != "All":
                if side == 'blue' and match['blue_team'] != team_filter: continue
                elif side == 'red' and match['red_team'] != team_filter: continue
            
            bans = match[f"{side.lower()}_bans"]
            if phase == 1: data.extend(bans[:3])
            else: data.extend(bans[3:5])
                
        return collections.Counter(data).most_common(n)

    def get_top_picks(self, side, n=5, tournament_filter=None, map_filter=None, team_filter=None):
        """Calculates top picks based on filters."""
        data = []
        
        for match in self.matches:
            if tournament_filter and tournament_filter != "All" and match['tournament'] != tournament_filter: continue
            if map_filter and map_filter != "All" and match['map'] != map_filter: continue
            if team_filter and team_filter != "All":
                if side == 'blue' and match['blue_team'] != team_filter: continue
                elif side == 'red' and match['red_team'] != team_filter: continue

            picks = match[f"{side.lower()}_picks"]
            data.extend(picks[:3])
                
        return collections.Counter(data).most_common(n)

    def get_hero_summary(self, side, tournament_filter=None, map_filter=None, team_filter=None):
        """
        Generates a summary dataframe: [Hero, Picks, Bans, Win Rate (float)]
        Returns a Pandas DataFrame.
        """
        stats = collections.defaultdict(lambda: {'picks': 0, 'bans': 0, 'wins': 0})
        
        for match in self.matches:
            # Apply Filters
            if tournament_filter and tournament_filter != "All" and match['tournament'] != tournament_filter: continue
            if map_filter and map_filter != "All" and match['map'] != map_filter: continue
            
            target_picks, target_bans, target_result = [], [], None
            
            if side == 'Blue':
                if team_filter and team_filter != "All" and match['blue_team'] != team_filter: continue
                target_picks = match['blue_picks']
                target_bans = match['blue_bans']
                target_result = match['blue_result']
            else: # Red
                if team_filter and team_filter != "All" and match['red_team'] != team_filter: continue
                target_picks = match['red_picks']
                target_bans = match['red_bans']
                target_result = match['red_result']

            # Aggregate
            for hero in target_picks:
                stats[hero]['picks'] += 1
                if target_result == 'WIN': stats[hero]['wins'] += 1
            for hero in target_bans:
                stats[hero]['bans'] += 1
        
        # Build DataFrame
        data = []
        for hero, s in stats.items():
            wr = (s['wins'] / s['picks'] * 100) if s['picks'] > 0 else 0.0
            data.append({
                'Hero': hero,
                'Picks': s['picks'],
                'Bans': s['bans'],
                'Win Rate': wr # Return float for sorting
            })
        
        df = pd.DataFrame(data)
        return df

    def get_hero_win_rate(self, hero_name):
        data = self.hero_win_rates.get(hero_name)
        if not data or data['total'] == 0: return None
        return (data['wins'] / data['total']) * 100