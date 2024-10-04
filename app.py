from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)
CORS(app)

@app.route('/stock-data', methods=['GET'])
def get_stock_data():
    symbol = request.args.get('symbol')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    if not start_date:
        # Default to 3 months ago if start date is not provided
        start_date = (datetime.now(pytz.UTC) - timedelta(days=90)).strftime('%Y-%m-%d')

    if not end_date:
        end_date = datetime.now(pytz.UTC).strftime('%Y-%m-%d')

    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            return jsonify({"error": f"No data available for {symbol}"}), 404

        data = []
        for date, row in hist.iterrows():
            data.append({
                "date": date.strftime('%Y-%m-%d'),
                "close": row['Close']
            })

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
