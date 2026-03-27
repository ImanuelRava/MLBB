import pandas as pd
import os

HERO_DATA = {}

def load_hero_data(file_path='Analyst.xlsx'):
    global HERO_DATA
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File '{file_path}' not found.")
        return {}

    try:
        # Read the specific sheet
        df = pd.read_excel(file_path, sheet_name='Hero Data')
        
        # 1. Clean Column Names (remove whitespace, lowercase for matching)
        df.columns = [str(col).strip() for col in df.columns]
        
        # 2. Define Helper to get value or default
        def get_row_val(row, key, default='N/A'):
            if key not in row:
                return default
            val = row[key]
            if pd.isna(val) or str(val).strip() == '':
                return default
            return str(val).strip()

        data = {}
        for index, row in df.iterrows():
            # Get Hero Name
            hero_name = get_row_val(row, 'Hero', None)
            if not hero_name:
                continue

            # 3. Build Dictionary with Defaults
            data[hero_name] = {
                "Role 1": get_row_val(row, 'Role 1', 'N/A'),
                "Role 2": get_row_val(row, 'Role 2', 'N/A'),
                "Lane 1": get_row_val(row, 'Lane 1', 'N/A'),
                "Lane 2": get_row_val(row, 'Lane 2', 'N/A'),
                "Durability": float(get_row_val(row, 'Durability', 0)),
                "Offense": float(get_row_val(row, 'Offense', 0)),
                "Crowd Control": float(get_row_val(row, 'Crowd Control', 0)),
                "Mobility": float(get_row_val(row, 'Mobility', 0)),
                "Lane Control": float(get_row_val(row, 'Lane Control', 0))
            }
        
        print(f"Successfully loaded {len(data)} heroes from Excel.")
        return data

    except Exception as e:
        print(f"[ERROR] Loading failed: {e}")
        return {}

# Load data
HERO_DATA = load_hero_data()