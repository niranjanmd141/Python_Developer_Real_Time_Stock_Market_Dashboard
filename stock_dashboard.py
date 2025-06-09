import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
from datetime import datetime, timedelta

# --- Configuration and Setup ---

# Set the page configuration for a wider layout
st.set_page_config(layout="wide", page_title="Real-Time Stock Dashboard")

# --- Helper Functions ---

def get_simulated_stock_data(symbol, days=30):
    """
    Simulates historical stock data for a given symbol and generates a 'live' price.
    This function replaces a real API call for demonstration purposes.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL').
        days (int): Number of days for historical data simulation.

    Returns:
        pd.DataFrame: A DataFrame with 'Date', 'Close', and 'Volume' columns.
                      'Close' price includes a simulated real-time fluctuation.
    """
    today = datetime.now()
    dates = [today - timedelta(days=i) for i in range(days -1, -1, -1)] # Dates from oldest to newest

    # Simulate base historical prices
    base_price = random.uniform(100, 500)
    prices = [base_price * (1 + random.uniform(-0.02, 0.03)) for _ in range(days)]
    volumes = [random.randint(1_000_000, 10_000_000) for _ in range(days)]

    df = pd.DataFrame({
        'Date': dates,
        'Close': prices,
        'Volume': volumes
    })

    # Simulate a small real-time fluctuation for the latest price
    # This will be applied on every 'refresh' to show movement
    current_live_fluctuation = random.uniform(-1, 1) # Small random change
    df.loc[df.index[-1], 'Close'] += current_live_fluctuation

    return df

# --- Streamlit App Layout ---

st.title("📈 Real-Time Stock Market Dashboard")

# Sidebar for user inputs
st.sidebar.header("Settings")
# Text input for stock symbol
stock_symbol = st.sidebar.text_input(
    "Enter Stock Symbol (e.g., AAPL, GOOGL)",
    "AAPL"
).upper() # Convert to uppercase for consistency

# Refresh interval slider (for simulated real-time)
refresh_interval = st.sidebar.slider(
    "Refresh Interval (seconds, for demo)",
    min_value=1,
    max_value=10,
    value=3
)

# Placeholder for dynamic content
live_data_placeholder = st.empty()

# --- Main Dashboard Logic ---

def update_dashboard():
    """
    Fetches (simulated) data and updates the dashboard.
    """
    with live_data_placeholder.container():
        st.subheader(f"Live Data for {stock_symbol}")

        # Get simulated stock data
        stock_df = get_simulated_stock_data(stock_symbol)

        if not stock_df.empty:
            # Display current metrics
            latest_data = stock_df.iloc[-1]
            st.markdown(f"""
                <div style="
                    background-color: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    text-align: center;
                ">
                    <h3 style="color: #333; margin-bottom: 10px;">Current Price:
                        <span style="color: { 'green' if latest_data['Close'] > stock_df.iloc[-2]['Close'] else 'red' if latest_data['Close'] < stock_df.iloc[-2]['Close'] else 'black' };
                        font-size: 2.5em; font-weight: bold;">
                        ${latest_data['Close']:.2f}
                        </span>
                    </h3>
                    <p style="color: #555; font-size: 1.1em;">
                        As of: {latest_data['Date'].strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
            """, unsafe_allow_html=True)


            # Create a Plotly line chart for stock price
            fig_price = px.line(
                stock_df,
                x='Date',
                y='Close',
                title=f'{stock_symbol} Stock Price Over Time',
                labels={'Close': 'Closing Price ($)', 'Date': 'Date'},
                template="plotly_white"
            )
            fig_price.update_traces(mode='lines+markers', line=dict(width=2))
            fig_price.update_layout(hovermode="x unified") # Enhanced hover functionality
            st.plotly_chart(fig_price, use_container_width=True)

            # Create a Plotly bar chart for volume
            fig_volume = px.bar(
                stock_df,
                x='Date',
                y='Volume',
                title=f'{stock_symbol} Trading Volume',
                labels={'Volume': 'Volume', 'Date': 'Date'},
                template="plotly_white",
                color_discrete_sequence=['#636EFA'] # A nice blue color
            )
            fig_volume.update_layout(hovermode="x unified")
            st.plotly_chart(fig_volume, use_container_width=True)

            st.markdown("---")
            st.write("### Raw Data (Last 5 entries)")
            st.dataframe(stock_df.tail())

        else:
            st.warning(f"Could not retrieve data for {stock_symbol}. Please check the symbol.")

# --- Real-Time Refresh Loop ---
# This loop simulates real-time updates by re-running the dashboard logic periodically.
while True:
    update_dashboard()
    time.sleep(refresh_interval) # Wait for the specified interval before refreshing
