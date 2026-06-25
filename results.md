# Lab Results & Key Takeaways

## Dataset

| Metric | Value |
|---|---|
| Total matches | 49,329 |
| Date range | 1872-11-30 → 2026-06-27 |
| Columns | date, home_team, away_team, home_score, away_score, tournament, city, country, neutral |

---

## Task 3: Data Exploration

### Top 10 Tournaments by Match Count

| Tournament | Matches |
|---|---|
| Friendly | 18,257 |
| Soccer World Cup qualification | 8,771 |
| UEFA Euro qualification | 2,824 |
| African Cup of Nations qualification | 2,327 |
| Soccer World Cup | 1,036 |
| Copa América | 869 |
| African Cup of Nations | 845 |
| AFC Asian Cup qualification | 829 |
| UEFA Nations League | 658 |
| CECAFA Cup | 620 |

### Top 15 Teams by Total Matches Played

| Team | Matches |
|---|---|
| Sweden | 1,102 |
| England | 1,091 |
| Argentina | 1,069 |
| Brazil | 1,060 |
| Germany | 1,032 |
| South Korea | 1,008 |
| Hungary | 1,004 |
| Mexico | 1,003 |
| Uruguay | 973 |
| France | 936 |
| Italy | 891 |
| Poland | 890 |
| Switzerland | 885 |
| Netherlands | 880 |
| Norway | 873 |

### Matches Per Decade

| Decade | Matches |
|---|---|
| 1870s | 13 |
| 1880s | 55 |
| 1890s | 59 |
| 1900s | 137 |
| 1910s | 330 |
| 1920s | 831 |
| 1930s | 1,079 |
| 1940s | 833 |
| 1950s | 1,651 |
| 1960s | 2,971 |
| 1970s | 4,133 |
| 1980s | 5,025 |
| 1990s | 6,944 |
| 2000s | 9,526 |
| 2010s | 9,787 |
| 2020s | 5,955 |

> International football has grown exponentially — the 2010s had ~750× more matches than the 1870s.

---

## Task 4 & 5: Feature Engineering & Data Split

- **Feature engineering window:** 1990-01-01 onward → **32,212 matches** with 8 engineered features
- **Training set:** matches before 2018-01-01 → **24,179 rows**
- **Test set:** matches from 2018-01-01 onward → **8,033 rows**

### Training Class Distribution

| Outcome | Proportion |
|---|---|
| Home win | 48.7% |
| Away win | 27.6% |
| Draw | 23.7% |

> Home advantage is real — nearly half of all matches are won by the home side.

---

## Task 6: Model Performance

**Model:** Random Forest (`n_estimators=200`, `max_depth=12`, `random_state=42`)

| Metric | Value |
|---|---|
| **Test accuracy** | **55.98%** |
| Baseline (always predict home win) | 47.19% |
| Improvement over baseline | +8.79 pp |

### Confusion Matrix

|  | Pred: Home win | Pred: Draw | Pred: Away win |
|---|---|---|---|
| **Actual: Home win** | 3,393 | 34 | 364 |
| **Actual: Draw** | 1,390 | 29 | 419 |
| **Actual: Away win** | 1,277 | 52 | 1,075 |

> The model struggles most with draws — a known challenge in football prediction due to their relative unpredictability.

### Feature Importances

| Feature | Importance |
|---|---|
| team_b_winrate | 0.2203 |
| team_a_winrate | 0.2062 |
| team_b_goal_avg | 0.1889 |
| team_a_goal_avg | 0.1821 |
| team_b_recent_form | 0.0752 |
| team_a_recent_form | 0.0750 |
| is_neutral | 0.0275 |
| is_major_tournament | 0.0248 |

> Historical win rate and goal-scoring average are by far the strongest predictors. Recent form matters but is secondary. Match context (neutral venue, tournament type) has relatively little predictive power.

---

## Task 7: Team Statistics Saved

- **215 World Cup-eligible teams** stored in `models/team_data.pkl`

### Top 5 Teams by Win Rate (≥ 100 matches)

| Team | Win Rate | Matches Played |
|---|---|---|
| Brazil | 63.2% | 1,060 |
| Spain | 58.7% | 784 |
| Germany | 57.8% | 1,032 |
| England | 57.1% | 1,091 |
| Iran | 56.6% | 613 |

---

## Task 8: Sample Predictions

| Match | Team A Win | Draw | Team B Win |
|---|---|---|---|
| Brazil vs Argentina | 33.0% | 31.7% | **35.3%** |
| Germany vs Brazil | **51.0%** | 21.8% | 27.2% |

> Brazil vs Argentina is almost a coin flip — both teams are very evenly matched historically. Germany holds a clear edge over Brazil in a neutral major tournament context.

---

## Key Takeaways

1. **AI-assisted development works** — the entire ML pipeline (data loading, feature engineering, model training, and a web app) was built through prompted code generation with IBM Bob.
2. **Historical performance predicts future results** — win rate and goal average together account for ~80% of the model's feature importance.
3. **55.98% accuracy beats a naive baseline by ~9 points**, meaningful in a 3-class problem (home win / draw / away win) where random chance would give ~33%.
4. **Draws are the hardest outcome to predict** — the model correctly identified only 29 of 1,838 actual draws in the test set.
5. **Football is inherently uncertain** — even the best historical features leave ~44% of outcomes unpredictable, reflecting the sport's appeal.
