import streamlit as st
from hero_data import HERO_DATA

# --- LOGIC ---

def generate_seq(bans):
    s = []
    if bans == 5:
        s.extend([('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red')])
        s.extend([('Pick', 'Blue'), ('Pick', 'Red'), ('Pick', 'Red'), ('Pick', 'Blue'), ('Pick', 'Blue'), ('Pick', 'Red')])
        s.extend([('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue')])
        s.extend([('Pick', 'Red'), ('Pick', 'Blue'), ('Pick', 'Blue'), ('Pick', 'Red')])
    else:
        for _ in range(bans):
            s.append(('Ban', 'Blue'))
            s.append(('Ban', 'Red'))
        pick_order = ['Blue', 'Red', 'Red', 'Blue', 'Blue', 'Red', 'Red', 'Blue', 'Blue', 'Red']
        s.extend([('Pick', t) for t in pick_order])
    return s

def display_icon_50px(hero_name):
    """Helper to display a consistent 50px icon or a placeholder."""
    try:
        st.image(f"{hero_name}.png", width=50)
    except:
        # Fallback if image is missing
        st.markdown(f"""
            <div style='width: 50px; height: 50px; background-color: #333; 
                        display: flex; align-items: center; justify-content: center; 
                        border-radius: 5px; font-size: 10px; color: #aaa; margin: 0 auto;'>
                {hero_name[:2]}
            </div>
        """, unsafe_allow_html=True)

# --- STREAMLIT APP ---

def main():
    st.set_page_config(page_title="Voltaire.Draft", layout="wide")

    # 1. Initialize Session State
    if 'step_index' not in st.session_state:
        st.session_state.step_index = 0
        st.session_state.blue_team = []
        st.session_state.red_team = []
        st.session_state.blue_bans = []  
        st.session_state.red_bans = []   
        st.session_state.ban_mode = 5

    # 2. Determine current turn
    sequence = generate_seq(st.session_state.ban_mode)
    total_steps = len(sequence)
    
    current_action, current_side = None, None
    if st.session_state.step_index < total_steps:
        current_action, current_side = sequence[st.session_state.step_index]

    # 3. Apply Dark Mode CSS
    st.markdown("""
        <style>
        .stApp {
            background-color: #111111;
            color: white;
        }
        /* Adjust standard Streamlit elements */
        h1, h2, h3, p, div, span, label {
            color: white !important;
        }
        
        /* BUTTON STYLING: Gray Background, White Text */
        div.stButton > button {
            color: white !important;
            background-color: #555555 !important; /* Gray */
            border-color: #555555 !important;
        }
        div.stButton > button:hover {
            color: white !important;
            background-color: #777777 !important; /* Lighter gray on hover */
            border-color: #777777 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 4. TOP BAR: Watermark & Settings
    col_header, col_settings = st.columns([3, 1])
    
    with col_header:
        st.markdown("<h1 style='text-align: left; color: #FF4B4B;'>Voltaire.Draft</h1>", unsafe_allow_html=True)

    with col_settings:
        # Ban Mode Selection (Buttons)
        b3, b5, rst = st.columns([1, 1, 1])
        
        disabled = st.session_state.step_index > 0
        
        with b3:
            if st.button("3 Bans", disabled=disabled, use_container_width=True):
                st.session_state.ban_mode = 3
                st.rerun()
        
        with b5:
            if st.button("5 Bans", disabled=disabled, use_container_width=True):
                st.session_state.ban_mode = 5
                st.rerun()
        
        with rst:
            if st.button("Reset", use_container_width=True):
                st.session_state.step_index = 0
                st.session_state.blue_team = []
                st.session_state.red_team = []
                st.session_state.blue_bans = []
                st.session_state.red_bans = []
                st.rerun()

    # 5. 3-COLUMN LAYOUT
    col_left, col_mid, col_right = st.columns([1, 2, 1], gap="small")

    # --- HELPER FOR SIDE COLUMN RENDERING ---
    def render_side_column(side_color, side_name, bans_list, team_list, is_active):
        """
        Renders the side column with stable header, single line bans, and single line picks.
        """
        # --- HEADER (Stable Height) ---
        st.markdown(f"### {side_name} Side")
        
        bar_color = side_color if is_active else "#555"
        st.markdown(f"""
            <div style='height: 4px; background-color: {bar_color}; border-radius: 2px; margin: 10px 0 20px 0;'></div>
        """, unsafe_allow_html=True)
        
        # --- BANS (Single Line) ---
        st.markdown("**Bans**")
        total_bans = 5 if st.session_state.ban_mode == 5 else 3
        ban_cols = st.columns(total_bans)
        
        for i in range(total_bans):
            with ban_cols[i]:
                if i < len(bans_list):
                    display_icon_50px(bans_list[i])
                else:
                    # Placeholder for stability
                    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

        # SEPARATION LINE
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 15px 0; border-color: #333;'>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # --- PICKS (Single Line - Always 5) ---
        st.markdown("**Picks**")
        pick_cols = st.columns(5)
        
        for i in range(5):
            with pick_cols[i]:
                if i < len(team_list):
                    display_icon_50px(team_list[i])
                else:
                    # Placeholder for stability
                    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

    # --- LEFT COLUMN: BLUE SIDE ---
    with col_left:
        is_blue_turn = (current_side == "Blue")
        render_side_column("blue", "🔵 Blue", st.session_state.blue_bans, st.session_state.blue_team, is_blue_turn)

    # --- CENTER COLUMN: HERO POOL ---
    with col_mid:
        if st.session_state.step_index < total_steps:
            st.markdown(f"### Select to **{current_action}** ({current_side})")
            
            # --- SEARCH BAR ---
            search_query = st.text_input("🔍 Search Hero...", "")
            
            # Filter available heroes
            used = set(st.session_state.blue_team + st.session_state.red_team + st.session_state.blue_bans + st.session_state.red_bans)
            available_heroes = [h for h in HERO_DATA.keys() if h not in used]
            
            # Filter by search query (Case insensitive)
            if search_query:
                available_heroes = [h for h in available_heroes if search_query.lower() in h.lower()]
            
            if not available_heroes:
                st.info("No heroes found matching your search.")
            else:
                # Create Grid (4 columns per row)
                for i in range(0, len(available_heroes), 4):
                    cols = st.columns(4)
                    batch = available_heroes[i:i+4]
                    
                    for j, hero in enumerate(batch):
                        with cols[j]:
                            # 1. Display 50px Icon
                            display_icon_50px(hero)
                            
                            # 2. Display Button
                            if st.button(hero, key=f"btn_{hero}", use_container_width=True):
                                # --- UPDATE LOGIC ---
                                if current_action == "Pick":
                                    if current_side == "Blue":
                                        st.session_state.blue_team.append(hero)
                                    else:
                                        st.session_state.red_team.append(hero)
                                else: # Ban
                                    if current_side == "Blue":
                                        st.session_state.blue_bans.append(hero)
                                    else:
                                        st.session_state.red_bans.append(hero)
                                
                                st.session_state.step_index += 1
                                st.rerun()
                            
        else:
            st.success("🎉 **Draft Complete!**")

    # --- RIGHT COLUMN: RED SIDE ---
    with col_right:
        is_red_turn = (current_side == "Red")
        render_side_column("red", "🔴 Red", st.session_state.red_bans, st.session_state.red_team, is_red_turn)

if __name__ == "__main__":
    main()