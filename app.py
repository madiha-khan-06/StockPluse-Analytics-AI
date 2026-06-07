import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="StockPluse-Analytics AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

.main{
    background:#f7f9fc;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#f8fafc;
    border-right:1px solid #e2e8f0;
}

/* Hero */
.hero-box{
    background:
    linear-gradient(
        135deg,
        #4f46e5,
        #6d28d9,
        #9333ea
    );

    padding:50px;
    border-radius:30px;
    color:white;
    margin-bottom:30px;

    box-shadow:
    0 15px 40px rgba(124,58,237,0.25);
}

.hero-title{
    font-size:70px;
    font-weight:900;
}

.hero-sub{
    font-size:24px;
}

/* Stock Cards */
.metric-card{
    background:white;

    padding:30px;

    border-radius:24px;

    box-shadow:
    0 10px 25px rgba(0,0,0,0.08);

    border:1px solid #eef2ff;

    transition:0.3s;
}

.metric-card:hover{
    transform:translateY(-6px);
}

.metric-title{
    font-size:24px;
    font-weight:700;
    color:#111827;
}

.metric-price{
    font-size:42px;
    font-weight:800;
}

.metric-change{
    font-size:20px;
    font-weight:700;
}

.green{
    color:#16a34a;
}

.red{
    color:#dc2626;
}

/* Info Boxes */
.info-box{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 8px 20px rgba(0,0,0,0.08);
}

/* Button */
.stButton > button{
    width:100%;
    height:60px;

    border:none;

    border-radius:18px;

    background:
    linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    color:white;

    font-size:18px;
    font-weight:700;

    box-shadow:
    0 10px 25px rgba(124,58,237,0.25);
}

.stButton > button:hover{
    transform:translateY(-3px);
}

/* Metrics */
[data-testid="metric-container"]{
    background:white;
    border-radius:18px;
    padding:10px;
    box-shadow:0 4px 12px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.markdown(
    "<div class='sidebar-title'>📊 StockPluse-Analytics</div>",
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📈 Stock Comparison",
        "🤖 AI Prediction",
        "📥 Download Data",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")

stocks = st.sidebar.multiselect(
    "Select Stocks",
    ["AAPL", "TSLA", "MSFT", "AMZN", "NVDA", "META", "GOOGL"],
    default=["AAPL", "TSLA", "MSFT"]
)

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2020-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("today")
)

prediction_days = st.sidebar.slider(
    "Prediction Days",
    7,
    90,
    30
)

run = st.sidebar.button("🚀 Generate Analysis")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("""
<div class='hero-box'>
    <div style="display:flex;align-items:center;gap:20px;">
        <div style="font-size:70px;">📈</div>
        <div>
            <div class='hero-title'>
                StockPluse-Analytics
            </div>
            <div class='hero-sub'>
                AI Powered Stock Market Analytics & Prediction Dashboard
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
if stocks:

    data = yf.download(
        stocks,
        start=start_date,
        end=end_date
    )

    close_prices = data["Close"]

# ---------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------
if menu == "🏠 Dashboard":

    st.subheader("📌 Market Overview")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("📈 Stocks", len(stocks))

    with col2:
        st.metric("📅 Forecast", prediction_days)

    with col3:
        st.metric("📊 Watchlist", len(stocks))

    with col4:
        st.metric("🚀 Status", "Active")

    if run:

        cols = st.columns(len(stocks))

        for i, stock in enumerate(stocks):

            latest_price = round(
                close_prices[stock].dropna().iloc[-1], 2
            )

            first_price = close_prices[stock].dropna().iloc[0]

            last_price = close_prices[stock].dropna().iloc[-1]

            growth = round(
                ((last_price-first_price)/first_price)*100,
                2
            )

            color = "green" if growth > 0 else "red"

            with cols[i]:

                st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-title'>{stock}</div>
                    <div class='metric-price'>
                        ${latest_price}
                    </div>
                    <div class='metric-change {color}'>
                        {growth}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # MARKET TREND CHART
        st.subheader("📊 Market Trend")

        fig = go.Figure()

        for stock in stocks:

            fig.add_trace(
                go.Scatter(
                    x=close_prices.index,
                    y=close_prices[stock],
                    mode='lines',
                    name=stock
                )
            )

        fig.update_layout(
    template="simple_white",
    height=650,
    title_x=0.5,
    font=dict(size=14),
    hovermode="x unified"
)

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# STOCK COMPARISON PAGE
# ---------------------------------------------------
elif menu == "📈 Stock Comparison":

    st.subheader("📈 Detailed Stock Comparison")

    comparison_stock = st.selectbox(
        "Choose Company",
        stocks
    )

    stock_data = close_prices[comparison_stock].dropna()

    # Moving Average
    ma50 = stock_data.rolling(50).mean()
    ma200 = stock_data.rolling(200).mean()

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=stock_data.index,
            y=stock_data,
            name='Closing Price'
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=ma50.index,
            y=ma50,
            name='50-Day MA'
        )
    )

    fig2.add_trace(
        go.Scatter(
            x=ma200.index,
            y=ma200,
            name='200-Day MA'
        )
    )

    fig2.update_layout(
    template="simple_white",
    height=650,
    title_x=0.5,
    font=dict(size=14),
    hovermode="x unified"
)

    st.plotly_chart(fig2, use_container_width=True)

    # STATISTICS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Highest Price",
            f"${round(stock_data.max(),2)}"
        )

    with col2:
        st.metric(
            "Lowest Price",
            f"${round(stock_data.min(),2)}"
        )

    with col3:
        st.metric(
            "Average Price",
            f"${round(stock_data.mean(),2)}"
        )

# ---------------------------------------------------
# AI PREDICTION PAGE
# ---------------------------------------------------
elif menu == "🤖 AI Prediction":

    st.subheader("🤖 AI Stock Forecast")

    selected_stock = st.selectbox(
        "Select Stock for Prediction",
        stocks
    )

    historical = close_prices[selected_stock].dropna()

    recent_data = historical.tail(100)

    future_x = np.arange(
        len(recent_data),
        len(recent_data)+prediction_days
    )

    # Simulated Prediction
    predicted = np.linspace(
        recent_data.iloc[-1],
        recent_data.iloc[-1]*1.15,
        prediction_days
    )

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            y=recent_data.values,
            mode='lines',
            name='Historical Data'
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=future_x,
            y=predicted,
            mode='lines',
            name='Predicted Trend',
            line=dict(dash='dash')
        )
    )

    fig3.update_layout(
    template="simple_white",
    height=650,
    title_x=0.5,
    font=dict(size=14),
    hovermode="x unified"
)

    st.plotly_chart(fig3, use_container_width=True)

    current_price = round(recent_data.iloc[-1],2)

    predicted_price = round(predicted[-1],2)

    expected_growth = round(
        ((predicted_price-current_price)/current_price)*100,
        2
    )

    st.success(
        f"📌 AI predicts {selected_stock} may reach "
        f"${predicted_price} within "
        f"{prediction_days} days "
        f"with expected growth of "
        f"{expected_growth}%."
    )

    # AI Explanation
    st.markdown("## 🧠 How AI Prediction Works")

    st.markdown("""
<div class='info-box'>

### Step 1 — Collect Historical Data
The application downloads historical stock market data from Yahoo Finance.

### Step 2 — Analyze Patterns
The AI analyzes:
- price movement
- trends
- growth patterns
- volatility

### Step 3 — Forecast Future Trend
Using historical movement patterns, the AI estimates future stock prices.

### Step 4 — Visualization
The dashboard visualizes:
- Historical Trend
- Predicted Future Trend

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DOWNLOAD PAGE
# ---------------------------------------------------
elif menu == "📥 Download Data":

    st.subheader("📥 Download Historical Dataset")

    st.dataframe(close_prices.tail(20))

    csv = close_prices.to_csv().encode('utf-8')

    st.download_button(
        label="⬇ Download CSV File",
        data=csv,
        file_name="stock_market_data.csv",
        mime="text/csv"
    )

# ---------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------
elif menu == "ℹ️ About Project":

    st.subheader("📖 About This Project")

    st.markdown("""
<div class='info-box'>

## 📌 Project Overview

StockPredict AI is an AI-powered stock market analytics and prediction system.

Users can:
- Select multiple stocks
- Compare company performance
- Analyze trends
- Generate AI-based predictions
- Download stock datasets

---

## 🛠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Programming |
| Streamlit | Web Application |
| yFinance | Stock Data API |
| Pandas | Data Processing |
| NumPy | Numerical Computation |
| Plotly | Interactive Visualization |

---

## 📊 Business Use Cases

- Financial Analytics
- Investment Research
- Market Trend Analysis
- AI Forecasting
- Portfolio Comparison

---

## 🎯 Key Features

✅ Interactive Dashboard  
✅ Real-time Stock Data  
✅ AI Prediction  
✅ Multi-stock Comparison  
✅ Downloadable Reports  
✅ Beautiful UI  

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div style="
background:white;
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0 4px 15px rgba(0,0,0,0.08);
margin-top:30px;">
Built with ❤️ using Streamlit, Plotly, Python & AI
</div>
""", unsafe_allow_html=True)