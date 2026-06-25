import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(
    page_title="Soccer 2026 Match Predictor",
    page_icon="⚽",
    layout="centered",
)


@st.cache_resource
def load_artifacts():
    model = joblib.load("models/match_predictor.pkl")
    team_data = joblib.load("models/team_data.pkl")
    return model, team_data["team_stats"], team_data["feature_cols"]


model, team_stats, feature_cols = load_artifacts()

st.title("⚽ Soccer 2026 Match Predictor")
st.caption("Predictions based on historical international football results (1872–2026).")

team_names = sorted(team_stats.keys())

col1, col2 = st.columns(2)
with col1:
    default_a = team_names.index("Brazil") if "Brazil" in team_names else 0
    team_a = st.selectbox("Team A", team_names, index=default_a)
with col2:
    default_b = team_names.index("Argentina") if "Argentina" in team_names else 1
    team_b = st.selectbox("Team B", team_names, index=default_b)

is_neutral = st.checkbox("Neutral venue", value=True)
is_major   = st.checkbox("Major tournament (e.g. World Cup)", value=True)

if st.button("Predict", type="primary", use_container_width=True):
    if team_a == team_b:
        st.error("Please pick two different teams.")
    else:
        stats_a = team_stats[team_a]
        stats_b = team_stats[team_b]

        row = pd.DataFrame([{
            "team_a_winrate":      stats_a["winrate"],
            "team_b_winrate":      stats_b["winrate"],
            "team_a_goal_avg":     stats_a["goal_avg"],
            "team_b_goal_avg":     stats_b["goal_avg"],
            "team_a_recent_form":  stats_a["recent_form"],
            "team_b_recent_form":  stats_b["recent_form"],
            "is_neutral":          int(is_neutral),
            "is_major_tournament": int(is_major),
        }]).reindex(columns=feature_cols)

        proba = model.predict_proba(row)[0]
        p_a, p_draw, p_b = float(proba[0]), float(proba[1]), float(proba[2])

        # --- Metrics ---
        m1, m2, m3 = st.columns(3)
        m1.metric(f"{team_a} wins", f"{p_a * 100:.1f}%")
        m2.metric("Draw",           f"{p_draw * 100:.1f}%")
        m3.metric(f"{team_b} wins", f"{p_b * 100:.1f}%")

        # --- Progress bars ---
        st.progress(p_a,    text=f"{team_a} wins")
        st.progress(p_draw, text="Draw")
        st.progress(p_b,    text=f"{team_b} wins")

        # --- Team stats table ---
        st.table(
            pd.DataFrame(
                {
                    "Win rate":            [round(stats_a["winrate"],      3), round(stats_b["winrate"],      3)],
                    "Avg goals scored":    [round(stats_a["goal_avg"],     3), round(stats_b["goal_avg"],     3)],
                    "Recent form (last 10)":[round(stats_a["recent_form"], 3), round(stats_b["recent_form"], 3)],
                    "Matches played":      [stats_a["matches_played"],        stats_b["matches_played"]],
                },
                index=[team_a, team_b],
            )
        )
