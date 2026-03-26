import streamlit as st
import pandas as pd
from analytics import (
    analyze_draft, 
    calculate_win_probability, 
    get_advantage_explanations, 
    get_team_suggestion,
    create_radar_chart
)
from utils import display_icon_50px

def render_analytics_panel(hero_stats, blue_team, red_team, blue_bans, red_bans):
    """Calculates and renders the analytics panel."""
    total_picks = len(blue_team) + len(red_team)
    
    if total_picks < 2:
        st.info("Select at least 2 heroes to see analysis.")
        return

    stats_df, blue_scores, red_scores = analyze_draft(hero_stats, blue_team, red_team)
    blue_adv, red_adv = get_advantage_explanations(blue_scores, red_scores)
    blue_prob, red_prob = calculate_win_probability(hero_stats, blue_team, red_team)
    
    suggestion_lane = None
    suggestion_heroes = []
    suggestion_text = ""
    suggestion_team_name = ""
    suggestion_color = ""
    
    if blue_prob < red_prob:
        suggestion_lane, suggestion_heroes, suggestion_text = get_team_suggestion(
            hero_stats, blue_team, red_team, blue_bans, red_bans
        )
        suggestion_team_name = "Blue"
        suggestion_color = "#1f77b4"
    elif red_prob < blue_prob:
        suggestion_lane, suggestion_heroes, suggestion_text = get_team_suggestion(
            hero_stats, red_team, blue_team, red_bans, blue_bans
        )
        suggestion_team_name = "Red"
        suggestion_color = "#d62728"
    
    with st.expander("📊 Draft Evaluation", expanded=True):
        # ==========================================
        # ROW 1: SPIDER CHART (Full Width)
        # ==========================================
        stats_df_long = stats_df.reset_index().melt(id_vars='Metric', var_name='Team', value_name='Score')
        radar_fig = create_radar_chart(stats_df_long)
        st.plotly_chart(radar_fig, use_container_width=True)

        # ==========================================
        # ROW 2: WIN PROBABILITY (Full Width)
        # ==========================================
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; font-size: 0.9em; margin-bottom: 5px;'>
                <span style='color: #1f77b4; font-weight: bold;'>Blue: {blue_prob}%</span>
                <span style='color: #d62728; font-weight: bold;'>Red: {red_prob}%</span>
            </div>
            <div style='display: flex; height: 24px; width: 100%; border-radius: 12px; overflow: hidden; background-color: #eee;'>
                <div style='width: {blue_prob}%; background-color: #1f77b4;'></div>
                <div style='width: {red_prob}%; background-color: #d62728;'></div>
            </div>
            <small style='color: #888; display: block; margin-top: 5px; text-align: center;'>Based on Total Stat Power</small>
        """, unsafe_allow_html=True)

        # ==========================================
        # ROW 2.5: SUGGESTION (If applicable)
        # ==========================================
        if suggestion_heroes:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: {suggestion_color}; margin-top: 0;'>💡 Suggestion for {suggestion_team_name} Team</h4>", unsafe_allow_html=True)
            st.markdown(f"<small>{suggestion_text}</small>", unsafe_allow_html=True)
            
            s1, s2, s3 = st.columns(3)
            suggestions_to_display = suggestion_heroes + [None] * (3 - len(suggestion_heroes))
            
            for i, hero in enumerate(suggestions_to_display):
                col = [s1, s2, s3][i]
                with col:
                    if hero:
                        display_icon_50px(hero)
                        st.caption(f"{hero}")

        # ==========================================
        # ROW 3: ADVANTAGES (Side by Side)
        # ==========================================
        # Removed the 'div' styling to remove the box appearance
        st.markdown("<br>", unsafe_allow_html=True) # Small spacer
        col_blue_adv, col_red_adv = st.columns(2)

        with col_blue_adv:
            st.markdown("<b style='color: #1f77b4; font-size: 1.1em;'>🔵 Blue Team</b>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 5px 0; border-color: #ddd;'>", unsafe_allow_html=True)
            if blue_adv:
                for adv in blue_adv:
                    st.markdown(f"✅ {adv}")
            else:
                st.markdown("<small>No significant advantage detected.</small>", unsafe_allow_html=True)

        with col_red_adv:
            st.markdown("<b style='color: #d62728; font-size: 1.1em;'>🔴 Red Team</b>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 5px 0; border-color: #ddd;'>", unsafe_allow_html=True)
            if red_adv:
                for adv in red_adv:
                    st.markdown(f"✅ {adv}")
            else:
                st.markdown("<small>No significant advantage detected.</small>", unsafe_allow_html=True)