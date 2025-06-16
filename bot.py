import os
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange
import telegram

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
bot = telegram.Bot(token=bot_token)

tickers = ["AAPL", "TSLA", "NVDA", "AMZN", "MSFT", "META", "GOOGL", "AMD", "NFLX", "BABA"]

messages = []

for ticker in tickers:
    df = yf.download(ticker, period="14d", interval="1d")
    if df.empty or len(df) < 14:
        continue

    df.dropna(inplace=True)
    df["RSI"] = RSIIndicator(close=df["Close"]).rsi()
    df["ATR"] = AverageTrueRange(high=df["High"], low=df["Low"], close=df["Close"]).average_true_range()

    last_rsi = df["RSI"].iloc[-1]
    last_atr = df["ATR"].iloc[-1]
    price = df["Close"].iloc[-1]

    if last_rsi < 30:
        messages.append(f"📈 {ticker}: RSI {last_rsi:.2f}, ATR {last_atr:.2f} — ВОЗМОЖНА ПОКУПКА по ${price:.2f}")
    elif last_rsi > 70:
        messages.append(f"📉 {ticker}: RSI {last_rsi:.2f}, ATR {last_atr:.2f} — ВОЗМОЖНА ПРОДАЖА по ${price:.2f}")

if not messages:
 messages.append("🤖 Сегодня нет сильных торговых сигналов.")

final_message = "🕒 Сигналы на сегодня:"

bot.send_message(chat_id=chat_id, text=final_message)
