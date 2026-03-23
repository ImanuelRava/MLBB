import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

def extract_hero_stats(hero_name):
    """
    Scrapes the Mobile Legends Fandom wiki for a specific hero's stats.
    """
    # Format the hero name for the URL
    formatted_name = hero_name.replace(" ", "_")
    url = f"https://mobile-legends.fandom.com/wiki/{formatted_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        infobox = soup.find('aside', class_='portable-infobox')
        if not infobox:
            return None

        stats = {
            "Hero Name": hero_name,
            "Durability": None,
            "Control Effect": None,
            "Offense": None
        }

        data_items = infobox.find_all('div', class_='pi-item')

        for item in data_items:
            label_tag = item.find('h3', class_='pi-data-label')
            if label_tag:
                label_text = label_tag.get_text(strip=True)
                
                if label_text in stats:
                    value_div = item.find('div', class_='pi-data-value')
                    if value_div:
                        # Extract percentage from width style
                        style_content = str(value_div)
                        match = re.search(r'width:\s*(\d+)%', style_content)
                        if match:
                            stats[label_text] = int(match.group(1))
                        else:
                            stats[label_text] = value_div.get_text(strip=True)

        return stats

    except Exception as e:
        print(f"Error extracting {hero_name}: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    
    # 1. CONFIGURATION
    input_filename = "MLBB.xlsx"   # Your input file name
    output_filename = "hero_stats_output.xlsx" # The result file name
    
    # 2. READ THE EXCEL FILE
    try:
        df_input = pd.read_excel(input_filename)
        
        # Ensure the 'Hero' column exists
        if 'Hero' not in df_input.columns:
            print("Error: The Excel file must contain a column named 'Hero'.")
        else:
            # Get the list of heroes, dropping any empty values
            heroes_to_scrape = df_input['Hero'].dropna().unique().tolist()
            
            print(f"Found {len(heroes_to_scrape)} unique heroes in {input_filename}.")
            print("Starting extraction...")

            scraped_data = []

            # 3. SCRAPE DATA
            for hero in heroes_to_scrape:
                print(f"Processing: {hero}...")
                data = extract_hero_stats(hero)
                
                if data:
                    scraped_data.append(data)
                else:
                    # If scraping failed, we still add a row so we don't lose the hero name
                    scraped_data.append({
                        "Hero Name": hero,
                        "Durability": "Not Found",
                        "Control Effect": "Not Found",
                        "Offense": "Not Found"
                    })
                
                # Sleep to be polite to the server
                time.sleep(1)

            # 4. MERGE AND SAVE
            # Create a DataFrame from the scraped results
            df_stats = pd.DataFrame(scraped_data)
            
            # Merge the original input with the new stats based on the Hero name
            # 'left_on' is the column in the original file, 'right_on' is in the scraped data
            df_final = pd.merge(df_input, df_stats, left_on='Hero', right_on='Hero Name', how='left')
            
            # Drop the redundant 'Hero Name' column from the scraped data (since we already have 'Hero')
            df_final = df_final.drop(columns=['Hero Name'])

            # Save to Excel
            df_final.to_excel(output_filename, index=False)
            print(f"\nDone! Data saved to {output_filename}")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")