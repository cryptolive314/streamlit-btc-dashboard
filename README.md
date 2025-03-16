# Hummingbot BTC Trading Dashboard

A Streamlit-based dashboard for monitoring and managing Bitcoin trading strategies using Hummingbot.

## Features

- **Real-time Trading Dashboard**: Monitor your BTC positions, account balance, and PnL metrics
- **Strategy Configuration**: Create and customize Bollinger Bands trading strategies
- **API Integration**: Connect to KuCoin and other exchanges via API
- **Trading History**: View and analyze your past trades with performance metrics
- **Risk Management**: Configure stop-loss, take-profit, and other risk parameters

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Plotly
- Requests

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/btc-trading-dashboard.git
cd btc-trading-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Usage

1. Start the Streamlit app using the command above
2. Access the dashboard at http://localhost:8501
3. Log in with the default credentials (admin/admin)
4. Configure your exchange API credentials
5. Create and deploy your trading strategy

## Configuration

The app includes several configurable parameters:

- Trading pair (default: BTC-USDT)
- Leverage (up to 20x)
- Position mode (HEDGE or ONE-WAY)
- Bollinger Bands parameters (length, standard deviation)
- Risk management settings (stop-loss, take-profit)

## Deployment

This app can be deployed to Streamlit Community Cloud:

1. Push the code to GitHub
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/)
3. Deploy the app from your GitHub repository

## Disclaimer

This dashboard is for educational and informational purposes only. Trading cryptocurrencies involves risk. Use at your own risk. 