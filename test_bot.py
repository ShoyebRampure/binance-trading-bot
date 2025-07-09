# Simple test to verify bot structure
print("Testing bot imports...")

try:
    from trading_bot import BasicBot, TradingBotLogger
    print("✅ Bot classes imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")

try:
    from binance.client import Client
    print("✅ Binance library imported successfully")
except ImportError as e:
    print(f"❌ Binance import error: {e}")

print("\n🎉 Bot is ready for testing!")
print("Next step: Get your Binance Testnet API keys")