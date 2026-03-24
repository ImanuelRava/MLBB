import pandas as pd
import plotly.express as px
from hero_data import HERO_DATA

# Define the 5 metrics we are now tracking
ALL_STATS = ['Durability', 'Offense', 'Control Effect', 'Mobility', 'Utility']

def analyze_draft(hero_stats, blue_team, red_team):
    """Calculates team stats based on the hero_stats DataFrame."""
    stats_cols = ALL_STATS
    
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

def calculate_win_probability(hero_stats, blue_team, red_team):
    """
    Calculates win probability based on total 'Power' (sum of all stats).
    Returns: Blue %, Red %
    """
    stats_cols = ALL_STATS
    
    blue_total = 0.0
    if blue_team:
        valid_blue = [h for h in blue_team if h in hero_stats.index]
        if valid_blue:
            blue_total = hero_stats.loc[valid_blue][stats_cols].sum().sum()

    red_total = 0.0
    if red_team:
        valid_red = [h for h in red_team if h in hero_stats.index]
        if valid_red:
            red_total = hero_stats.loc[valid_red][stats_cols].sum().sum()
            
    total_power = blue_total + red_total
    
    if total_power == 0:
        return 50.0, 50.0
    
    blue_prob = (blue_total / total_power) * 100
    red_prob = (red_total / total_power) * 100
    
    return round(blue_prob, 1), round(red_prob, 1)

def get_advantage_explanations(blue_scores, red_scores):
    """Compares stats to generate natural language advantages."""
    stats_cols = ALL_STATS
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
            elif stat == "Utility":
                blue_adv.append("Higher Utility (Better Team Buffs/Support)")
                
        elif diff <= -1.0:
            if stat == "Durability":
                red_adv.append("Higher Durability (Tankier front line)")
            elif stat == "Offense":
                red_adv.append("Higher Offense (More burst damage)")
            elif stat == "Control Effect":
                red_adv.append("Stronger Crowd Control (Better lockdown)")
            elif stat == "Mobility":
                red_adv.append("Superior Mobility (Better rotations)")
            elif stat == "Utility":
                red_adv.append("Higher Utility (Better Team Buffs/Support)")
            
    return blue_adv, red_adv

def get_team_suggestion(hero_stats, my_team, opp_team, own_bans, opp_bans):
    """
    Analyzes team composition based on LANES and STAT BALANCE.
    1. Identifies Missing Lane.
    2. Identifies which Stat is causing the team to lose (Deficit).
    3. Suggests heroes fitting the lane that patch the Deficit.
    """
    stats_cols = ALL_STATS

    # 1. Identify Available Heroes
    # CRITICAL: Filter out BOTH picked heroes AND banned heroes
    used_heroes = set(my_team + opp_team + own_bans + opp_bans)
    available_heroes = [h for h in HERO_DATA.keys() if h not in used_heroes]
    
    if not available_heroes:
        return None, [], "No heroes available to suggest."

    # 2. Analyze Current Team Lanes
    lane_counts = {}
    for hero in my_team:
        if hero in hero_stats.index:
            l1 = hero_stats.loc[hero]['Lane 1']
            l2 = hero_stats.loc[hero]['Lane 2']
            if l1 != 'N/A':
                lane_counts[l1] = lane_counts.get(l1, 0) + 1
            if l2 != 'N/A':
                lane_counts[l2] = lane_counts.get(l2, 0) + 1

    # 3. Determine Needed Lane
    key_lanes = ['EXP Lane', 'Jungle', 'Mid Lane', 'Gold Lane', 'Roaming']
    needed_lane = None
    for lane in key_lanes:
        if lane_counts.get(lane, 0) == 0:
            needed_lane = lane
            break

    if not needed_lane:
        return None, [], "Team composition covers all lanes."

    # 4. Determine Stat Deficit (Where is my team losing?)
    # Calculate Average Stats for My Team
    my_scores = [0.0] * len(stats_cols)
    if my_team:
        valid_my = [h for h in my_team if h in hero_stats.index]
        if valid_my:
            my_scores = hero_stats.loc[valid_my][stats_cols].mean().tolist()

    # Calculate Average Stats for Opponent Team
    opp_scores = [0.0] * len(stats_cols)
    if opp_team:
        valid_opp = [h for h in opp_team if h in hero_stats.index]
        if valid_opp:
            opp_scores = hero_stats.loc[valid_opp][stats_cols].mean().tolist()
    
    # Find the stat with the biggest gap (Opponent > Me)
    deficits = {}
    for i, col in enumerate(stats_cols):
        deficit = opp_scores[i] - my_scores[i]
        if deficit > 0.5: # Only consider if deficit is significant
            deficits[col] = deficit
    
    # Target Stat: The one we are losing the most in
    target_stat = None
    if deficits:
        target_stat = max(deficits, key=deficits.get)
    
    # 5. Find Top 3 Candidates
    candidates = []
    
    for hero in available_heroes:
        if hero in hero_stats.index:
            l1 = hero_stats.loc[hero]['Lane 1']
            l2 = hero_stats.loc[hero]['Lane 2']
            
            if l1 == needed_lane or l2 == needed_lane:
                # Calculate Score
                total_stats = hero_stats.loc[hero][stats_cols].sum()
                
                if target_stat:
                    # Score heavily weighted towards the missing stat
                    balance_score = (hero_stats.loc[hero][target_stat] * 2.5) + total_stats
                else:
                    # If no deficit, just use total stats
                    balance_score = total_stats
                
                candidates.append((hero, balance_score))
                
    if not candidates:
        return None, [], f"No {needed_lane} heroes available in the pool."
        
    # Sort by Score
    candidates.sort(key=lambda x: x[1], reverse=True)
    top_3_heroes = [x[0] for x in candidates[:3]]
    
    reason = f"Missing <b>{needed_lane}</b> lane. "
    if target_stat:
        reason += f"Team is weak in {target_stat}. Suggested to improve <b>{target_stat}</b>."
    else:
        reason += "Suggested to improve overall strength."
        
    return needed_lane, top_3_heroes, reason

def create_radar_chart(stats_df_long):
    """
    Creates a spider/radar chart to compare team stats.
    Expects a DataFrame with columns: 'Metric', 'Team', 'Score'.
    Background is set to transparent.
    """
    fig = px.line_polar(
        stats_df_long, 
        r='Score', 
        theta='Metric', 
        color='Team', 
        line_close=True,
        range_r=[0, 10], # Assuming stats are on a 0-10 scale
        color_discrete_map={'Blue': '#1f77b4', 'Red': '#d62728'} # Match your app colors
    )
    
    # Fill the area under the lines
    fig.update_traces(fill='toself')
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=False, # Hide numbers on axis for cleaner look
                gridcolor='lightgray' # Grid line color
            ),
            angularaxis=dict(
                gridcolor='lightgray' # Angular grid line color
            )
        ),
        showlegend=True,
        margin=dict(l=20, r=20, t=20, b=20), # Tight margins
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    return fig