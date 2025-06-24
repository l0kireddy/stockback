# lstm_model.py
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

scaler = MinMaxScaler()

def get_stock_data(symbol):
    data = yf.download(symbol, period='60d', interval='1d')
    return data[['Close']]

def train_and_predict(symbol):
    df = get_stock_data(symbol)
    if df.shape[0] < 30:
        return None  # Not enough data

    data = scaler.fit_transform(df)
    X, y = [], []
    for i in range(10, len(data)):
        X.append(data[i-10:i, 0])
        y.append(data[i, 0])

    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)),
        LSTM(50),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, batch_size=8, verbose=0)

    last_10 = data[-10:]
    last_10 = last_10.reshape((1, 10, 1))
    predicted_scaled = model.predict(last_10)
    predicted = scaler.inverse_transform(predicted_scaled)
    return float(predicted[0][0])
