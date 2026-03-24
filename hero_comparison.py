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
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("Team Comparison (Radar Chart)")
            stats_df_long = stats_df.reset_index().melt(id_vars='Metric', var_name='Team', value_name='Score')
            radar_fig = create_radar_chart(stats_df_long)
            st.plotly_chart(radar_fig, use_container_width=True)
        
        with c2:
            st.write("Team Analysis")
            
            # Win Probability Bar
            st.markdown("<b>Estimated Win Probability</b>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style='display: flex; justify-content: space-between; font-size: 0.9em; margin-bottom: 5px;'>
                    <span style='color: #1f77b4'>Blue: {blue_prob}%</span>
                    <span style='color: #d62728'>Red: {red_prob}%</span>
                </div>
                <div style='display: flex; height: 20px; width: 100%; border-radius: 5px; overflow: hidden; background-color: #eee;'>
                    <div style='width: {blue_prob}%; background-color: #1f77b4;'></div>
                    <div style='width: {red_prob}%; background-color: #d62728;'></div>
                </div>
                <small style='color: #888; display: block; margin-top: 5px;'>Based on Total Stat Power</small>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Suggestion Block
            if suggestion_heroes:
                st.markdown(f"<h4 style='color: {suggestion_color}; margin-top: 0;'>Suggestion for {suggestion_team_name} Team</h4>", unsafe_allow_html=True)
                st.markdown(f"<small>{suggestion_text}</small>", unsafe_allow_html=True)
                
                s1, s2, s3 = st.columns(3)
                suggestions_to_display = suggestion_heroes + [None] * (3 - len(suggestion_heroes))
                
                for i, hero in enumerate(suggestions_to_display):
                    col = [s1, s2, s3][i]
                    with col:
                        if hero:
                            display_icon_50px(hero)
                            st.caption(f"{hero}")
                        else:
                            st.empty()
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("Advantages")
            
            st.markdown("<div style='margin-bottom: 10px; font-weight: bold; color: #1f77b4;'>🔵 Blue Team</div>", unsafe_allow_html=True)
            if blue_adv:
                for adv in blue_adv:
                    st.markdown(f"- {adv}")
            else:
                st.markdown("<small>No significant advantage.</small>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom: 10px; font-weight: bold; color: #d62728;'>🔴 Red Team</div>", unsafe_allow_html=True)
            if red_adv:
                for adv in red_adv:
                    st.markdown(f"- {adv}")
            else:
                st.markdown("<small>No significant advantage.</small>", unsafe_allow_html=True)