# NBA 2024-25 Season Analytics Dashboard

An interactive Streamlit dashboard analyzing NBA team and player performance for the 2024-25 season.

**Live App:** [link](https://your-app-url.streamlit.app)  
**GitHub:** [link](https://github.com/Krupsbhojani/SUNY_DATA_VIZ_Assignment_5)
---

## What it does

Tracks team wins, scoring trends, and player stats across the 2024-25 NBA season using charts, filters, and monthly breakdowns.

---

## Data Source

- **Where:** [Basketball Reference](https://www.basketball-reference.com)
- **What:** Team and player stats from the 2024-25 regular season
- **How collected:** Manually copied from the team and player summary pages into the app

## How to Update

At the end of each new season, go to Basketball Reference, grab the updated team/player stats, and replace the numbers in the `app.py` DataFrames. No API or credentials needed.

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New App** → select this repo → set `app.py` as main file → **Deploy**
