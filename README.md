# 🏭 BrassCast - Raw Material Predictor

An end-to-end Machine Learning pipeline and interactive dashboard designed to predict raw material (Brass) cost volatility using global commodity prices.

## 🚀 Features
- **Data Engineering:** Automated fetching of 15+ years of global market data (Copper, Zinc, USD/INR, Crude Oil).
- **Feature Engineering:** Computes a custom Synthetic Brass Index, Moving Averages (SMA), and Volatility metrics.
- **Machine Learning:** Uses a Random Forest Classifier (trained chronologically to prevent lookahead bias) to predict price direction over a 5-day horizon.
- **Interactive Dashboard:** Built with Streamlit and Plotly to provide a real-time, user-friendly interface.

## 💻 How to Run Locally
1. Clone the repository.
2. Install requirements: \pip install -r requirements.txt\" >> README.md
echo 
3.
Run
the
app:
\streamlit
run
app/app.py\"
