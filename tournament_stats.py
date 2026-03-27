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
    
    # Row 2: Map and Team
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        maps = ["All"] + analyzer.get_unique_values('map')
        selected_map = st.selectbox("Map", maps, key="filter_map")
        
    with col_f2:
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
        sort_by = st.selectbox(
            "Sort By",
            ("Total Picks", "Ban P1", "Win Rate"), 
            key="filter_sort"
        )

    st.markdown("---")

    # ==========================================
    # STATISTICS TABLE
    # ==========================================
    st.markdown(f"### 📊 {selected_side} Side Statistics")
    
    df_summary = analyzer.get_hero_summary(
        side=selected_side,
        tournament_filter=selected_tournament,
        map_filter=selected_map,
        team_filter=selected_team
    )
    
    if not df_summary.empty:
        # Sort
        ascending_order = False
        df_summary = df_summary.sort_values(by=sort_by, ascending=ascending_order).reset_index(drop=True)
        
        # Header Row (Layered)
        cols_h1 = st.columns([0.5, 1.5, 1.2, 1.2, 0.8])
        cols_h1[0].markdown("")
        cols_h1[1].markdown("")
        cols_h1[2].markdown("<div style='text-align: center; font-weight: bold;'>Pick</div>", unsafe_allow_html=True)
        cols_h1[3].markdown("<div style='text-align: center; font-weight: bold;'>Ban</div>", unsafe_allow_html=True)
        cols_h1[4].markdown("")
        
        # Row 2: Sub Headers
        cols_h2 = st.columns([0.5, 1.5, 0.6, 0.6, 0.6, 0.6, 0.8])
        cols_h2[0].markdown("")
        cols_h2[1].markdown("<b>Hero</b>", unsafe_allow_html=True)
        cols_h2[2].markdown("<div style='text-align: center; font-size: 0.85em;'>Upper</div>", unsafe_allow_html=True)
        cols_h2[3].markdown("<div style='text-align: center; font-size: 0.85em;'>Lower</div>", unsafe_allow_html=True)
        cols_h2[4].markdown("<div style='text-align: center; font-size: 0.85em;'>Upper</div>", unsafe_allow_html=True)
        cols_h2[5].markdown("<div style='text-align: center; font-size: 0.85em;'>Lower</div>", unsafe_allow_html=True)
        cols_h2[6].markdown("<div style='text-align: center;'><b>Win Rate</b></div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 0; padding: 0;'>", unsafe_allow_html=True)
        
        # Data Rows
        for index, row in df_summary.iterrows():
            row_cols = st.columns([0.5, 1.5, 0.6, 0.6, 0.6, 0.6, 0.8])
            
            # Icon
            with row_cols[0]:
                display_icon_50px(row['Hero'])
            
            # Hero
            row_cols[1].markdown(f"<div style='padding-top: 10px;'>{row['Hero']}</div>", unsafe_allow_html=True)
            
            # Pick Upper
            row_cols[2].markdown(f"<div style='padding-top: 10px; text-align: center;'>{row['Pick P1']}</div>", unsafe_allow_html=True)
            
            # Pick Lower
            row_cols[3].markdown(f"<div style='padding-top: 10px; text-align: center;'>{row['Pick P2']}</div>", unsafe_allow_html=True)
            
            # Ban Upper
            row_cols[4].markdown(f"<div style='padding-top: 10px; text-align: center;'>{row['Ban P1']}</div>", unsafe_allow_html=True)
            
            # Ban Lower
            row_cols[5].markdown(f"<div style='padding-top: 10px; text-align: center;'>{row['Ban P2']}</div>", unsafe_allow_html=True)
            
            # Win Rate
            wr_str = f"{row['Win Rate']:.1f}%"
            row_cols[6].markdown(f"<div style='padding-top: 10px; text-align: center;'>{wr_str}</div>", unsafe_allow_html=True)

    else:
        st.info("No data available for the selected filters.")