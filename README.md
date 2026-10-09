# E-commerce Analytics

Cleaning and analysis of simulated e-commerce orders (`main.ipynb`), plus a live dashboard.

## Dashboard

`dashboard.py` is a Streamlit dashboard showing the top 5 products, revenue by region and a customer type summary, with filters for date, region and customer type. It runs the code cells of `main.ipynb` (loading and cleaning the raw CSV) and uses the resulting dataframe, reloading when the notebook changes.

`dashboard.py` was created by Claude (Anthropic's Claude Code)

```
pip install -r requirements.txt
streamlit run dashboard.py
```
