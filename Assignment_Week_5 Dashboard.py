import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="NBA 2024-25 Dashboard", layout="wide")
st.title("NBA 2024-25 Season Analytics")
st.markdown("**Objective:** Track team and player performance to see who's leading the league and why.")

# load data
teams   = pd.read_csv("teams.csv")
players = pd.read_csv("players.csv")
monthly = pd.read_csv("monthly.csv")

# sidebar filters
st.sidebar.header("Filters")
conf = st.sidebar.selectbox("Conference", ["Both", "East", "West"])
min_ppg = st.sidebar.slider("Min Team PPG", 100, 125, 108)
playoffs_only = st.sidebar.checkbox("Playoff teams only")

df = teams.copy()
if conf != "Both":
    df = df[df["Conference"] == conf]
df = df[df["PPG"] >= min_ppg]
if playoffs_only:
    df = df[df["Playoff"] == True]

df["Win_PCT"] = (df["Wins"] / (df["Wins"] + df["Losses"])).round(3)

# metric cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Teams", len(df))
c2.metric("Avg PPG", f"{df['PPG'].mean():.1f}")
c3.metric("Avg Wins", f"{df['Wins'].mean():.0f}")
c4.metric("Top Scorer", "SGA – 32.7")

tab1, tab2, tab3 = st.tabs(["Team Overview", "Player Stats", "Monthly Trends"])

# --- Tab 1: Team Overview ---
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(df.sort_values("Wins"), x="Wins", y="Team", orientation="h",
                     color="Conference", title="Wins by Team",
                     color_discrete_map={"East": "#1f77b4", "West": "#ff7f0e"})
        fig.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.write("OKC leads the league with 68 wins, and the West overall has more wins than the East. Boston is the clear top seed in the East.")

    with col2:
        fig2 = px.scatter(df, x="PPG", y="Win_PCT", text="Team", color="Conference",
                          size="Wins", title="PPG vs Win %",
                          color_discrete_map={"East": "#1f77b4", "West": "#ff7f0e"})
        fig2.update_traces(textposition="top center")
        fig2.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig2, use_container_width=True)
        st.write("Scoring more generally leads to more wins, but Indiana is an outlier; high PPG but also gives up a lot. Defense still matters.")

    st.subheader("Team Stats Heatmap")
    cols = ["PPG", "OPP_PPG", "FG_PCT", "3P_PCT", "REB", "AST"]
    hm = df.set_index("Team")[cols]
    hm_norm = (hm - hm.min()) / (hm.max() - hm.min())
    fig3 = go.Figure(go.Heatmap(z=hm_norm.values, x=cols, y=hm.index.tolist(),
                                colorscale="Blues", text=hm.values.round(1),
                                texttemplate="%{text}", showscale=True))
    fig3.update_layout(title="Normalized Stats (darker = better)", height=400,
                       margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig3, use_container_width=True)
    st.write("Boston and Denver are strong across the board. Indiana scores a ton but also allows the most points, which explains why they're not at the top.")

# --- Tab 2: Player Stats ---
with tab2:
    color_by = st.selectbox("Color scatter by:", ["PPG", "RPG", "APG", "PER", "FG_PCT"])
    col1, col2 = st.columns(2)

    with col1:
        fig4 = px.bar(players.sort_values("PPG"), x="PPG", y="Player", orientation="h",
                      color="PPG", color_continuous_scale="Oranges", title="Points Per Game")
        fig4.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig4, use_container_width=True)
        st.write("SGA is the scoring leader at 32.7 PPG, just ahead of Jokic and Giannis. LaMelo at 30.1 is a bit surprising given Charlotte's record.")

    with col2:
        fig5 = px.scatter(players, x="RPG", y="APG", size="PPG", color=color_by,
                          hover_name="Player", color_continuous_scale="Viridis",
                          title="Rebounds vs Assists (size = PPG)")
        fig5.update_layout(height=420, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig5, use_container_width=True)
        st.write("Jokic is in a league of his own, top in both rebounds and assists while scoring 30. Haliburton leads in assists at nearly 11 per game.")

    st.dataframe(players.sort_values("PPG", ascending=False).reset_index(drop=True),
                 use_container_width=True)

# --- Tab 3: Monthly Trends ---
with tab3:
    team_list = monthly["Team"].unique().tolist()
    selected = st.multiselect("Select teams:", team_list, default=team_list)
    mf = monthly[monthly["Team"].isin(selected)]
    month_order = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"]

    col1, col2 = st.columns(2)

    with col1:
        fig6 = px.line(mf, x="Month", y="Win_PCT", color="Team", markers=True,
                       title="Monthly Win %", category_orders={"Month": month_order})
        fig6.update_layout(height=380, margin=dict(l=0, r=0, t=40, b=0), yaxis_tickformat=".0%")
        st.plotly_chart(fig6, use_container_width=True)
        st.write("OKC has been the most consistent team all season, rarely dipping below 85%. Cleveland had a slow start but really picked up after December.")

    with col2:
        fig7 = px.line(mf, x="Month", y="PPG", color="Team", markers=True,
                       title="Monthly PPG", category_orders={"Month": month_order})
        fig7.update_layout(height=380, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig7, use_container_width=True)
        st.write("All three teams score more as the season goes on, which is pretty typical. Boston's January dip lines up with a tough stretch of away games.")

st.caption("Data: Basketball Reference | 2024-25 NBA Regular Season")
