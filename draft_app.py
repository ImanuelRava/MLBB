import streamlit as st
import pandas as pd
from hero_data import HERO_DATA
import draft_comparison as dc
import tournament_stats as ts
from data_analyzer import DataAnalyzer

# --- MAIN APP ---

def main():
    st.set_page_config(page_title="Zahl's Index", layout="wide", page_icon="favicon.ico")

    # 1. Initialize Session State
    if 'step_index' not in st.session_state:
        st.session_state.step_index = 0
        st.session_state.blue_team = []
        st.session_state.red_team = []
        st.session_state.blue_bans = []  
        st.session_state.red_bans = []   
        st.session_state.ban_mode = 5
        st.session_state.draft_mode = "Comparison" 
        st.session_state.comp_target_side = "Blue"
        
        # Initialize Data Analyzer (Loads Tournament Stats sheet)
        st.session_state.data_analyzer = DataAnalyzer()

    # 2. Load Data
    # HERO_DATA is now loaded from Excel via hero_data.py
    if not HERO_DATA:
        st.error("Hero Data failed to load. Please check 'Analyst.xlsx' for a sheet named 'Hero Data'.")
        return

    try:
        hero_stats = pd.DataFrame.from_dict(HERO_DATA, orient='index')
    except Exception as e:
        st.error(f"Error processing hero data: {e}")
        return

    # 3. CSS
    st.markdown("""
        <style>
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
        button[k^="rem_"] {
            height: 30px;
            padding: 0px;
            font-size: 14px;
        }
        div[data-testid="stSidebar"] .stRadio > label {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # 4. SIDEBAR NAVIGATION
    with st.sidebar:
        st.markdown("<h2>Navigation</h2>", unsafe_allow_html=True)
        st.session_state.draft_mode = st.radio(
            "Page", 
            ["Comparison", "Tournament Statistics"],
            label_visibility="collapsed"
        )
        st.markdown("---")

    # 5. TOP BAR
    col_header, col_settings = st.columns([4, 1])

    with col_header:
        st.markdown("<h1 style='text-align: left; margin: 0; margin-bottom: 5px;'>Zahl's Index</h1>", unsafe_allow_html=True)
        # Show file status
        if os.path.exists('Analyst.xlsx'):
            st.caption("✅ Data Loaded")
        else:
            st.caption("❌ Data Missing")

    with col_settings:
        if st.button("Reset", use_container_width=True):
            st.session_state.step_index = 0
            st.session_state.blue_team = []
            st.session_state.red_team = []
            st.session_state.blue_bans = []
            st.session_state.red_bans = []
            if 'sim_search' in st.session_state: st.session_state.sim_search = ""
            if 'comp_search' in st.session_state: st.session_state.comp_search = ""
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 6. ROUTER
    if st.session_state.draft_mode == "Comparison":
        dc.render_comparison_mode(hero_stats)
    elif st.session_state.draft_mode == "Tournament Statistics":
        ts.render_tournament_stats()

if __name__ == "__main__":
    import os # Needed for file check in UI
    main()