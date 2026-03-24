import streamlit as st
from hero_data import HERO_DATA
from utils import display_icon_50px
from hero_comparison import render_analytics_panel

# Callback function for Comparison Mode
def handle_comparison_selection(hero_name):
    target = st.session_state.comp_target_side
    
    if target == "Blue":
        if len(st.session_state.blue_team) < 5:
            st.session_state.blue_team.append(hero_name)
        else:
            st.session_state.warning_msg = "Blue team is full (5/5)"
    else:
        if len(st.session_state.red_team) < 5:
            st.session_state.red_team.append(hero_name)
        else:
            st.session_state.warning_msg = "Red team is full (5/5)"
    
    # Clear the search bar safely via callback
    st.session_state.comp_search = ""

def render_comparison_mode(hero_stats):
    # Display warning if any (from callback)
    if 'warning_msg' in st.session_state:
        st.warning(st.session_state.warning_msg)
        del st.session_state.warning_msg

    # ==========================================
    # ROW 1: DRAFT (TEAMS) & ANALYTICS
    # ==========================================
    col_draft, col_analytics = st.columns([1, 1.2])

    with col_draft:
        st.markdown("### Teams")
        
        # Helper to render a single team column
        def render_side_column(side_color, side_name, team_list):
            st.markdown(f"### {side_name} Side")
            st.markdown("Picks")
            pick_cols = st.columns(5)
            for i in range(5):
                with pick_cols[i]:
                    if i < len(team_list):
                        hero = team_list[i]
                        display_icon_50px(hero)
                        
                        # Add Remove Button
                        if st.button("🗑️", key=f"rem_{side_name}_{i}", help="Remove Hero"):
                            if side_name == "Blue":
                                st.session_state.blue_team.pop(i)
                            else:
                                st.session_state.red_team.pop(i)
                            st.rerun()
                    else:
                        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

        # Blue Team
        render_side_column("blue", "Blue", st.session_state.blue_team)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Red Team (Below Blue)
        render_side_column("red", "Red", st.session_state.red_team)

    with col_analytics:
        # ANALYTICS (Right Side)
        render_analytics_panel(hero_stats, st.session_state.blue_team, st.session_state.red_team, [], [])

    # ==========================================
    # ROW 2: HERO SELECTION (Full Width)
    # ==========================================
    st.markdown("---")
    st.markdown("### Hero Selection")
    
    # Controls: Target Side & Search
    col_t1, col_t2, col_search = st.columns([1, 1, 4])
    
    with col_t1:
        if st.button("Add to Blue", use_container_width=True, type="primary" if st.session_state.comp_target_side == "Blue" else "secondary"):
            st.session_state.comp_target_side = "Blue"
            st.rerun()
            
    with col_t2:
        if st.button("Add to Red", use_container_width=True, type="primary" if st.session_state.comp_target_side == "Red" else "secondary"):
            st.session_state.comp_target_side = "Red"
            st.rerun()
            
    with col_search:
        search_query = st.text_input("🔍 Search Hero...", label_visibility="collapsed", key="comp_search")

    # Hero Grid
    used = set(st.session_state.blue_team + st.session_state.red_team)
    available_heroes = [h for h in HERO_DATA.keys() if h not in used]
    if search_query: available_heroes = [h for h in available_heroes if search_query.lower() in h.lower()]

    if not available_heroes:
        st.info("All heroes picked or none match search.")
    else:
        for i in range(0, len(available_heroes), 8): # Increased columns to 8 for full width
            cols = st.columns(8)
            batch = available_heroes[i:i+8]
            for j, hero in enumerate(batch):
                with cols[j]:
                    display_icon_50px(hero)
                    # Use on_click callback
                    st.button(hero, key=f"comp_btn_{hero}", use_container_width=True, 
                               on_click=handle_comparison_selection, args=(hero,))