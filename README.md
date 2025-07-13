# Binance Futures Trading Bot

A simplified trading bot for Binance Futures Testnet built with Python. This bot supports market orders, limit orders, and stop-limit orders with comprehensive logging and error handling.

## Features

### Core Features
- ✅ Market Orders (Buy/Sell)
- ✅ Limit Orders (Buy/Sell)
- ✅ Stop-Limit Orders (Bonus feature)
- ✅ Command-line interface with input validation
- ✅ Comprehensive logging system
- ✅ Error handling and API exception management
- ✅ Account balance monitoring
- ✅ Order status tracking and cancellation
- ✅ Symbol information retrieval

### Technical Implementation
- 🔧 Structured code with clear separation of concerns
- 📝 Detailed API request/response logging
- 🛡️ Input validation and error handling
- 🔄 Reusable components and methods
- 📊 Real-time order tracking and status updates

## Prerequisites

### 1. Binance Testnet Account
1. Go to [Binance Testnet](https://testnet.binancefuture.com/)
2. Register for a new account
3. Navigate to API Management
4. Create new API keys
5. Enable Futures Trading permissions

### 2. Python Environment
- Python 3.7 or higher
- pip package manager

## Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd binance-trading-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup API Credentials
You'll need your Binance Testnet API credentials:
- API Key
- API Secret

## Usage

### Command Line Interface
```bash
python trading_bot.py --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET --testnet
```

### Interactive Menu
The bot provides an interactive menu with the following options:

1. **Place Market Order** - Execute immediate buy/sell orders at current market price
2. **Place Limit Order** - Set buy/sell orders at specific price levels
3. **Place Stop-Limit Order** - Advanced order type with stop price trigger
4. **View Open Orders** - Display all active orders
5. **Cancel Order** - Cancel existing orders by ID
6. **Check Order Status** - Get detailed order information
7. **Get Symbol Info** - Display trading pair information and current price
8. **View Account Balance** - Show account balance and unrealized PnL
9. **Exit** - Close the application

### Example Usage Flow

```bash
# Start the bot
python trading_bot.py --api-key YOUR_KEY --api-secret YOUR_SECRET --testnet

# Example interaction:
💰 Account Balance: 10000.0 USDT
💰 Available Balance: 10000.0 USDT
📊 Unrealized PnL: 0.0 USDT

📋 Available Commands:
1. Place Market Order
2. Place Limit Order
...

Select an option (1-9): 1
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter quantity: 0.001

✅ Market order placed successfully!
Order ID: 12345678
Status: FILLED
```

## Logging

The bot generates comprehensive logs in `trading_bot.log`:

- ✅ All API requests and responses
- ✅ Order executions and status changes
- ✅ Error messages and exceptions
- ✅ Account balance updates
- ✅ System events and user interactions

### Log Format
```
2025-07-09 10:30:45,123 - TradingBot - INFO - API REQUEST - Method: futures_create_order, Params: {
  "symbol": "BTCUSDT",
  "side": "BUY",
  "type": "MARKET",
  "quantity": 0.001
}
```

## Code Structure

### Main Components

1. **BasicBot Class** - Core trading functionality
   - API client initialization
   - Order placement methods
   - Account management
   - Error handling

2. **TradingBotLogger Class** - Logging system
   - File and console logging
   - API request/response logging
   - Error tracking

3. **Main CLI Interface** - User interaction
   - Menu system
   - Input validation
   - Command processing

### Key Methods

- `place_market_order()` - Execute market orders
- `place_limit_order()` - Place limit orders
- `place_stop_limit_order()` - Advanced stop-limit orders
- `get_account_balance()` - Retrieve account information
- `get_open_orders()` - List active orders
- `cancel_order()` - Cancel specific orders
- `get_order_status()` - Order status tracking

## Error Handling

The bot includes comprehensive error handling for:

- ✅ API connection failures
- ✅ Invalid order parameters
- ✅ Insufficient balance
- ✅ Network timeouts
- ✅ Invalid symbol or trading pair
- ✅ Order execution failures

## Testing

### Testnet Configuration
The bot is configured to use Binance Futures Testnet:
- Base URL: `https://testnet.binancefuture.com`
- Testnet mode: Enabled by default
- Virtual funds: No real money involved

### Test Scenarios
1. **Account Connection** - Verify API credentials
2. **Market Orders** - Test immediate execution
3. **Limit Orders** - Test order placement and cancellation
4. **Stop-Limit Orders** - Test advanced order types
5. **Error Handling** - Test invalid inputs and API errors

## Security Notes

- 🔐 API credentials are passed via command line arguments
- 🔐 All requests use HTTPS encryption
- 🔐 Testnet environment ensures no real funds are at risk
- 🔐 API keys should never be hardcoded in source code

## File Structure

```
binance-trading-bot/
├── trading_bot.py          # Main bot implementation
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── trading_bot.log        # Generated log file
└── .gitignore            # Git ignore file
```

## Requirements Met

### Core Requirements ✅
- [x] Python implementation
- [x] Binance Futures Testnet integration
- [x] Market and limit order support
- [x] Buy/sell order sides
- [x] Official Binance API usage
- [x] Command-line interface
- [x] Input validation
- [x] Order execution status output
- [x] Comprehensive logging
- [x] Error handling

### Bonus Features ✅
- [x] Stop-Limit order type
- [x] Enhanced CLI interface
- [x] Advanced logging system
- [x] Account balance monitoring
- [x] Order management features

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify API credentials
   - Check network connectivity
   - Ensure testnet URL is accessible

2. **Order Placement Failures**
   - Check symbol validity
   - Verify sufficient balance
   - Validate order parameters

3. **Permission Errors**
   - Ensure API key has futures trading permissions
   - Check API restrictions

## Future Enhancements

Potential improvements for production use:
- WebSocket integration for real-time data
- Database integration for order history
- Advanced order types (OCO, TWAP, Grid)
- Risk management features
- Portfolio tracking
- Automated trading strategies

## 📬 Contact

For questions or issues, please contact:

- **Email**: shoyebrampure@gmail.com  
- **GitHub**: [ShoyebRampure](https://github.com/ShoyebRampure)


## License

This project is created for educational and demonstration purposes.
