#!/usr/bin/env python3
"""
Simplified Trading Bot for Binance Futures Testnet
Author: [Your Name]
Date: July 2025
"""

import logging
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import argparse


class TradingBotLogger:
    """Enhanced logging system for the trading bot"""
    
    def __init__(self, log_file: str = "trading_bot.log"):
        self.logger = logging.getLogger("TradingBot")
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for detailed logs
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler for user feedback
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_api_request(self, method: str, params: Dict[str, Any]):
        """Log API request details"""
        self.logger.info(f"API REQUEST - Method: {method}, Params: {json.dumps(params, indent=2)}")
    
    def log_api_response(self, method: str, response: Dict[str, Any]):
        """Log API response details"""
        self.logger.info(f"API RESPONSE - Method: {method}, Response: {json.dumps(response, indent=2)}")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log error details"""
        self.logger.error(f"ERROR {context}: {str(error)}")
    
    def log_order_execution(self, order_details: Dict[str, Any]):
        """Log order execution details"""
        self.logger.info(f"ORDER EXECUTED: {json.dumps(order_details, indent=2)}")


class BasicBot:
    """Simplified Trading Bot for Binance Futures Testnet"""
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """Initialize the trading bot with API credentials"""
        self.logger = TradingBotLogger()
        
        try:
            # Initialize Binance client with testnet configuration
            self.client = Client(api_key, api_secret, testnet=testnet)
            if testnet:
                self.client.API_URL = 'https://testnet.binancefuture.com'
                self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
            
            self.logger.logger.info("Trading Bot initialized successfully")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            self.logger.log_error(e, "Bot Initialization")
            raise
    
    def _test_connection(self):
        """Test API connection and permissions"""
        try:
            self.logger.log_api_request("ping", {})
            ping_result = self.client.futures_ping()
            self.logger.log_api_response("ping", ping_result)
            
            # Test account access
            self.logger.log_api_request("account_info", {})
            account_info = self.client.futures_account()
            self.logger.log_api_response("account_info", {"status": "success", "totalWalletBalance": account_info.get('totalWalletBalance', 'N/A')})
            
            self.logger.logger.info("✅ API connection successful")
            
        except BinanceAPIException as e:
            self.logger.log_error(e, "API Connection Test")
            raise
    
    def get_account_balance(self) -> Dict[str, Any]:
        """Get account balance information"""
        try:
            self.logger.log_api_request("futures_account", {})
            account_info = self.client.futures_account()
            
            balance_info = {
                'totalWalletBalance': account_info.get('totalWalletBalance', '0'),
                'availableBalance': account_info.get('availableBalance', '0'),
                'totalUnrealizedProfit': account_info.get('totalUnrealizedProfit', '0')
            }
            
            self.logger.log_api_response("futures_account", balance_info)
            return balance_info
            
        except BinanceAPIException as e:
            self.logger.log_error(e, "Get Account Balance")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information and price"""
        try:
            self.logger.log_api_request("futures_symbol_ticker", {"symbol": symbol})
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            
            self.logger.log_api_request("futures_exchange_info", {})
            exchange_info = self.client.futures_exchange_info()
            
            symbol_info = None
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    symbol_info = s
                    break
            
            if not symbol_info:
                raise ValueError(f"Symbol {symbol} not found")
            
            result = {
                'symbol': symbol,
                'price': ticker['price'],
                'status': symbol_info['status'],
                'baseAsset': symbol_info['baseAsset'],
                'quoteAsset': symbol_info['quoteAsset'],
                'minQty': next((f['minQty'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'), 'N/A'),
                'stepSize': next((f['stepSize'] for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE'), 'N/A')
            }
            
            self.logger.log_api_response("symbol_info", result)
            return result
            
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Get Symbol Info for {symbol}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """Place a market order"""
        try:
            order_params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': Client.FUTURE_ORDER_TYPE_MARKET,
                'quantity': quantity,
                'timestamp': int(time.time() * 1000)
            }
            
            self.logger.log_api_request("futures_create_order", order_params)
            
            order = self.client.futures_create_order(**order_params)
            
            self.logger.log_api_response("futures_create_order", order)
            self.logger.log_order_execution(order)
            
            return order
            
        except BinanceOrderException as e:
            self.logger.log_error(e, f"Market Order {side} {quantity} {symbol}")
            raise
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Market Order {side} {quantity} {symbol}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """Place a limit order"""
        try:
            order_params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': Client.FUTURE_ORDER_TYPE_LIMIT,
                'quantity': quantity,
                'price': price,
                'timeInForce': Client.TIME_IN_FORCE_GTC,
                'timestamp': int(time.time() * 1000)
            }
            
            self.logger.log_api_request("futures_create_order", order_params)
            
            order = self.client.futures_create_order(**order_params)
            
            self.logger.log_api_response("futures_create_order", order)
            self.logger.log_order_execution(order)
            
            return order
            
        except BinanceOrderException as e:
            self.logger.log_error(e, f"Limit Order {side} {quantity} {symbol} @ {price}")
            raise
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Limit Order {side} {quantity} {symbol} @ {price}")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
        """Place a stop-limit order (Bonus feature)"""
        try:
            order_params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': Client.FUTURE_ORDER_TYPE_STOP,
                'quantity': quantity,
                'price': price,
                'stopPrice': stop_price,
                'timeInForce': Client.TIME_IN_FORCE_GTC,
                'timestamp': int(time.time() * 1000)
            }
            
            self.logger.log_api_request("futures_create_order", order_params)
            
            order = self.client.futures_create_order(**order_params)
            
            self.logger.log_api_response("futures_create_order", order)
            self.logger.log_order_execution(order)
            
            return order
            
        except BinanceOrderException as e:
            self.logger.log_error(e, f"Stop-Limit Order {side} {quantity} {symbol} @ {price} (stop: {stop_price})")
            raise
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Stop-Limit Order {side} {quantity} {symbol} @ {price} (stop: {stop_price})")
            raise
    
    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order"""
        try:
            cancel_params = {
                'symbol': symbol,
                'orderId': order_id
            }
            
            self.logger.log_api_request("futures_cancel_order", cancel_params)
            
            result = self.client.futures_cancel_order(**cancel_params)
            
            self.logger.log_api_response("futures_cancel_order", result)
            
            return result
            
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Cancel Order {order_id} for {symbol}")
            raise
    
    def get_open_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """Get all open orders"""
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol
            
            self.logger.log_api_request("futures_get_open_orders", params)
            
            orders = self.client.futures_get_open_orders(**params)
            
            self.logger.log_api_response("futures_get_open_orders", {"count": len(orders)})
            
            return orders
            
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Get Open Orders for {symbol or 'all symbols'}")
            raise
    
    def get_order_status(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        try:
            params = {
                'symbol': symbol,
                'orderId': order_id
            }
            
            self.logger.log_api_request("futures_get_order", params)
            
            order = self.client.futures_get_order(**params)
            
            self.logger.log_api_response("futures_get_order", order)
            
            return order
            
        except BinanceAPIException as e:
            self.logger.log_error(e, f"Get Order Status {order_id} for {symbol}")
            raise


def validate_input(prompt: str, input_type: type, validation_func=None):
    """Validate user input with type checking and optional validation function"""
    while True:
        try:
            user_input = input(prompt)
            
            if input_type == str:
                value = user_input.strip().upper()
            else:
                value = input_type(user_input)
            
            if validation_func and not validation_func(value):
                print("❌ Invalid input. Please try again.")
                continue
            
            return value
            
        except ValueError:
            print(f"❌ Please enter a valid {input_type.__name__}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    parser.add_argument("--api-key", required=True, help="Binance API Key")
    parser.add_argument("--api-secret", required=True, help="Binance API Secret")
    parser.add_argument("--testnet", action="store_true", default=True, help="Use testnet (default: True)")
    
    args = parser.parse_args()
    
    print("🚀 Binance Futures Trading Bot")
    print("=" * 50)
    
    try:
        # Initialize bot
        bot = BasicBot(args.api_key, args.api_secret, args.testnet)
        
        # Display account information
        balance = bot.get_account_balance()
        print(f"💰 Account Balance: {balance['totalWalletBalance']} USDT")
        print(f"💰 Available Balance: {balance['availableBalance']} USDT")
        print(f"📊 Unrealized PnL: {balance['totalUnrealizedProfit']} USDT")
        print()
        
        while True:
            print("\n📋 Available Commands:")
            print("1. Place Market Order")
            print("2. Place Limit Order")
            print("3. Place Stop-Limit Order")
            print("4. View Open Orders")
            print("5. Cancel Order")
            print("6. Check Order Status")
            print("7. Get Symbol Info")
            print("8. View Account Balance")
            print("9. Exit")
            
            choice = validate_input("Select an option (1-9): ", str, lambda x: x in "123456789")
            
            if choice == "1":
                # Market Order
                symbol = validate_input("Enter symbol (e.g., BTCUSDT): ", str)
                side = validate_input("Enter side (BUY/SELL): ", str, lambda x: x in ["BUY", "SELL"])
                quantity = validate_input("Enter quantity: ", float, lambda x: x > 0)
                
                try:
                    order = bot.place_market_order(symbol, side, quantity)
                    print(f"✅ Market order placed successfully!")
                    print(f"Order ID: {order['orderId']}")
                    print(f"Status: {order['status']}")
                except Exception as e:
                    print(f"❌ Error placing market order: {e}")
            
            elif choice == "2":
                # Limit Order
                symbol = validate_input("Enter symbol (e.g., BTCUSDT): ", str)
                side = validate_input("Enter side (BUY/SELL): ", str, lambda x: x in ["BUY", "SELL"])
                quantity = validate_input("Enter quantity: ", float, lambda x: x > 0)
                price = validate_input("Enter price: ", float, lambda x: x > 0)
                
                try:
                    order = bot.place_limit_order(symbol, side, quantity, price)
                    print(f"✅ Limit order placed successfully!")
                    print(f"Order ID: {order['orderId']}")
                    print(f"Status: {order['status']}")
                except Exception as e:
                    print(f"❌ Error placing limit order: {e}")
            
            elif choice == "3":
                # Stop-Limit Order
                symbol = validate_input("Enter symbol (e.g., BTCUSDT): ", str)
                side = validate_input("Enter side (BUY/SELL): ", str, lambda x: x in ["BUY", "SELL"])
                quantity = validate_input("Enter quantity: ", float, lambda x: x > 0)
                price = validate_input("Enter limit price: ", float, lambda x: x > 0)
                stop_price = validate_input("Enter stop price: ", float, lambda x: x > 0)
                
                try:
                    order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                    print(f"✅ Stop-limit order placed successfully!")
                    print(f"Order ID: {order['orderId']}")
                    print(f"Status: {order['status']}")
                except Exception as e:
                    print(f"❌ Error placing stop-limit order: {e}")
            
            elif choice == "4":
                # View Open Orders
                symbol = input("Enter symbol (or press Enter for all): ").strip().upper()
                symbol = symbol if symbol else None
                
                try:
                    orders = bot.get_open_orders(symbol)
                    if orders:
                        print(f"\n📋 Open Orders ({len(orders)}):")
                        for order in orders:
                            print(f"ID: {order['orderId']} | {order['symbol']} | {order['side']} | {order['type']} | Qty: {order['origQty']} | Status: {order['status']}")
                    else:
                        print("📋 No open orders found.")
                except Exception as e:
                    print(f"❌ Error getting open orders: {e}")
            
            elif choice == "5":
                # Cancel Order
                symbol = validate_input("Enter symbol: ", str)
                order_id = validate_input("Enter order ID: ", str)
                
                try:
                    result = bot.cancel_order(symbol, order_id)
                    print(f"✅ Order {order_id} cancelled successfully!")
                    print(f"Status: {result['status']}")
                except Exception as e:
                    print(f"❌ Error cancelling order: {e}")
            
            elif choice == "6":
                # Check Order Status
                symbol = validate_input("Enter symbol: ", str)
                order_id = validate_input("Enter order ID: ", str)
                
                try:
                    order = bot.get_order_status(symbol, order_id)
                    print(f"\n📊 Order Status:")
                    print(f"ID: {order['orderId']}")
                    print(f"Symbol: {order['symbol']}")
                    print(f"Side: {order['side']}")
                    print(f"Type: {order['type']}")
                    print(f"Quantity: {order['origQty']}")
                    print(f"Filled: {order['executedQty']}")
                    print(f"Status: {order['status']}")
                    print(f"Time: {datetime.fromtimestamp(order['time']/1000)}")
                except Exception as e:
                    print(f"❌ Error getting order status: {e}")
            
            elif choice == "7":
                # Get Symbol Info
                symbol = validate_input("Enter symbol: ", str)
                
                try:
                    info = bot.get_symbol_info(symbol)
                    print(f"\n📊 Symbol Information:")
                    print(f"Symbol: {info['symbol']}")
                    print(f"Current Price: {info['price']}")
                    print(f"Status: {info['status']}")
                    print(f"Base Asset: {info['baseAsset']}")
                    print(f"Quote Asset: {info['quoteAsset']}")
                    print(f"Min Quantity: {info['minQty']}")
                    print(f"Step Size: {info['stepSize']}")
                except Exception as e:
                    print(f"❌ Error getting symbol info: {e}")
            
            elif choice == "8":
                # View Account Balance
                try:
                    balance = bot.get_account_balance()
                    print(f"\n💰 Account Information:")
                    print(f"Total Wallet Balance: {balance['totalWalletBalance']} USDT")
                    print(f"Available Balance: {balance['availableBalance']} USDT")
                    print(f"Unrealized PnL: {balance['totalUnrealizedProfit']} USDT")
                except Exception as e:
                    print(f"❌ Error getting account balance: {e}")
            
            elif choice == "9":
                print("👋 Thank you for using the Trading Bot!")
                break
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()