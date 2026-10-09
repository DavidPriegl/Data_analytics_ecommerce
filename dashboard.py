import os

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = 'data/python_data_analytics_cleaned.csv'

st.set_page_config(page_title='E-commerce Dashboard', layout='wide')


@st.cache_data
def load_data(path, mtime):
    # mtime is part of the cache key, so re-running the notebook's to_csv refreshes the data
    df = pd.read_csv(path, parse_dates=['OrderDate'])
    return df


df = load_data(DATA_PATH, os.path.getmtime(DATA_PATH))

st.title('E-commerce Dashboard')

# Sidebar filters
st.sidebar.header('Filters')
min_d, max_d = df['OrderDate'].min().date(), df['OrderDate'].max().date()
date_range = st.sidebar.date_input('Order date', (min_d, max_d), min_value=min_d, max_value=max_d)
regions = st.sidebar.multiselect('Region', sorted(df['Region'].unique()), default=sorted(df['Region'].unique()))
types = st.sidebar.multiselect(
    'Customer type', sorted(df['CustomerType'].unique()), default=sorted(df['CustomerType'].unique())
)
if st.sidebar.button('Reload data'):
    st.cache_data.clear()
    st.rerun()

mask = df['Region'].isin(regions) & df['CustomerType'].isin(types)
if len(date_range) == 2:
    start, end = date_range
    in_range = df['OrderDate'].between(pd.Timestamp(start), pd.Timestamp(end))
    # rows with no date stay in unless the user narrows the range
    mask &= in_range | (df['OrderDate'].isna() & ((start, end) == (min_d, max_d)))
f = df[mask]

if f.empty:
    st.warning('No data for the selected filters.')
    st.stop()

# KPIs
revenue = f['Revenue'].sum()
orders = f['OrderID'].nunique()
c1, c2, c3, c4 = st.columns(4)
c1.metric('Total revenue', f'${revenue:,.0f}')
c2.metric('Orders', f'{orders:,}')
c3.metric('Customers', f"{f['CustomerID'].nunique():,}")
c4.metric('Avg order value', f'${revenue / orders:,.2f}')

left, right = st.columns(2)

# Top 5 products
top5 = f.groupby('Product')['Revenue'].sum().nlargest(5).sort_values().reset_index()
fig = px.bar(top5, x='Revenue', y='Product', orientation='h', text_auto='$,.0f', title='Top 5 products by revenue')
fig.update_layout(yaxis_title=None, xaxis_title=None)
left.plotly_chart(fig, width='stretch')

# Revenue by region
reg = f.groupby('Region')['Revenue'].sum().sort_values(ascending=False).reset_index()
fig = px.bar(reg, x='Region', y='Revenue', text_auto='$,.0f', title='Revenue by region')
fig.update_layout(xaxis_title=None, yaxis_title=None)
right.plotly_chart(fig, width='stretch')

# Customer type summary
st.subheader('Customer type summary')
summary = (
    f.groupby('CustomerType')
    .agg(TotalRevenue=('Revenue', 'sum'), Orders=('OrderID', 'nunique'), AvgOrderValue=('Revenue', 'mean'))
    .sort_values('TotalRevenue', ascending=False)
)
summary['RevenueShare'] = summary['TotalRevenue'] / summary['TotalRevenue'].sum()
t1, t2 = st.columns([3, 2])
t1.dataframe(
    summary,
    width='stretch',
    column_config={
        'TotalRevenue': st.column_config.NumberColumn('Total revenue', format='$%,.0f'),
        'AvgOrderValue': st.column_config.NumberColumn('Avg order value', format='$%.2f'),
        'RevenueShare': st.column_config.ProgressColumn('Share', format='percent', min_value=0, max_value=1),
    },
)
fig = px.pie(summary.reset_index(), names='CustomerType', values='TotalRevenue', hole=0.5)
t2.plotly_chart(fig, width='stretch')
