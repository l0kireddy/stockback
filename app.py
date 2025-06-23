from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import requests

app = Flask(__name__)
CORS(app)

@app.route("/api/stock/<symbol>")
def get_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return jsonify({"price": f"{price:.2f}"})
    except Exception as e:
        return jsonify({"error": "Invalid symbol or data not available"}), 400

@app.route("/api/stock/<symbol>/history")
def get_stock_history(symbol):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="7d")
        data = {
            "dates": hist.index.strftime('%Y-%m-%d').tolist(),
            "prices": hist["Close"].round(2).tolist()
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Could not fetch history"}), 400
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use PORT from environment if available
    app.run(host="0.0.0.0", port=port)
