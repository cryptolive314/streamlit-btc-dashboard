import streamlit as st
import pandas as pd
import requests
import json
import os
import time
from datetime import datetime
import plotly.graph_objects as go

# Configure the page
st.set_page_config(
    page_title="Hummingbot BTC Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #0068C9;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .success-text {
        color: #00CC96;
        font-weight: bold;
    }
    .warning-text {
        color: #FFA15A;
        font-weight: bold;
    }
    .danger-text {
        color: #FF4B4B;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>Hummingbot BTC Trading Dashboard</h1>", unsafe_allow_html=True)

# Initialize session state variables
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
if 'strategies' not in st.session_state:
    st.session_state.strategies = []
if 'api_credentials' not in st.session_state:
    st.session_state.api_credentials = {}
if 'active_positions' not in st.session_state:
    st.session_state.active_positions = []
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'account_balance' not in st.session_state:
    st.session_state.account_balance = 0
if 'pnl' not in st.session_state:
    st.session_state.pnl = 0

# Sidebar for navigation
with st.sidebar:
    st.image("https://hummingbot.org/hummingbot-icon.png", width=100)
    st.markdown("## BTC Trading Dashboard")
    
    if not st.session_state.login_status:
        with st.form("login_form"):
            st.markdown("### Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username == "admin" and password == "admin":
                    st.success("Login successful!")
                    st.session_state.login_status = True
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials!")
    
    else:
        # Navigation menu
        page = st.radio("Navigation", ["Dashboard", "API Credentials", "Strategies", "Trading History", "Settings"])
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.login_status = False
            st.experimental_rerun()

# Main content
if not st.session_state.login_status:
    st.info("Please login using the form in the sidebar to access the dashboard.")
else:
    if page == "Dashboard":
        # Overview section with key metrics
        st.markdown("<h2 class='section-header'>Trading Overview</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='card'><h3>Account Balance</h3><p class='success-text'>$1,000.00 USDT</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='card'><h3>Active Positions</h3><p class='warning-text'>1 BTC-USDT</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='card'><h3>24h PnL</h3><p class='success-text'>+$25.35 (2.5%)</p></div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div class='card'><h3>Strategy Status</h3><p class='success-text'>Running</p></div>", unsafe_allow_html=True)
        
        # Mock BTC price chart
        st.markdown("<h2 class='section-header'>BTC-USDT Price Chart</h2>", unsafe_allow_html=True)
        
        # Create sample price data
        dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
        btc_prices = [
            63000, 62500, 62800, 63200, 64000, 63800, 63500, 64200, 65000, 64800,
            65500, 66000, 65800, 65300, 66200, 67000, 66800, 66500, 67500, 68000,
            67800, 67500, 68200, 69000, 68500, 68000, 69500, 70000, 69800, 69500
        ]
        
        df = pd.DataFrame({
            'Date': dates,
            'Price': btc_prices
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], mode='lines', name='BTC-USDT'))
        fig.update_layout(
            title='BTC-USDT Price',
            xaxis_title='Date',
            yaxis_title='Price (USDT)',
            height=500,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Active positions
        st.markdown("<h2 class='section-header'>Active Positions</h2>", unsafe_allow_html=True)
        
        positions_data = {
            'Trading Pair': ['BTC-USDT'],
            'Type': ['Long'],
            'Entry Price': ['$68,250.00'],
            'Current Price': ['$69,500.00'],
            'Size': ['0.001 BTC'],
            'Leverage': ['20x'],
            'PnL': ['+$25.00 (1.8%)'],
            'Stop Loss': ['$64,837.50 (-5%)'],
            'Take Profit': ['$69,615.00 (+2%)']
        }
        
        positions_df = pd.DataFrame(positions_data)
        st.dataframe(positions_df, use_container_width=True)
        
        # Recent trades
        st.markdown("<h2 class='section-header'>Recent Trades</h2>", unsafe_allow_html=True)
        
        trades_data = {
            'Time': ['2023-03-15 14:30:22', '2023-03-15 10:15:05', '2023-03-14 22:45:30'],
            'Trading Pair': ['BTC-USDT', 'BTC-USDT', 'BTC-USDT'],
            'Type': ['Buy', 'Sell', 'Buy'],
            'Price': ['$68,250.00', '$67,890.00', '$66,450.00'],
            'Amount': ['0.001 BTC', '0.0015 BTC', '0.001 BTC'],
            'Fee': ['$0.14', '$0.20', '$0.13'],
            'PnL': ['--', '+$45.32', '--']
        }
        
        trades_df = pd.DataFrame(trades_data)
        st.dataframe(trades_df, use_container_width=True)
    
    elif page == "API Credentials":
        st.markdown("<h2 class='section-header'>API Credentials</h2>", unsafe_allow_html=True)
        
        # Display current credentials
        st.markdown("<h3>Current API Credentials</h3>", unsafe_allow_html=True)
        
        # Sample credential
        credential = {
            'name': 'KuCoin-BTC-Strategy',
            'exchange': 'KuCoin Perpetual',
            'api_key': '67d7257b1d0ebb000196f785',
            'api_secret': '********-****-****-****-************',
            'passphrase': '**************'
        }
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {credential['name']}")
            st.markdown(f"**Exchange:** {credential['exchange']}")
            st.markdown(f"**API Key:** {credential['api_key']}")
        with col2:
            st.markdown(f"**API Secret:** {credential['api_secret']}")
            st.markdown(f"**Passphrase:** {credential['passphrase']}")
        
        # Form to add new credentials
        st.markdown("<h3>Add New Credential</h3>", unsafe_allow_html=True)
        
        with st.form("credential_form"):
            name = st.text_input("Credential Name")
            exchange = st.selectbox("Exchange", ["KuCoin Perpetual", "Binance", "Bybit", "OKX"])
            api_key = st.text_input("API Key")
            api_secret = st.text_input("API Secret", type="password")
            passphrase = st.text_input("API Passphrase (if applicable)", type="password")
            
            submit_button = st.form_submit_button("Save Credential")
            
            if submit_button:
                if name and exchange and api_key and api_secret:
                    st.success(f"Credential '{name}' for {exchange} saved successfully!")
                else:
                    st.error("Please fill in all required fields.")
    
    elif page == "Strategies":
        st.markdown("<h2 class='section-header'>Strategies</h2>", unsafe_allow_html=True)
        
        # Current strategy configuration
        st.markdown("<h3>Current Strategy Configuration</h3>", unsafe_allow_html=True)
        
        strategy_config = {
            'name': 'BTC-Liquidation-Strategy',
            'type': 'Bollinger Bands',
            'trading_pair': 'BTC-USDT',
            'candles_interval': '3m',
            'total_amount': '1000 USDT',
            'leverage': '20x',
            'max_executors': '5',
            'cooldown_time': '60 minutes',
            'position_mode': 'HEDGE',
            'stop_loss': '5%',
            'take_profit': '2%',
            'bollinger_length': '100',
            'std_dev': '2.00',
            'long_threshold': '0.00',
            'short_threshold': '1.00'
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Strategy Name:** {strategy_config['name']}")
            st.markdown(f"**Strategy Type:** {strategy_config['type']}")
            st.markdown(f"**Trading Pair:** {strategy_config['trading_pair']}")
            st.markdown(f"**Candles Interval:** {strategy_config['candles_interval']}")
            st.markdown(f"**Amount:** {strategy_config['total_amount']}")
        with col2:
            st.markdown(f"**Leverage:** {strategy_config['leverage']}")
            st.markdown(f"**Max Executors:** {strategy_config['max_executors']}")
            st.markdown(f"**Cooldown Time:** {strategy_config['cooldown_time']}")
            st.markdown(f"**Position Mode:** {strategy_config['position_mode']}")
            st.markdown(f"**Stop Loss:** {strategy_config['stop_loss']}")
        with col3:
            st.markdown(f"**Take Profit:** {strategy_config['take_profit']}")
            st.markdown(f"**Bollinger Length:** {strategy_config['bollinger_length']}")
            st.markdown(f"**Std Dev:** {strategy_config['std_dev']}")
            st.markdown(f"**Long Threshold:** {strategy_config['long_threshold']}")
            st.markdown(f"**Short Threshold:** {strategy_config['short_threshold']}")
        
        # Form to create a new strategy
        st.markdown("<h3>Create New Strategy</h3>", unsafe_allow_html=True)
        
        strategy_types = ["Bollinger Bands", "MACD", "RSI", "Pure Market Making", "Cross-Exchange Market Making"]
        
        with st.form("strategy_form"):
            strategy_name = st.text_input("Strategy Name")
            strategy_type = st.selectbox("Strategy Type", strategy_types)
            trading_pair = st.text_input("Trading Pair", "BTC-USDT")
            
            col1, col2 = st.columns(2)
            with col1:
                candles_interval = st.selectbox("Candles Interval", ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"])
                total_amount = st.number_input("Total Amount (USDT)", min_value=10.0, max_value=10000.0, value=1000.0, step=10.0)
                leverage = st.slider("Leverage", min_value=1, max_value=20, value=3)
                position_mode = st.selectbox("Position Mode", ["HEDGE", "ONE-WAY"])
            with col2:
                stop_loss = st.slider("Stop Loss (%)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
                take_profit = st.slider("Take Profit (%)", min_value=1.0, max_value=10.0, value=2.0, step=0.5)
                cooldown_time = st.slider("Cooldown Time (minutes)", min_value=1, max_value=120, value=5)
                max_executors = st.slider("Max Executors Per Side", min_value=1, max_value=10, value=5)
            
            st.markdown("### Strategy-Specific Parameters")
            if strategy_type == "Bollinger Bands":
                bb_length = st.slider("Bollinger Band Length", min_value=10, max_value=200, value=20)
                std_dev = st.slider("Standard Deviation", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
                long_threshold = st.slider("Long Threshold", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
                short_threshold = st.slider("Short Threshold", min_value=0.0, max_value=1.0, value=1.0, step=0.1)
            
            submit_button = st.form_submit_button("Create Strategy")
            
            if submit_button:
                if strategy_name and trading_pair:
                    st.success(f"Strategy '{strategy_name}' created successfully!")
                else:
                    st.error("Please fill in all required fields.")
    
    elif page == "Trading History":
        st.markdown("<h2 class='section-header'>Trading History</h2>", unsafe_allow_html=True)
        
        # Date range picker
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2023, 3, 1))
        with col2:
            end_date = st.date_input("End Date", datetime(2023, 3, 16))
        
        # Sample trade history data
        trades_data = {
            'Time': [
                '2023-03-15 14:30:22', '2023-03-15 10:15:05', '2023-03-14 22:45:30',
                '2023-03-14 16:20:45', '2023-03-14 09:35:12', '2023-03-13 20:10:33',
                '2023-03-13 14:55:29', '2023-03-13 08:40:16', '2023-03-12 22:25:08',
                '2023-03-12 16:10:42'
            ],
            'Trading Pair': ['BTC-USDT'] * 10,
            'Type': ['Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell'],
            'Price': [
                '$68,250.00', '$67,890.00', '$66,450.00', '$66,980.00', '$65,750.00',
                '$66,320.00', '$64,890.00', '$65,240.00', '$63,750.00', '$64,320.00'
            ],
            'Amount': [
                '0.001 BTC', '0.0015 BTC', '0.001 BTC', '0.002 BTC', '0.001 BTC',
                '0.0018 BTC', '0.001 BTC', '0.0012 BTC', '0.001 BTC', '0.0014 BTC'
            ],
            'Fee': [
                '$0.14', '$0.20', '$0.13', '$0.27', '$0.13',
                '$0.24', '$0.13', '$0.16', '$0.13', '$0.18'
            ],
            'PnL': [
                '--', '+$45.32', '--', '-$22.45', '--',
                '+$37.82', '--', '+$18.65', '--', '+$28.93'
            ]
        }
        
        trades_df = pd.DataFrame(trades_data)
        st.dataframe(trades_df, use_container_width=True)
        
        # Performance metrics
        st.markdown("<h3>Performance Metrics</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", "10")
        with col2:
            st.metric("Win Rate", "75%")
        with col3:
            st.metric("Total PnL", "+$108.27")
        with col4:
            st.metric("Return on Investment", "+10.83%")
        
        # PnL chart
        st.markdown("<h3>PnL Over Time</h3>", unsafe_allow_html=True)
        
        # Sample PnL data
        dates = pd.date_range(start='2023-03-12', periods=4, freq='D')
        daily_pnl = [28.93, 56.47, -22.45, 45.32]
        cumulative_pnl = [28.93, 85.40, 62.95, 108.27]
        
        df_pnl = pd.DataFrame({
            'Date': dates,
            'Daily PnL': daily_pnl,
            'Cumulative PnL': cumulative_pnl
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_pnl['Date'], y=df_pnl['Daily PnL'], name='Daily PnL'))
        fig.add_trace(go.Scatter(x=df_pnl['Date'], y=df_pnl['Cumulative PnL'], name='Cumulative PnL', mode='lines+markers'))
        fig.update_layout(
            title='PnL Performance',
            xaxis_title='Date',
            yaxis_title='Profit/Loss (USDT)',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif page == "Settings":
        st.markdown("<h2 class='section-header'>Settings</h2>", unsafe_allow_html=True)
        
        st.markdown("### General Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Enable Email Notifications", value=False)
            st.checkbox("Enable Telegram Notifications", value=False)
            email = st.text_input("Email Address")
        with col2:
            st.checkbox("Auto-restart on Error", value=True)
            st.checkbox("Enable Debug Logging", value=False)
            telegram_id = st.text_input("Telegram Chat ID")
        
        st.markdown("### Risk Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Enable Global Stop Loss", value=True)
            global_stop_loss = st.slider("Global Stop Loss (%)", min_value=1.0, max_value=20.0, value=15.0, step=0.5)
        with col2:
            st.checkbox("Enable Daily Loss Limit", value=True)
            daily_loss_limit = st.slider("Daily Loss Limit (%)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("© 2023 Hummingbot BTC Trading Dashboard | Not Financial Advice | Use At Your Own Risk") 