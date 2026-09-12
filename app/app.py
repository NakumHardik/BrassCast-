import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="BrassCast", layout="wide", page_icon="📈")

# --- 2. Sidebar Controls ---
st.sidebar.title("🏭 BrassCast")
st.sidebar.markdown("Predictive Raw Material Dashboard")
st.sidebar.divider()

# Let user pick which model to use (if they ran notebooks 4, 5, and 6, they have multiple!)
if os.path.exists('models'):
    model_files = [f for f in os.listdir('models') if f.endswith('.joblib')]
else:
    model_files = []

if not model_files:
    st.sidebar.error("No models found! Please run the training notebooks first.")
    st.stop()

selected_model = st.sidebar.selectbox("🧠 Select AI Model", model_files)

st.sidebar.divider()
st.sidebar.info("This dashboard uses Global Commodity data to predict Indian Brass prices.")

# --- 3. Load Data & Model ---
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/ml_features.csv', index_col=0, parse_dates=True)

@st.cache_resource
def load_model(model_name):
    return joblib.load(f'models/{model_name}')

df = load_data()
model = load_model(selected_model)

# Limit data to last 2 years for a cleaner chart
display_df = df.tail(500)

# --- 4. Top Row Metrics ---
st.title("📈 Market Intelligence Dashboard")

latest = df.iloc[-1]
prev = df.iloc[-2]

current_price = latest['Brass_Cost']
price_change = current_price - prev['Brass_Cost']
pct_change = (price_change / prev['Brass_Cost']) * 100

col1, col2, col3 = st.columns(3)

# Metric 1: Current Price
col1.metric("Current Brass Cost", f"₹{current_price:.2f}/kg", f"{price_change:+.2f} ({pct_change:+.2f}%)")

# Metric 2: Market Risk
volatility = latest['Volatility_14d'] * 100
col2.metric("14-Day Volatility Risk", f"{volatility:.2f}%")

# Metric 3: AI Prediction
feature_columns = ['copper_Close', 'zinc_proxy_Close', 'usdinr_Close', 'crude_Close', 'copx_Close', 'Brass_Cost', 'Daily_Return', 'SMA_10', 'SMA_30', 'Volatility_14d']
prediction = model.predict(df[feature_columns].iloc[-1:])

if prediction[0] == 1:
    col3.metric("AI 5-Day Forecast", "UP ⬆️", "Bullish", delta_color="normal")
    st.success("🤖 **Procurement Strategy:** Prices are expected to rise. Consider locking in raw material orders now.")
else:
    col3.metric("AI 5-Day Forecast", "DOWN ⬇️", "Bearish", delta_color="inverse")
    st.error("🤖 **Procurement Strategy:** Prices are expected to drop. Consider delaying non-urgent purchases.")

# --- 5. Interactive Advanced Charts (Like StockVision) ---
st.markdown("### 📊 Technical Analysis")

# Create a chart with 2 rows (Top is price, bottom is daily returns)
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])

# Add Brass Cost Line
fig.add_trace(go.Scatter(x=display_df.index, y=display_df['Brass_Cost'], name='Brass Cost (₹/kg)', line=dict(color='#ff9900', width=2)), row=1, col=1)

# Add Moving Averages
fig.add_trace(go.Scatter(x=display_df.index, y=display_df['SMA_10'], name='10-Day SMA', line=dict(color='#00d4ff', width=1, dash='dot')), row=1, col=1)
fig.add_trace(go.Scatter(x=display_df.index, y=display_df['SMA_30'], name='30-Day SMA', line=dict(color='#ff0055', width=1, dash='dot')), row=1, col=1)

# Add Daily Returns (Bar Chart)
colors = ['#00ff00' if val > 0 else '#ff0000' for val in display_df['Daily_Return']]
fig.add_trace(go.Bar(x=display_df.index, y=display_df['Daily_Return'], name='Daily Return', marker_color=colors), row=2, col=1)

fig.update_layout(
    height=650, 
    template="plotly_dark", 
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)