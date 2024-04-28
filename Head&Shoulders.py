import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def detect_head_and_shoulders(data):
    # Identify potential peaks and troughs
    peaks, _ = find_peaks(data, prominence=0.1)
    troughs, _ = find_peaks(-data, prominence=0.1)

    # Check if there are at least two peaks and two troughs
    if len(peaks) < 3 or len(troughs) < 2:
        return False

    # Check if the middle peak is the highest
    middle_peak_index = peaks[1]
    if data[middle_peak_index] < max(data[peaks]):
        return False

    # Check if the trough between the left and middle peak is the lowest
    left_trough_index = troughs[troughs < middle_peak_index][-1]
    if data[left_trough_index] < min(data[troughs]):
        return False

    # Check if the trough between the middle and right peak is the lowest
    right_trough_index = troughs[troughs > middle_peak_index][0]
    if data[right_trough_index] < min(data[troughs]):
        return False

    return True

if __name__ == "__main__":
    # Load sample financial data (replace with your own data)
    file_path = "C:/Documents/GitHub/Python/historical files/WIPRO-EQ_ONE_DAY_candle_data.csv"
    data = pd.read_csv(file_path)

    # Extract 'Close' prices
    close_prices = data['Close']

    # Detect head and shoulder pattern
    is_head_and_shoulders = detect_head_and_shoulders(close_prices)

    # Identify potential peaks and troughs
    peaks, _ = find_peaks(close_prices, prominence=0.1)
    troughs, _ = find_peaks(-close_prices, prominence=0.1)

    # Visualize closing prices with potential peaks and troughs
    plt.figure(figsize=(10, 6))
    plt.plot(close_prices, label='Close Prices')
    plt.plot(close_prices.index[peaks], close_prices[peaks], 'bo', label='Peaks')
    plt.plot(close_prices.index[troughs], close_prices[troughs], 'ro', label='Troughs')
    plt.title('Closing Prices with Peaks and Troughs')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    if is_head_and_shoulders:
        print("Head and shoulder pattern detected!")
    else:
        print("No head and shoulder pattern detected.")
