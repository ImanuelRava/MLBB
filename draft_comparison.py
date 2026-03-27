import streamlit as st
from hero_data import HERO_DATA
from utils import display_icon_50px
from hero_comparison import render_analytics_panel

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
    
    st.session_state.comp_search = ""

def render_comparison_mode(hero_stats):
    # Initialize target side if not exists
    if 'comp_target_side' not in st.session_state:
        st.session_state.comp_target_side = "Blue"

    if 'warning_msg' in st.session_state:
        st.warning(st.session_state.warning_msg)
        del st.session_state.warning_msg

    # ==========================================
    # ROW 1: DRAFT (TEAMS) & ANALYTICS
    # ==========================================
    col_draft, col_analytics = st.columns([1, 1.2])

    with col_draft:
        st.markdown("### Teams")
        
        def render_side_column(side_color, side_name, team_list):
            st.markdown(f"### {side_name} Side")
            st.markdown("Picks")
            pick_cols = st.columns(5)
            for i in range(5):
                with pick_cols[i]:
                    if i < len(team_list):
                        hero = team_list[i]
                        display_icon_50px(hero)
                        
                        if st.button("🗑️", key=f"rem_{side_name}_{i}", help="Remove Hero"):
                            if side_name == "Blue":
                                st.session_state.blue_team.pop(i)
                            else:
                                st.session_state.red_team.pop(i)
                            st.rerun()
                    else:
                        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

        render_side_column("blue", "Blue", st.session_state.blue_team)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        render_side_column("red", "Red", st.session_state.red_team)

    with col_analytics:
        render_analytics_panel(hero_stats, st.session_state.blue_team, st.session_state.red_team, [], [])

    # ==========================================
    # ROW 2: HERO SELECTION (Full Width)
    # ==========================================
    st.markdown("---")
    st.markdown("### Hero Selection")
    
    # CSS for active target button
    active_blue_css = """
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(1) button {
        background-color: #2196F3 !important;
        color: white !important;
        border: none !important;
    }
    """
    active_red_css = """
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) > div:nth-child(2) button {
        background-color: #F44336 !important;
        color: white !important;
        border: none !important;
    }
    """

    if st.session_state.comp_target_side == "Blue":
        st.markdown(f"<style>{active_blue_css}</style>", unsafe_allow_html=True)
    else:
        st.markdown(f"<style>{active_red_css}</style>", unsafe_allow_html=True)
    
    # Row 2.1: Buttons and Search
    col_t1, col_t2, col_search = st.columns([1, 1, 4])
    
    with col_t1:
        if st.button("Add to Blue", use_container_width=True):
            st.session_state.comp_target_side = "Blue"
            st.rerun()
            
    with col_t2:
        if st.button("Add to Red", use_container_width=True):
            st.session_state.comp_target_side = "Red"
            st.rerun()
            
    with col_search:
        search_query = st.text_input("🔍 Search Hero...", label_visibility="collapsed", key="comp_search")

    # Row 2.2: Filters
    # FIX: Added None checks to prevent sorting errors
    roles = set()
    lanes = set()
    for hero_info in HERO_DATA.values():
        r1 = hero_info.get("Role 1")
        r2 = hero_info.get("Role 2")
        l1 = hero_info.get("Lane 1")
        l2 = hero_info.get("Lane 2")
        
        if r1 and r1 != "N/A": roles.add(r1)
        if r2 and r2 != "N/A": roles.add(r2)
        if l1 and l1 != "N/A": lanes.add(l1)
        if l2 and l2 != "N/A": lanes.add(l2)
            
    sorted_roles = sorted(list(roles))
    sorted_lanes = sorted(list(lanes))
    
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_role = st.selectbox("Filter by Role", ["All"] + sorted_roles, key="comp_role_filter")
    with col_filter2:
        selected_lane = st.selectbox("Filter by Lane", ["All"] + sorted_lanes, key="comp_lane_filter")

    # Filter heroes
    used = set(st.session_state.blue_team + st.session_state.red_team)
    available_heroes = [h for h in HERO_DATA.keys() if h not in used]
    
    # Apply Search Filter
    if search_query: 
        available_heroes = [h for h in available_heroes if search_query.lower() in h.lower()]
    
    # Apply Role Filter
    if selected_role != "All":
        available_heroes = [
            h for h in available_heroes 
            if HERO_DATA[h].get("Role 1") == selected_role or HERO_DATA[h].get("Role 2") == selected_role
        ]
        
    # Apply Lane Filter
    if selected_lane != "All":
        available_heroes = [
            h for h in available_heroes 
            if HERO_DATA[h].get("Lane 1") == selected_lane or HERO_DATA[h].get("Lane 2") == selected_lane
        ]

    # Display Heroes Grid
    if not available_heroes:
        st.info("All heroes picked or none match search.")
    else:
        for i in range(0, len(available_heroes), 8):
            cols = st.columns(8)
            batch = available_heroes[i:i+8]
            for j, hero in enumerate(batch):
                with cols[j]:
                    display_icon_50px(hero)
                    st.button(hero, key=f"comp_btn_{hero}", use_container_width=True, 
                               on_click=handle_comparison_selection, args=(hero,))