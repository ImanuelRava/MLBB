import streamlit as st
from hero_data import HERO_DATA
from draft_logic import generate_seq
from utils import display_icon_50px
from hero_comparison import render_analytics_panel

def handle_hero_selection(hero_name, action, side):
    if action == "Pick":
        if side == "Blue":
            st.session_state.blue_team.append(hero_name)
        else:
            st.session_state.red_team.append(hero_name)
    else: 
        if side == "Blue":
            st.session_state.blue_bans.append(hero_name)
        else:
            st.session_state.red_bans.append(hero_name)
    
    st.session_state.step_index += 1
    st.session_state.sim_search = ""

def render_simulation_mode(hero_stats):
    sequence = generate_seq(st.session_state.ban_mode)
    total_steps = len(sequence)
    current_action, current_side = None, None
    
    if st.session_state.step_index < total_steps:
        current_action, current_side = sequence[st.session_state.step_index]

    col_blue, col_red = st.columns(2, gap="large")

    def render_side_column(side_color, side_name, team_list, bans_list, is_active):
        st.markdown(f"### {side_name} Side")
        bar_color = side_color if is_active else "#cccccc"
        st.markdown(f"""
            <div style='height: 4px; background-color: {bar_color}; border-radius: 2px; margin: 5px 0 15px 0;'></div>
        """, unsafe_allow_html=True)
        
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
        render_side_column("blue", "Blue", st.session_state.blue_team, st.session_state.blue_bans, is_blue_turn)

    with col_red:
        is_red_turn = (current_side == "Red")
        render_side_column("red", "Red", st.session_state.red_team, st.session_state.red_bans, is_red_turn)

    st.markdown("---")
    
    # Display current turn instruction
    if st.session_state.step_index < total_steps:
        if current_action == "Pick": action_color = "green"
        elif current_action == "Ban": action_color = "orange"
        else: action_color = "black"
        st.markdown(f"<h3 style='text-align: center; color: {action_color} !important;'>Select to {current_action} ({current_side})</h3>", unsafe_allow_html=True)
    else:
        st.success("🎉 Draft Complete!")
    
    # --- Role & Lane Filter Logic ---
    # Extract unique roles and lanes from HERO_DATA
    roles = set()
    lanes = set()
    for hero_info in HERO_DATA.values():
        roles.add(hero_info["Role 1"])
        if hero_info["Role 2"] != "N/A":
            roles.add(hero_info["Role 2"])
        
        lanes.add(hero_info["Lane 1"])
        if hero_info["Lane 2"] != "N/A":
            lanes.add(hero_info["Lane 2"])
            
    sorted_roles = sorted(list(roles))
    sorted_lanes = sorted(list(lanes))
    
    # Search Bar (Above)
    search_query = st.text_input("🔍 Search Hero...", label_visibility="visible", key="sim_search")
    
    # Filters (Below)
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_role = st.selectbox("Filter by Role", ["All"] + sorted_roles, key="role_filter")
    with col_filter2:
        selected_lane = st.selectbox("Filter by Lane", ["All"] + sorted_lanes, key="lane_filter")

    # Filter heroes
    used = set(st.session_state.blue_team + st.session_state.red_team + st.session_state.blue_bans + st.session_state.red_bans)
    available_heroes = [h for h in HERO_DATA.keys() if h not in used]
    
    # Apply Search Filter
    if search_query: 
        available_heroes = [h for h in available_heroes if search_query.lower() in h.lower()]
    
    # Apply Role Filter
    if selected_role != "All":
        available_heroes = [
            h for h in available_heroes 
            if HERO_DATA[h]["Role 1"] == selected_role or HERO_DATA[h]["Role 2"] == selected_role
        ]
        
    # Apply Lane Filter
    if selected_lane != "All":
        available_heroes = [
            h for h in available_heroes 
            if HERO_DATA[h]["Lane 1"] == selected_lane or HERO_DATA[h]["Lane 2"] == selected_lane
        ]

    # Display Heroes
    if not available_heroes:
        st.info("No heroes found matching your criteria.")
    elif st.session_state.step_index < total_steps:
        for i in range(0, len(available_heroes), 4):
            cols = st.columns(4)
            batch = available_heroes[i:i+4]
            for j, hero in enumerate(batch):
                with cols[j]:
                    display_icon_50px(hero)
                    st.button(hero, key=f"btn_{hero}", use_container_width=True, 
                               on_click=handle_hero_selection, args=(hero, current_action, current_side))

    st.markdown("---")
    render_analytics_panel(hero_stats, st.session_state.blue_team, st.session_state.red_team, st.session_state.blue_bans, st.session_state.red_bans)