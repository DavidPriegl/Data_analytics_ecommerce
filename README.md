# E-commerce Analytics

Cleaning and analysis of simulated e-commerce orders (`main.ipynb`), plus a live dashboard.

## Dashboard

`dashboard.py` is a Streamlit dashboard showing the top 5 products, revenue by region and a customer type summary, with filters for date, region and customer type. It reads `data/python_data_analytics_cleaned.csv`, which is written by the last cell of `main.ipynb`, and reloads when that file changes.

`dashboard.py` was created by Claude (Anthropic's Claude Code)

```
pip install -r requirements.txt
streamlit run dashboard.py
```
