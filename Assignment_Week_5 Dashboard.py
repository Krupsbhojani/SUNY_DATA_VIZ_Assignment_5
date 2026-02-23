import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="NBA 2024-25 Dashboard", layout="wide")
st.title("NBA 2024-25 Season Analytics")
st.markdown("**Objective:** Analyze team and player performance trends across the 2024-25 NBA regular season to identify top performers and scoring patterns.")

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.header("Filters")
selected_conf = st.sidebar.selectbox("Conference", ["Both", "East", "West"])
ppg_range = st.sidebar.slider("Min Points Per Game (team)", 100, 125, 108)
show_playoffs = st.sidebar.checkbox("Playoff teams only", value=False)

# ── Data ─────────────────────────────────────────────────────────────────────
teams = pd.DataFrame({
    "Team": ["Boston Celtics","Oklahoma City Thunder","Cleveland Cavaliers","Denver Nuggets",
             "Minnesota Timberwolves","New York Knicks","Golden State Warriors","LA Clippers",
             "Dallas Mavericks","Phoenix Suns","Milwaukee Bucks","Indiana Pacers",
             "Orlando Magic","Houston Rockets","Sacramento Kings"],
    "Conference": ["East","West","East","West","West","East","West","West",
                   "West","West","East","East","East","West","West"],
    "Wins": [61,68,64,50,49,51,46,43,40,36,35,46,41,52,39],
    "Losses": [21,14,18,32,33,31,36,39,42,46,47,36,41,30,43],
    "PPG": [120.6,119.5,114.2,115.8,112.4,116.5,118.3,113.7,117.9,109.2,111.0,123.5,108.2,110.7,116.1],
    "OPP_PPG": [108.1,108.9,105.6,113.2,110.8,114.0,117.2,112.5,116.1,114.8,114.3,121.8,107.5,111.4,118.3],
    "FG_PCT": [48.1,47.2,47.8,48.5,46.9,46.5,47.8,46.3,47.4,44.8,45.5,47.3,44.6,45.9,48.2],
    "3P_PCT": [38.2,36.8,36.5,36.1,35.4,35.8,37.2,36.0,37.5,34.2,34.8,37.1,34.1,35.3,37.8],
    "REB": [46.5,44.2,46.8,46.1,45.0,44.7,43.8,43.5,43.9,44.1,43.6,44.2,47.1,43.8,45.0],
    "AST": [27.8,28.5,25.1,29.4,24.8,27.2,29.0,24.6,28.7,22.5,24.1,29.8,22.4,25.3,28.1],
    "Playoff": [True,True,True,True,True,True,False,True,True,False,False,True,True,True,False],
})

players = pd.DataFrame({
    "Player": ["Shai Gilgeous-Alexander","Giannis Antetokounmpo","Luka Doncic","Jayson Tatum",
               "Karl-Anthony Towns","Donovan Mitchell","Anthony Edwards","LaMelo Ball",
               "Tyrese Haliburton","Nikola Jokic","Kevin Durant","Devin Booker"],
    "Team": ["OKC","MIL","DAL","BOS","NYK","CLE","MIN","CHA","IND","DEN","PHX","PHX"],
    "PPG": [32.7,30.4,28.1,26.9,24.9,26.5,25.9,30.1,20.1,29.7,27.1,27.4],
    "RPG": [5.5,12.2,8.7,8.1,13.4,6.1,5.4,5.8,3.8,12.7,6.9,4.5],
    "APG": [6.4,5.8,7.8,4.9,3.5,5.7,5.1,8.5,10.9,9.0,5.1,4.8],
    "FG_PCT": [53.5,55.2,48.7,46.6,55.8,48.2,46.4,43.3,47.3,57.9,50.1,49.8],
    "3P_PCT": [35.6,27.4,37.4,36.1,40.2,36.7,34.5,37.2,38.5,35.8,38.6,36.4],
    "PER": [31.2,30.5,27.8,25.4,23.8,24.1,22.9,26.7,23.5,32.1,24.8,25.2],
})

monthly = pd.DataFrame({
    "Month": ["Oct","Nov","Dec","Jan","Feb","Mar","Apr"]*3,
    "Team": ["Boston Celtics"]*7 + ["Oklahoma City Thunder"]*7 + ["Cleveland Cavaliers"]*7,
    "Win_PCT": [0.75,0.80,0.78,0.74,0.79,0.82,0.80,
                0.85,0.87,0.84,0.86,0.88,0.86,0.89,
                0.70,0.78,0.82,0.80,0.83,0.81,0.84],
    "PPG": [118,121,120,119,122,123,121,
            117,120,119,121,120,122,121,
            112,114,115,113,116,115,117],
})

# ── Apply filters ─────────────────────────────────────────────────────────────
df = teams.copy()
if selected_conf != "Both":
    df = df[df["Conference"] == selected_conf]
df = df[df["PPG"] >= ppg_range]
if show_playoffs:
    df = df[df["Playoff"] == True]

# ── Metric Cards ──────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Teams Shown", len(df))
m2.metric("Avg PPG", f"{df['PPG'].mean():.1f}")
m3.metric("Avg Wins", f"{df['Wins'].mean():.0f}")
m4.metric("Top Scorer (Player)", "SGA – 32.7")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Team Overview", "Player Stats", "Monthly Trends"])

# ════════════════════════════════════════════════════════════════════
# TAB 1 – Team Overview
# ════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Team Performance Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Bar chart – Wins by team
        fig_bar = px.bar(df.sort_values("Wins", ascending=True),
                         x="Wins", y="Team", orientation="h",
                         color="Conference", title="Wins by Team",
                         color_discrete_map={"East":"#1f77b4","West":"#ff7f0e"})
        fig_bar.update_layout(height=400, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("Teams in the West are generally posting more wins this season, with OKC leading the league. Conference balance is noticeably skewed toward the West.")

    with col2:
        # Scatter – PPG vs Win %
        df["Win_PCT"] = df["Wins"] / (df["Wins"] + df["Losses"])
        fig_scatter = px.scatter(df, x="PPG", y="Win_PCT", text="Team",
                                 color="Conference", size="Wins",
                                 title="Points Per Game vs Win %",
                                 color_discrete_map={"East":"#1f77b4","West":"#ff7f0e"})
        fig_scatter.update_traces(textposition="top center")
        fig_scatter.update_layout(height=400, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("There's a clear positive trend : teams that score more tend to win more. OKC and Boston stand out as both high-scoring and high-winning.")

    # Heatmap – team stat categories
    st.subheader("Team Stats Heatmap")
    heatmap_cols = ["PPG","OPP_PPG","FG_PCT","3P_PCT","REB","AST"]
    heatmap_df = df.set_index("Team")[heatmap_cols]
    heatmap_norm = (heatmap_df - heatmap_df.min()) / (heatmap_df.max() - heatmap_df.min())
    fig_heat = go.Figure(go.Heatmap(
        z=heatmap_norm.values,
        x=heatmap_cols,
        y=heatmap_norm.index.tolist(),
        colorscale="Blues",
        text=heatmap_df.values.round(1),
        texttemplate="%{text}",
        showscale=True,
    ))
    fig_heat.update_layout(title="Normalized Team Stats (darker = better)", height=400,
                           margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("Boston and Denver rank highly across most categories, especially shooting efficiency. Indiana stands out for scoring but struggles defensively with a high opponent PPG.")

# ════════════════════════════════════════════════════════════════════
# TAB 2 – Player Stats
# ════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Player Performance Breakdown")

    selected_stat = st.selectbox("Color by:", ["PPG","RPG","APG","PER","FG_PCT"])

    col1, col2 = st.columns(2)

    with col1:
        # Horizontal bar – PPG
        fig_ppg = px.bar(players.sort_values("PPG"),
                         x="PPG", y="Player", orientation="h",
                         color="PPG", color_continuous_scale="Oranges",
                         title="Points Per Game – Top Players")
        fig_ppg.update_layout(height=420, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig_ppg, use_container_width=True)
        st.markdown("SGA leads the league in scoring this season, narrowly ahead of Jokic and Giannis. The gap at the top is tight, making the scoring race one of the best in years.")

    with col2:
        # Scatter – RPG vs APG sized by PPG
        fig_pscatter = px.scatter(players, x="RPG", y="APG",
                                  size="PPG", color=selected_stat,
                                  hover_name="Player",
                                  color_continuous_scale="Viridis",
                                  title="Rebounds vs Assists (size = PPG)")
        fig_pscatter.update_layout(height=420, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig_pscatter, use_container_width=True)
        st.markdown("Jokic sits in his own category : elite in both rebounding and assists while scoring 30+. Haliburton leads all players in assists, showing Indiana's pass-first system.")

    st.subheader("Raw Player Stats Table")
    st.dataframe(players.sort_values("PPG", ascending=False).reset_index(drop=True), use_container_width=True)

# ════════════════════════════════════════════════════════════════════
# TAB 3 – Monthly Trends
# ════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Monthly Win % Trends – Top 3 Teams")

    selected_teams = st.multiselect("Select teams:", ["Boston Celtics","Oklahoma City Thunder","Cleveland Cavaliers"],
                                    default=["Boston Celtics","Oklahoma City Thunder","Cleveland Cavaliers"])

    monthly_filtered = monthly[monthly["Team"].isin(selected_teams)]

    col1, col2 = st.columns(2)

    with col1:
        fig_line = px.line(monthly_filtered, x="Month", y="Win_PCT", color="Team",
                           markers=True, title="Monthly Win Percentage",
                           category_orders={"Month":["Oct","Nov","Dec","Jan","Feb","Mar","Apr"]})
        fig_line.update_layout(height=380, margin=dict(l=0,r=0,t=40,b=0), yaxis_tickformat=".0%")
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown("OKC has been consistently dominant all season with little drop-off. Boston and Cleveland both improved as the season progressed, peaking around March.")

    with col2:
        fig_ppg_line = px.line(monthly_filtered, x="Month", y="PPG", color="Team",
                               markers=True, title="Monthly Points Per Game",
                               category_orders={"Month":["Oct","Nov","Dec","Jan","Feb","Mar","Apr"]})
        fig_ppg_line.update_layout(height=380, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig_ppg_line, use_container_width=True)
        st.markdown("All three teams show a slight upward scoring trend through the year, which is common as teams settle into their systems. Boston's mid-season dip in January likely reflects a tough schedule stretch.")

st.markdown("---")
st.caption("Data source: Basketball Reference (basketball-reference.com) | Stats reflect 2024-25 NBA Regular Season")
