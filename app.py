import streamlit as st
import os
import base64
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voltaire Draft", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

# --- STATE MANAGEMENT ---
def init_session():
    if 'seq' not in st.session_state:
        st.session_state.seq = [] 
        st.session_state.step = 0
        st.session_state.selected_hero = None
        st.session_state.active_filter = "All"
        st.session_state.search_query = ""
        st.session_state.theme = "Dark"
        st.session_state.turn_duration = 30
        st.session_state.turn_start_time = 0
        reset_draft_lists()

def reset_draft_lists():
    st.session_state.blue_bans = []
    st.session_state.red_bans = []
    st.session_state.blue_picks = []
    st.session_state.red_picks = []
    st.session_state.pool = list(ALL_HEROES)
    st.session_state.selected_hero = None

def toggle_theme():
    st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"

# --- DATA SETUP ---
HERO_DATA = {
    # Tanks
    "Akai": "Tank", "Atlas": "Tank", "Baxia": "Tank", "Belerick": "Tank", "Franco": "Tank", 
    "Gatotkaca": "Tank", "Gloo": "Tank", "Grock": "Tank", "Hylos": "Tank", "Johnson": "Tank", 
    "Khufra": "Tank", "Minotaur": "Tank", "Tigreal": "Tank", "Uranus": "Tank",
    "Alice": "Tank", "Barats": "Tank", "Edith": "Tank", "Esmeralda": "Tank",
    
    # Fighters
    "Aldous": "Fighter", "Alpha": "Fighter", "Argus": "Fighter", "Aulus": "Fighter", "Badang": "Fighter", 
    "Balmond": "Fighter", "Bane": "Fighter", "Chou": "Fighter", "Cici": "Fighter", "Dyrroth": "Fighter", 
    "Fredrinn": "Fighter", "Freya": "Fighter", "Guinevere": "Fighter", "Hilda": "Fighter", 
    "Jawhead": "Fighter", "Khaleed": "Fighter", "Lapu-Lapu": "Fighter", "Leomord": "Fighter", 
    "Lukas": "Fighter", "Martis": "Fighter", "Masha": "Fighter", "Paquito": "Fighter", "Phoveus": "Fighter", 
    "Ruby": "Fighter", "Roger": "Fighter", "Silvanna": "Fighter", "Sun": "Fighter", 
    "Sora": "Fighter", "Terizla": "Fighter", "Thamuz": "Fighter", "X.Borg": "Fighter", 
    "Yu Zhong": "Fighter", "Zilong": "Fighter", "Alucard": "Fighter", "Arlott": "Fighter",
    
    # Assassins
    "Aamon": "Assassin", "Benedetta": "Assassin", "Fanny": "Assassin", "Gusion": "Assassin", 
    "Hanzo": "Assassin", "Harley": "Assassin", "Hayabusa": "Assassin", "Helcurt": "Assassin", 
    "Joy": "Assassin", "Julian": "Assassin", "Karina": "Assassin", "Lancelot": "Assassin", 
    "Ling": "Assassin", "Natalia": "Assassin", "Nolan": "Assassin", "Saber": "Assassin", 
    "Selena": "Assassin", "Suyou": "Assassin", "Yi Sun-shin": "Assassin", "Yin": "Assassin",
    
    # Mages
    "Aurora": "Mage", "Cecilion": "Mage", "Chang'e": "Mage", "Cyclops": "Mage", 
    "Eudora": "Mage", "Gord": "Mage", "Harith": "Mage", "Kadita": "Mage", "Kagura": "Mage", 
    "Luo Yi": "Mage", "Lylia": "Mage", "Lunox": "Mage", "Nana": "Mage", "Novaria": "Mage", 
    "Odette": "Mage", "Pharsa": "Mage", "Valentina": "Mage", "Vale": "Mage", "Valir": "Mage", 
    "Vexana": "Mage", "Xavier": "Mage", "Yve": "Mage", "Zetian": "Mage", "Zhask": "Mage", 
    "Zhuxin": "Mage",
    
    # Marksmen
    "Beatrix": "Marksman", "Brody": "Marksman", "Bruno": "Marksman", "Claude": "Marksman", 
    "Clint": "Marksman", "Granger": "Marksman", "Hanabi": "Marksman", "Ixia": "Marksman", 
    "Irithel": "Marksman", "Karrie": "Marksman", "Kimmy": "Marksman", "Layla": "Marksman", 
    "Lesley": "Marksman", "Melissa": "Marksman", "Miya": "Marksman", "Moskov": "Marksman", 
    "Natan": "Marksman", "Obsidia": "Marksman", "Popol and Kupa": "Marksman", "Wanwan": "Marksman",
    
    # Supports
    "Angela": "Support", "Carmilla": "Support", "Chip": "Support", "Diggie": "Support", 
    "Estes": "Support", "Faramis": "Support", "Floryn": "Support", "Kaja": "Support", 
    "Kalea": "Support", "Lolita": "Support", "Marcel": "Support", "Mathilda": "Support", 
    "Rafaela": "Support"
}

ALL_HEROES = sorted(list(HERO_DATA.keys()))

# --- LOGIC ---

def generate_seq(bans):
    s = []
    if bans == 5:
        # First Ban Phase
        s.append(('Ban', 'Blue'))
        s.append(('Ban', 'Red'))
        s.append(('Ban', 'Blue'))
        s.append(('Ban', 'Red'))
        s.append(('Ban', 'Blue'))
        s.append(('Ban', 'Red'))
        # First Pick Phase
        s.append(('Pick', 'Blue'))
        s.append(('Pick', 'Red'))
        s.append(('Pick', 'Red'))
        s.append(('Pick', 'Blue'))
        s.append(('Pick', 'Blue'))
        s.append(('Pick', 'Red'))
        # Second Ban Phase
        s.append(('Ban', 'Red'))
        s.append(('Ban', 'Blue'))
        s.append(('Ban', 'Red'))
        s.append(('Ban', 'Blue'))
        # Second Pick Phase
        s.append(('Pick', 'Red'))
        s.append(('Pick', 'Blue'))
        s.append(('Pick', 'Blue'))
        s.append(('Pick', 'Red'))
    else:
        # Standard Mode (3 Bans)
        for _ in range(bans):
            s.append(('Ban', 'Blue'))
            s.append(('Ban', 'Red'))
        # Pick Phase
        order = ['Blue', 'Red', 'Red', 'Blue', 'Blue', 'Red', 'Red', 'Blue', 'Blue', 'Red']
        for t in order:
            s.append(('Pick', t))
    return s

def start_game(ban_count):
    reset_draft_lists()
    st.session_state.seq = generate_seq(ban_count)
    st.session_state.step = 0
    # Keep 50s for Tournament (5 bans) as it is a longer game
    st.session_state.turn_duration = 50 if ban_count == 5 else 30
    st.session_state.turn_start_time = time.time()

def exit_game():
    st.session_state.seq = []
    st.session_state.step = 0
    st.session_state.selected_hero = None
    reset_draft_lists()

def select_hero(hero):
    st.session_state.selected_hero = hero

def confirm_action():
    hero = st.session_state.selected_hero
    if not hero: return
    action, team = st.session_state.seq[st.session_state.step]
    
    if action == 'Ban':
        if team == 'Blue': st.session_state.blue_bans.append(hero)
        else: st.session_state.red_bans.append(hero)
    else:
        if team == 'Blue': st.session_state.blue_picks.append(hero)
        else: st.session_state.red_picks.append(hero)
    
    st.session_state.pool.remove(hero)
    st.session_state.step += 1
    st.session_state.selected_hero = None
    st.session_state.turn_start_time = time.time()

# --- IMAGE HANDLING ---
def get_local_image_path(name):
    return f"{name}.png"

def get_base64_image(name):
    file_path = f"{name}.png"
    theme_bg = "e2e8f0" if st.session_state.theme == "Light" else "0f3460"
    theme_text = "1a202c" if st.session_state.theme == "Light" else "ffffff"
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    else:
        return f"https://via.placeholder.com/70x70/{theme_bg}/{theme_text}?text={name[0]}"

# --- UI RENDERERS ---

def get_theme_css():
    if st.session_state.theme == "Dark":
        bg_color, panel_bg, text_color = "#1a1a2e", "rgba(15, 52, 96, 0.8)", "#ffffff"
        border_color, header_bg, input_bg = "#4a4a6a", "#16213e", "#0f3460"
        grid_bg, btn_bg, btn_text = "#0f3460", "#0f3460", "#ffffff"
        btn_border, btn_hover = "#4a4a6a", "#e94560"
        primary_btn, accent_btn = "#3498db", "#e94560"
    else:
        bg_color, panel_bg, text_color = "#f7fafc", "rgba(255, 255, 255, 0.9)", "#2d3748"
        border_color, header_bg, input_bg = "#cbd5e0", "#ffffff", "#edf2f7"
        grid_bg, btn_bg, btn_text = "#edf2f7", "#edf2f7", "#2d3748"
        btn_border, btn_hover = "#cbd5e0", "#e2e8f0"
        primary_btn, accent_btn = "#2b6cb0", "#e53e3e"

    return f"""
    <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        #MainMenu, footer, header {{ visibility: hidden; }}
        
        /* Buttons */
        .stButton > button {{
            color: {btn_text};
            background-color: {btn_bg};
            border: 1px solid {btn_border};
            border-radius: 6px;
            transition: all 0.3s;
        }}
        .stButton > button:hover {{ border-color: {btn_hover}; background-color: {btn_hover}; }}
        
        /* Primary Button */
        div[data-testid="stVerticalBlock"] > div:has(> button[kind="primary"]) > button {{
            background-color: {primary_btn} !important; border-color: {primary_btn} !important; color: white !important;
        }}
        
        /* Inputs & Search Text Fix */
        .stTextInput > div > div > input, .stTextInput > label {{
            color: {text_color} !important;
            background-color: {input_bg} !important;
            border: 1px solid {border_color} !important;
        }}
        
        /* Header */
        .brand-header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 20px; background-color: {header_bg};
            border-bottom: 2px solid {border_color}; margin-bottom: 20px; color: {text_color};
        }}
        .brand-title {{ font-size: 24px; font-weight: bold; letter-spacing: 2px; color: {text_color}; text-decoration: none !important; }}
        .brand-title span {{ color: #e94560; }}
        
        /* Team Titles */
        .team-title {{ font-size: 18px; font-weight: bold; text-align: center; margin-bottom: 8px; color: {text_color}; }}
        
        /* Hero Grid */
        .hero-grid-item {{ display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 5px; cursor: pointer; }}
        .hero-circle {{
            width: 60px; height: 60px; border-radius: 50%; border: 2px solid {border_color};
            object-fit: cover; background-color: {grid_bg}; transition: transform 0.2s;
        }}
        .hero-name {{ font-size: 10px; margin-top: 4px; color: {text_color}; }}
        
        /* Selected Hero */
        .hero-selected .hero-circle {{
            border-color: {accent_btn}; box-shadow: 0 0 10px {accent_btn}; transform: scale(1.1);
        }}
        
        /* Team Panels */
        .team-panel {{
            background-color: {panel_bg}; border-radius: 8px; padding: 10px; height: 100%;
            border: 1px solid {border_color}; display: flex; flex-direction: column; align-items: center;
        }}

        /* Overlay Button */
        div:has(> div > button[data-testid*="sel_"]) {{ position: relative !important; }}
        button[data-testid*="sel_"] {{
            position: absolute !important; top: 0; left: 0; width: 100%; height: 100%;
            opacity: 0 !important; z-index: 999; border: none !important; background: transparent !important;
            cursor: pointer; margin: 0 !important; padding: 0 !important;
        }}
    </style>
    """

def render_header():
    col_brand, col_mode3, col_mode5, col_theme, col_exit = st.columns([2, 1.2, 1.2, 1, 1])
    with col_brand:
        st.markdown("<div class='brand-title'>VOLTAIRE<span>.DRAFT</span></div>", unsafe_allow_html=True)
    with col_mode3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Standard (3 Bans)", key="mode_3", use_container_width=True, on_click=lambda: start_game(3)): pass
    with col_mode5:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Tournament (5 Bans)", key="mode_5", use_container_width=True, on_click=lambda: start_game(5)): pass
    with col_theme:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"Theme: {st.session_state.theme}", key="theme_btn", use_container_width=True, on_click=toggle_theme): pass
    with col_exit:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Exit", key="exit_btn", use_container_width=True, on_click=exit_game)

def render_main_ui():
    is_running = len(st.session_state.seq) > 0 and st.session_state.step < len(st.session_state.seq)
    
    current_action, current_team = None, None
    remaining_time = 0
    blue_title = "BLUE SIDE"
    red_title = "RED SIDE"
    
    if is_running:
        current_action, current_team = st.session_state.seq[st.session_state.step]
        elapsed = time.time() - st.session_state.turn_start_time
        remaining_time = max(0, st.session_state.turn_duration - elapsed)
        timer_text = f" ({int(remaining_time)}s)" if remaining_time > 0 else " (TIME UP)"
        
        # Update Titles with Turn Info
        turn_info = f": {current_action}{timer_text}"
        if current_team == "Blue":
            blue_title += f'<span style="color:#3498db">{turn_info}</span>'
            red_title += '<span style="opacity:0.5"> (Waiting)</span>'
        else:
            blue_title += '<span style="opacity:0.5"> (Waiting)</span>'
            red_title += f'<span style="color:#e74c3c">{turn_info}</span>'
    elif len(st.session_state.seq) > 0:
        blue_title += '<span style="color:#2ecc71"> (COMPLETED)</span>'
        red_title += '<span style="color:#2ecc71"> (COMPLETED)</span>'
    else:
        blue_title += '<span style="opacity:0.5"> (Select Mode)</span>'
        red_title += '<span style="opacity:0.5"> (Select Mode)</span>'

    col_blue, col_grid, col_red = st.columns([1, 3, 1])

    # --- BLUE PANEL ---
    with col_blue:
        st.markdown("<div class='team-panel'>", unsafe_allow_html=True)
        st.markdown(f"<div class='team-title'>{blue_title}</div>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:10px'>BANS</small>", unsafe_allow_html=True)
        # Reduced image size to 32px for compactness
        for h in st.session_state.blue_bans: st.image(get_local_image_path(h), width=32)
        st.markdown("<hr style='margin: 5px 0'>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:10px'>PICKS</small>", unsafe_allow_html=True)
        for h in st.session_state.blue_picks: st.image(get_local_image_path(h), width=32)
        if is_running and current_team == 'Blue' and st.session_state.selected_hero:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"CONFIRM {current_action}", key="confirm_blue", type="primary", use_container_width=True, on_click=confirm_action): pass
        st.markdown("</div>", unsafe_allow_html=True)

    # --- HERO GRID ---
    with col_grid:
        search = st.text_input("Search Hero...", value=st.session_state.search_query, key="search_input")
        st.session_state.search_query = search 
        
        roles = ["All", "Tank", "Fighter", "Assassin", "Mage", "Marksman", "Support"]
        cols_f = st.columns(len(roles))
        for i, r in enumerate(roles):
            with cols_f[i]:
                if st.button(r, key=f"f_{r}", use_container_width=True, disabled=st.session_state.active_filter == r):
                    st.session_state.active_filter = r
                    st.rerun()

        visible_heroes = [h for h in st.session_state.pool if 
                          (st.session_state.active_filter == "All" or HERO_DATA.get(h) == st.session_state.active_filter) and
                          (search.lower() in h.lower())]
        
        grid_cols = st.columns(7) # Increased to 7 columns for grid to make it more compact too
        for i, hero in enumerate(visible_heroes):
            with grid_cols[i % 7]:
                is_sel = st.session_state.selected_hero == hero
                sel_class = "hero-selected" if is_sel else ""
                img_src = get_base64_image(hero)
                
                card_html = f"""
                <div class="hero-grid-item {sel_class}">
                    <img src="{img_src}" class="hero-circle">
                    <div class="hero-name">{hero}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                st.button("", key=f"sel_{hero}", use_container_width=True, disabled=not is_running, on_click=lambda h=hero: select_hero(h))

    # --- RED PANEL ---
    with col_red:
        st.markdown("<div class='team-panel'>", unsafe_allow_html=True)
        st.markdown(f"<div class='team-title'>{red_title}</div>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:10px'>BANS</small>", unsafe_allow_html=True)
        for h in st.session_state.red_bans: st.image(get_local_image_path(h), width=32)
        st.markdown("<hr style='margin: 5px 0'>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:10px'>PICKS</small>", unsafe_allow_html=True)
        for h in st.session_state.red_picks: st.image(get_local_image_path(h), width=32)
        if is_running and current_team == 'Red' and st.session_state.selected_hero:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"CONFIRM {current_action}", key="confirm_red", type="primary", use_container_width=True, on_click=confirm_action): pass
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN APP LOOP ---
init_session()
st.markdown(get_theme_css(), unsafe_allow_html=True)

render_header()
render_main_ui()

if len(st.session_state.seq) > 0 and st.session_state.step < len(st.session_state.seq):
    time.sleep(1)
    st.rerun()