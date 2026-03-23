import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import unquote

def download_fandom_icons():
    # URL for the Fandom List of Heroes
    url = "https://mobile-legends.fandom.com/wiki/List_of_heroes"
    
    # Folder to save icons
    save_folder = "ml_fandom_icons"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    print(f"Accessing {url}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to retrieve page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # On Fandom "List of heroes" pages, data is usually in a table with class "wikitable"
    # Or we can just look for all images inside links that point to hero pages
    images_downloaded = 0

    # Find all table rows or hero containers
    # Strategy: Find all links (<a>) that have an image inside, and check if the link goes to a hero page
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href', '')
        
        # Filter for hero links (usually /wiki/HeroName)
        # We ignore links that have ':' like 'File:', 'Category:', etc.
        if href.startswith('/wiki/') and ':' not in href:
            
            img_tag = a_tag.find('img')
            if img_tag:
                src = img_tag.get('data-src') or img_tag.get('src')
                
                if not src:
                    continue

                # Fandom uses dynamic scaling (e.g., /scale-to-width-down/50)
                # We want the original quality, so we strip the resizing parameters.
                # Example URL: .../images/.../Hero.png/revision/latest/scale-to-width-down/50?cb=...
                # Target URL:  .../images/.../Hero.png/revision/latest?cb=...
                
                if '/scale-to-width-down' in src:
                    src = src.split('/scale-to-width-down')[0]
                
                # Ensure it starts with https
                if src.startswith('//'):
                    src = 'https:' + src
                
                # Extract hero name for the filename
                # We try to get it from the alt text (usually "HeroName icon") or the URL
                alt_text = img_tag.get('alt', '')
                filename = unquote(src.split('/')[-1].split('?')[0])
                
                # If the filename is weird (like "revision?cb=..."), let's use the alt text
                if 'revision' in filename or len(filename) < 3:
                    if alt_text:
                        # Clean up alt text (e.g., "Miya icon" -> "Miya.png")
                        clean_name = alt_text.replace(' ', '_').replace('_icon', '')
                        filename = f"{clean_name}.png"
                    else:
                        # Fallback: use the href
                        filename = href.split('/')[-1] + ".png"

                file_path = os.path.join(save_folder, filename)
                
                # Skip if already exists
                if os.path.exists(file_path):
                    continue

                print(f"Downloading: {alt_text} -> {filename}")
                
                try:
                    img_resp = requests.get(src, headers=headers, stream=True)
                    img_resp.raise_for_status()
                    
                    with open(file_path, 'wb') as f:
                        for chunk in img_resp.iter_content(1024):
                            f.write(chunk)
                    
                    images_downloaded += 1
                    # Small delay to be polite
                    time.sleep(0.2)
                    
                except Exception as e:
                    print(f"Error downloading {filename}: {e}")

    print(f"\nDone! Downloaded {images_downloaded} hero icons to '{save_folder}'.")

if __name__ == "__main__":
    download_fandom_icons()