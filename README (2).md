# Customer Segmentation Project

Team project: group customers into segments (High-Value, Regular,
Low-Spending) using clustering, and present it through a dashboard.

## Project goal

Analyze customer data (age, income, spending, purchase frequency) and
automatically group customers into meaningful segments to support
business decisions (e.g. who to target with loyalty offers vs. who's
already high-value).

## Team roles (Week 1)

| Role | This week's job |
|---|---|
| Data Engineer | Load the real dataset, check types/nulls/duplicates, put clean data in `/data/processed` |
| ML Engineer | Research clustering (K-Means) + RFM theory, prep for Week 2 modeling |
| Dashboard Dev | Get the Streamlit skeleton in `/dashboard` running locally |
| Analyst / PM | Draft the report outline in `/docs`, track decisions and insights |

## Folder structure

```
/data
  /raw          <- original, untouched dataset files
  /processed    <- cleaned data, ready for modeling
/notebooks      <- exploration and modeling code
/dashboard      <- the Streamlit app
/docs           <- report, slides, write-ups
```

## Dataset

Using the **Mall Customer Segmentation** dataset (Kaggle). Search
"Mall Customer Segmentation Data" on kaggle.com and download
`Mall_Customers.csv` into `/data/raw` — it's a small, free, public
dataset with columns for CustomerID, Gender, Age, Annual Income, and
Spending Score.

A synthetic stand-in (`customers_sample.csv`, made with
`generate_sample_data.py`) is included in `/data/raw` so you can test
the pipeline today before the real dataset is downloaded and swapped
in.

## Setup (everyone should do this once)

```
pip install pandas scikit-learn matplotlib seaborn streamlit
```

## Running things

```
python notebooks/segmentation.py      # runs clustering, saves plots + labeled CSV
streamlit run dashboard/dashboard.py  # opens the interactive dashboard
```

## Git workflow

1. One person creates the repo on GitHub and adds the other 3 as collaborators.
2. Everyone clones it: `git clone <repo-url>`
3. Each person works in their own branch: `git checkout -b your-name-week1`
4. Commit and push your work, then open a Pull Request to merge into `main`.
5. Review each other's PRs before merging so everyone knows what changed.

## Week 1 checklist

- [ ] Repo created, everyone has access and has cloned it
- [ ] Real dataset downloaded into `/data/raw`
- [ ] Data loaded, checked for nulls/duplicates/outliers (Data Engineer)
- [ ] EDA done: histograms, boxplots, correlation heatmap (whoever's free — good to split by column)
- [ ] Cleaning decisions documented in `/docs`
- [ ] Dashboard skeleton runs locally without errors (Dashboard Dev)
- [ ] Report outline drafted (Analyst/PM)
- [ ] Feature list for clustering finalized (likely: Age, Annual Income, Spending Score)
