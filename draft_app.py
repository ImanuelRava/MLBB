import streamlit as st
import pandas as pd
from hero_data import HERO_DATA
import draft_simulation as ds
import draft_comparison as dc

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
        st.session_state.draft_mode = "Simulation" 
        st.session_state.comp_target_side = "Blue"

    # 2. Load Data
    try:
        hero_stats = pd.DataFrame.from_dict(HERO_DATA, orient='index')
    except Exception as e:
        st.error(f"Error loading hero data: {e}")
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
        /* Specific style for the remove button */
        button[k^="rem_"] {
            height: 30px;
            padding: 0px;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 4. TOP BAR
    col_header, col_mode, col_settings = st.columns([3, 1.5, 1])

    with col_header:
        st.markdown("<h1 style='text-align: left; margin: 0;'>Zahl's Index</h1>", unsafe_allow_html=True)

    with col_mode:
        st.session_state.draft_mode = st.radio(
            "Mode", 
            ["Simulation", "Comparison"], 
            label_visibility="collapsed", 
            horizontal=True
        )

    with col_settings:
        if st.session_state.draft_mode == "Simulation":
            b3, b5 = st.columns([1, 1])
            disabled = st.session_state.step_index > 0
            with b3:
                if st.button("3 Bans", disabled=disabled, use_container_width=True):
                    st.session_state.ban_mode = 3
                    st.rerun()
            with b5:
                if st.button("5 Bans", disabled=disabled, use_container_width=True):
                    st.session_state.ban_mode = 5
                    st.rerun()
        
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

    # 5. ROUTER
    if st.session_state.draft_mode == "Simulation":
        ds.render_simulation_mode(hero_stats)
    elif st.session_state.draft_mode == "Comparison":
        dc.render_comparison_mode(hero_stats)

if __name__ == "__main__":
    main()