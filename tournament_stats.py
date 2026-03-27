import streamlit as st
from data_analyzer import DataAnalyzer
from utils import display_icon_50px
import pandas as pd

def render_tournament_stats():
    st.markdown("<h1 style='text-align: center;'>Tournament Statistics</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Check if analyzer is initialized
    if 'data_analyzer' not in st.session_state:
        st.session_state.data_analyzer = DataAnalyzer()

    analyzer = st.session_state.data_analyzer

    if not analyzer.is_loaded:
        st.warning("Tournament data is not loaded. Please ensure 'Analyst.xlsx' is in the application folder.")
        return

    # ==========================================
    # FILTERS
    # ==========================================
    # Row 1: Tournament
    tournaments = ["All"] + analyzer.get_unique_values('tournament')
    selected_tournament = st.selectbox("Tournament", tournaments, key="filter_tourney")
    
    # Row 2: Map and Team (Team list depends on Tournament)
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        maps = ["All"] + analyzer.get_unique_values('map')
        selected_map = st.selectbox("Map", maps, key="filter_map")
        
    with col_f2:
        # Pass the tournament filter to get teams for that tournament
        teams = ["All"] + analyzer.get_unique_values('team', tournament_filter=selected_tournament)
        selected_team = st.selectbox("Team", teams, key="filter_team")
    
    # Row 3: Side and Sort
    col_f3, col_f4 = st.columns(2)
    
    with col_f3:
        selected_side = st.radio(
            "Select Side",
            ("Blue", "Red"),
            horizontal=True,
            key="filter_side"
        )
    
    with col_f4:
        # Sort By options
        sort_by = st.selectbox(
            "Sort By",
            ("Picks", "Bans", "Win Rate"),
            key="filter_sort"
        )

    st.markdown("---")

    # ==========================================
    # STATISTICS TABLE (Visual with Icons)
    # ==========================================
    st.markdown(f"### 📊 {selected_side} Side Statistics")
    
    # Generate the summary dataframe
    df_summary = analyzer.get_hero_summary(
        side=selected_side,
        tournament_filter=selected_tournament,
        map_filter=selected_map,
        team_filter=selected_team
    )
    
    if not df_summary.empty:
        # Sort the dataframe
        # Note: Win Rate is a float, descending
        ascending_order = False 
        df_summary = df_summary.sort_values(by=sort_by, ascending=ascending_order).reset_index(drop=True)
        
        # Header Row
        header_cols = st.columns([0.6, 1.5, 0.8, 0.8, 0.8])
        header_cols[0].markdown("**Icon**")
        header_cols[1].markdown("**Hero**")
        header_cols[2].markdown("**Picks**")
        header_cols[3].markdown("**Bans**")
        header_cols[4].markdown("**Win Rate**")
        
        st.markdown("<hr style='margin: 0; padding: 0;'>", unsafe_allow_html=True)
        
        # Data Rows
        for index, row in df_summary.iterrows():
            row_cols = st.columns([0.6, 1.5, 0.8, 0.8, 0.8])
            
            # 1. Icon
            with row_cols[0]:
                display_icon_50px(row['Hero'])
            
            # 2. Hero Name
            row_cols[1].markdown(f"<div style='padding-top: 10px;'>{row['Hero']}</div>", unsafe_allow_html=True)
            
            # 3. Picks
            row_cols[2].markdown(f"<div style='padding-top: 10px; text-align: center;'>{row['Picks']}</div>", unsafe_allow_html=True)
            
            # 4. Bans
            row_cols[3].markdown(f"<div style='padding-top: 10px; text-align: center;'>{row['Bans']}</div>", unsafe_allow_html=True)
            
            # 5. Win Rate (Format the float here)
            wr_str = f"{row['Win Rate']:.1f}%"
            row_cols[4].markdown(f"<div style='padding-top: 10px; text-align: center;'>{wr_str}</div>", unsafe_allow_html=True)

    else:
        st.info("No data available for the selected filters.")