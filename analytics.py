import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    """
    stats_cols = ALL_STATS
    used_heroes = set(my_team + opp_team + own_bans + opp_bans)
    available_heroes = [h for h in HERO_DATA.keys() if h not in used_heroes]
    
    if not available_heroes:
        return None, [], "No heroes available to suggest."

    lane_counts = {}
    for hero in my_team:
        if hero in hero_stats.index:
            l1 = hero_stats.loc[hero]['Lane 1']
            l2 = hero_stats.loc[hero]['Lane 2']
            if l1 != 'N/A':
                lane_counts[l1] = lane_counts.get(l1, 0) + 1
            if l2 != 'N/A':
                lane_counts[l2] = lane_counts.get(l2, 0) + 1

    key_lanes = ['EXP Lane', 'Jungle', 'Mid Lane', 'Gold Lane', 'Roaming']
    needed_lane = None
    for lane in key_lanes:
        if lane_counts.get(lane, 0) == 0:
            needed_lane = lane
            break

    if not needed_lane:
        return None, [], "Team composition covers all lanes."

    my_scores = [0.0] * len(stats_cols)
    if my_team:
        valid_my = [h for h in my_team if h in hero_stats.index]
        if valid_my:
            my_scores = hero_stats.loc[valid_my][stats_cols].mean().tolist()

    opp_scores = [0.0] * len(stats_cols)
    if opp_team:
        valid_opp = [h for h in opp_team if h in hero_stats.index]
        if valid_opp:
            opp_scores = hero_stats.loc[valid_opp][stats_cols].mean().tolist()
    
    deficits = {}
    for i, col in enumerate(stats_cols):
        deficit = opp_scores[i] - my_scores[i]
        if deficit > 0.3:
            deficits[col] = deficit
    
    target_stat = None
    if deficits:
        target_stat = max(deficits, key=deficits.get)
    
    candidates = []
    
    for hero in available_heroes:
        if hero in hero_stats.index:
            l1 = hero_stats.loc[hero]['Lane 1']
            l2 = hero_stats.loc[hero]['Lane 2']
            
            if l1 == needed_lane or l2 == needed_lane:
                total_stats = hero_stats.loc[hero][stats_cols].sum()
                
                if target_stat:
                    balance_score = (hero_stats.loc[hero][target_stat] * 2.5) + total_stats
                else:
                    balance_score = total_stats
                
                candidates.append((hero, balance_score))
                
    if not candidates:
        return None, [], f"No {needed_lane} heroes available in the pool."
        
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
    Creates a spider/radar chart with a PENTAGONAL border and a comparison table.
    - Border: Pentagon (5-sided polygon).
    - Interaction: Non-rotateable.
    - Includes a data table below the chart.
    """
    
    # 1. Prepare Data
    # Pivot long format to wide for easier access
    df_wide = stats_df_long.pivot(index='Metric', columns='Team', values='Score').reset_index()
    
    # Ensure specific order
    metric_order = ALL_STATS
    df_wide['Metric'] = pd.Categorical(df_wide['Metric'], categories=metric_order, ordered=True)
    df_wide = df_wide.sort_values('Metric')
    
    metrics = df_wide['Metric'].tolist()
    blue_vals = df_wide['Blue'].tolist()
    red_vals = df_wide['Red'].tolist()
    
    # Close the loop for radar lines
    metrics_closed = metrics + [metrics[0]]
    blue_vals_closed = blue_vals + [blue_vals[0]]
    red_vals_closed = red_vals + [red_vals[0]]
    
    # 2. Create Subplots (Radar top, Table bottom)
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.6, 0.4],
        specs=[[{'type': 'polar'}], [{'type': 'table'}]],
        vertical_spacing=0.05
    )

    # 3. Add Radar Traces
    # Blue Team
    fig.add_trace(
        go.Scatterpolar(
            r=blue_vals_closed,
            theta=metrics_closed,
            name='Blue',
            fill='toself',
            line_color='#1f77b4',
            opacity=0.8
        ),
        row=1, col=1
    )

    # Red Team
    fig.add_trace(
        go.Scatterpolar(
            r=red_vals_closed,
            theta=metrics_closed,
            name='Red',
            fill='toself',
            line_color='#d62728',
            opacity=0.8
        ),
        row=1, col=1
    )

    # 4. Add Data Table
    cell_values = [
        df_wide['Metric'].tolist(),
        [f"{x:.2f}" for x in df_wide['Blue'].tolist()],
        [f"{x:.2f}" for x in df_wide['Red'].tolist()]
    ]

    fig.add_trace(
        go.Table(
            header=dict(
                values=['<b>Metric</b>', '<b>Blue</b>', '<b>Red</b>'],
                fill_color='#f0f2f6',
                align='center',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=cell_values,
                fill_color=[['white'], ['#e6f2ff', 'white']],
                align='center',
                font=dict(size=11)
            )
        ),
        row=2, col=1
    )

    # 5. Update Layout
    # shape='polygon' creates the pentagonal grid/border because we have 5 categories.
    fig.update_layout(
        dragmode=False, # Make non-rotateable
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=30, b=20),
        polar=dict(
            shape='polygon', # THIS sets the pentagonal border/grid
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=False,
                gridcolor='lightgray',
                showline=False
            ),
            angularaxis=dict(
                gridcolor='lightgray',
                showline=False
            ),
            bgcolor='rgba(0,0,0,0)'
        )
    )

    return fig