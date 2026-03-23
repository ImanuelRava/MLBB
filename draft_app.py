import streamlit as st
import pandas as pd
import altair as alt
from hero_data import HERO_DATA

# --- LOGIC FUNCTIONS ---

def generate_seq(bans):
    """Generates the draft sequence based on ban count."""
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
            <div style='width: 50px; height: 50px; background-color: #f0f2f6; 
                        display: flex; align-items: center; justify-content: center; 
                        border-radius: 5px; font-size: 10px; color: #555; margin: 0 auto;'>
                {hero_name[:2]}
            </div>
        """, unsafe_allow_html=True)

def get_advantage_explanations(blue_scores, red_scores):
    """Compares stats to generate natural language advantages."""
    stats_cols = ['Durability', 'Offense', 'Control Effect', 'Mobility']
    blue_adv = []
    red_adv = []

    for i, stat in enumerate(stats_cols):
        b_val = blue_scores[i]
        r_val = red_scores[i]
        diff = b_val - r_val

        if diff >= 1.0:
            if stat == "Durability":
                blue_adv.append("Higher Durability (Tankier front line)")
            elif stat == "Offense":
                blue_adv.append("Higher Offense (More burst damage)")
            elif stat == "Control Effect":
                blue_adv.append("Stronger Crowd Control (Better lockdown)")
            elif stat == "Mobility":
                blue_adv.append("Superior Mobility (Better rotations)")
        elif diff <= -1.0:
            if stat == "Durability":
                red_adv.append("Higher Durability (Tankier front line)")
            elif stat == "Offense":
                red_adv.append("Higher Offense (More burst damage)")
            elif stat == "Control Effect":
                red_adv.append("Stronger Crowd Control (Better lockdown)")
            elif stat == "Mobility":
                red_adv.append("Superior Mobility (Better rotations)")
            
    return blue_adv, red_adv

def analyze_draft(hero_stats, blue_team, red_team):
    """Calculates team stats based on the hero_stats DataFrame."""
    stats_cols = ['Durability', 'Offense', 'Control Effect', 'Mobility']
    
    blue_scores = [0.0] * len(stats_cols)
    red_scores = [0.0] * len(stats_cols)
    
    if blue_team:
        valid_blue = [h for h in blue_team if h in hero_stats.index]
        if valid_blue:
            df_blue = hero_stats.loc[valid_blue]
            blue_scores = df_blue[stats_cols].mean().tolist()

    if red_team:
        valid_red = [h for h in red_team if h in hero_stats.index]
        if valid_red:
            df_red = hero_stats.loc[valid_red]
            red_scores = df_red[stats_cols].mean().tolist()

    comp_df = pd.DataFrame({
        'Metric': stats_cols,
        'Blue': blue_scores,
        'Red': red_scores
    }).set_index('Metric')
    
    return comp_df, blue_scores, red_scores


# --- MAIN APP ---

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

    # 2. Load Data
    try:
        hero_stats = pd.DataFrame.from_dict(HERO_DATA, orient='index')
    except Exception as e:
        st.error(f"Error loading hero data: {e}")
        return

    # 3. Determine current turn
    sequence = generate_seq(st.session_state.ban_mode)
    total_steps = len(sequence)
    current_action, current_side = None, None
    if st.session_state.step_index < total_steps:
        current_action, current_side = sequence[st.session_state.step_index]

    # 4. CSS (White Background + Button Styling)
    st.markdown("""
        <style>
        /* Force White Background */
        .stApp {
            background-color: white;
        }
        
        /* Style Buttons */
        div.stButton > button {
            color: white !important;
            background-color: #555555 !important;
            border-color: #555555 !important;
            border-radius: 5px;
            white-space: nowrap;
        }
        div.stButton > button:hover {
            color: white !important;
            background-color: #777777 !important;
            border-color: #777777 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 5. TOP BAR
    col_header, col_settings = st.columns([3, 1])
    with col_header:
        st.markdown("<h1 style='text-align: left; color: #FF4B4B; margin: 0;'>Voltaire.Draft</h1>", unsafe_allow_html=True)

    with col_settings:
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

    st.markdown("<br>", unsafe_allow_html=True)

    # --- SECTION 1: TEAMS (Top Row) ---
    col_blue, col_red = st.columns(2, gap="large")

    def render_side_column(side_color, side_name, bans_list, team_list, is_active):
        st.markdown(f"### {side_name} Side")
        bar_color = side_color if is_active else "#cccccc"
        st.markdown(f"""
            <div style='height: 4px; background-color: {bar_color}; border-radius: 2px; margin: 5px 0 15px 0;'></div>
        """, unsafe_allow_html=True)
        
        # BANS (Removed Bold)
        st.markdown("Bans")
        total_bans = 5 if st.session_state.ban_mode == 5 else 3
        ban_cols = st.columns(total_bans)
        for i in range(total_bans):
            with ban_cols[i]:
                if i < len(bans_list):
                    display_icon_50px(bans_list[i])
                else:
                    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 10px 0; border-color: #ddd;'>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # PICKS (Removed Bold)
        st.markdown("Picks")
        pick_cols = st.columns(5)
        for i in range(5):
            with pick_cols[i]:
                if i < len(team_list):
                    display_icon_50px(team_list[i])
                else:
                    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

    with col_blue:
        is_blue_turn = (current_side == "Blue")
        render_side_column("blue", "🔵 Blue", st.session_state.blue_bans, st.session_state.blue_team, is_blue_turn)

    with col_red:
        is_red_turn = (current_side == "Red")
        render_side_column("red", "🔴 Red", st.session_state.red_bans, st.session_state.red_team, is_red_turn)

    # --- SECTION 2: HERO SELECTION ---
    st.markdown("---")
    
    if st.session_state.step_index < total_steps:
        # Robust Color Logic
        if current_action == "Pick":
            action_color = "green"
        elif current_action == "Ban":
            action_color = "orange"
        else:
            action_color = "black"

        # Render Text (No Bold)
        st.markdown(f"<h3 style='text-align: center; color: {action_color} !important;'>Select to {current_action} ({current_side})</h3>", unsafe_allow_html=True)
        
        search_query = st.text_input("🔍 Search Hero...", label_visibility="collapsed")
        
        used = set(st.session_state.blue_team + st.session_state.red_team + st.session_state.blue_bans + st.session_state.red_bans)
        available_heroes = [h for h in HERO_DATA.keys() if h not in used]
        
        if search_query:
            available_heroes = [h for h in available_heroes if search_query.lower() in h.lower()]
        
        if not available_heroes:
            st.info("No heroes found matching your search.")
        else:
            for i in range(0, len(available_heroes), 4):
                cols = st.columns(4)
                batch = available_heroes[i:i+4]
                for j, hero in enumerate(batch):
                    with cols[j]:
                        display_icon_50px(hero)
                        if st.button(hero, key=f"btn_{hero}", use_container_width=True):
                            if current_action == "Pick":
                                if current_side == "Blue":
                                    st.session_state.blue_team.append(hero)
                                else:
                                    st.session_state.red_team.append(hero)
                            else: 
                                if current_side == "Blue":
                                    st.session_state.blue_bans.append(hero)
                                else:
                                    st.session_state.red_bans.append(hero)
                            st.session_state.step_index += 1
                            st.rerun()
    else:
        # Removed Bold from Draft Complete
        st.success("🎉 Draft Complete!")

    # --- SECTION 3: ANALYSIS ---
    total_picks = len(st.session_state.blue_team) + len(st.session_state.red_team)
    
    if total_picks >= 2:
        st.markdown("---")
        
        stats_df, blue_scores, red_scores = analyze_draft(hero_stats, st.session_state.blue_team, st.session_state.red_team)
        blue_adv, red_adv = get_advantage_explanations(blue_scores, red_scores)
        
        with st.expander("📊 Draft Evaluation", expanded=True):
            c1, c2 = st.columns(2)
            
            with c1:
                # Removed Bold from Header
                st.write("Team Comparison (Avg Stats)")
                stats_df_long = stats_df.reset_index().melt(id_vars='Metric', var_name='Team', value_name='Score')
                
                chart = alt.Chart(stats_df_long).mark_bar().encode(
                    x=alt.X('Metric:N', title='Metric'),
                    y=alt.Y('Score:Q', title='Average Score', scale=alt.Scale(domain=[0, 10])),
                    xOffset='Team:N', 
                    color=alt.Color('Team:N', 
                                    scale=alt.Scale(domain=['Blue', 'Red'], range=['#1f77b4', '#d62728']),
                                    legend=None),
                    tooltip=['Metric', 'Team', 'Score']
                ).properties(
                    width='container',
                    height=300,
                    background='white'
                )
                st.altair_chart(chart, use_container_width=True)
            
            with c2:
                # Removed Bold from Header
                st.write("Team Analysis")
                st.markdown("<div style='margin-bottom: 10px; font-weight: bold; color: #1f77b4;'>🔵 Blue Team Advantages</div>", unsafe_allow_html=True)
                if blue_adv:
                    for adv in blue_adv:
                        st.markdown(f"- {adv}")
                else:
                    st.markdown("<small>No significant statistical advantage.</small>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("<div style='margin-bottom: 10px; font-weight: bold; color: #d62728;'>🔴 Red Team Advantages</div>", unsafe_allow_html=True)
                if red_adv:
                    for adv in red_adv:
                        st.markdown(f"- {adv}")
                else:
                    st.markdown("<small>No significant statistical advantage.</small>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
