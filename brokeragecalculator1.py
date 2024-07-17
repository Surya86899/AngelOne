# Original transactions in the format provided
original_transactions = [
    ('Buy', '2022-06-23', '2022-06-24', 2825.0, 176, 500000, 15),
    ('Sell', '2022-10-03', 3613.425, 176, 638762.8, 15),
    ('Buy', '2022-11-01', '2022-11-02', 3607.45, 177, 638762.8, 0),
    ('Sell', '2022-11-28', 3898.2, 177, 690225.55, 0),
    ('Buy', '2022-12-21', '2022-12-22', 3529.5, 195, 690225.55, 13),
    ('Sell (Stop Loss)', '2023-01-12', 3318.0345, 195, 648989.7775000001, 13),
    ('Buy', '2023-01-18', '2023-01-19', 1215.0, 534, 648989.7775000001, 32),
    ('Sell (Stop Loss)', '2023-01-25', 1194.93, 534, 638272.3975000001, 32),
    ('Buy', '2023-02-15', '2023-02-16', 4514.0, 141, 638272.3975000001, 2),
    ('Sell (Stop Loss)', '2023-05-31', 4525.285, 141, 639863.5825, 2),
    ('Buy', '2023-07-04', '2023-07-05', 1634.95, 391, 639863.5825, 7),
    ('Sell (Stop Loss)', '2023-08-02', 1549.4489999999998, 391, 606432.6914999998, 7),
    ('Buy', '2023-09-07', '2023-09-08', 274.75, 2207, 606432.6914999998, 12),
    ('Sell', '2024-01-18', 375.275, 2207, 828291.3664999998, 12),
    ('Buy', '2024-04-25', '2024-04-26', 1133.95, 730, 828291.3664999998, 4),
    ('Sell (Stop Loss)', '2024-06-04', 1136.784875, 730, 830360.8252499998, 4)
]

# Function to transform transactions to desired format
def transform_to_desired_format(transactions):
    transformed_transactions = []
    for transaction in transactions:
        if len(transaction) >= 7:
            transaction_type = transaction[0]
            buy_date = transaction[1] if transaction_type == 'Buy' else transaction[2]
            buy_price = transaction[3]
            quantity = transaction[4]
            capital = transaction[5]
            sl = transaction[6]
            transformed_transactions.append((transaction_type, buy_date, buy_price, quantity, capital, sl))
        else:
            # Handle cases where the tuple does not have the expected number of elements
            transformed_transactions.append(transaction)

    return transformed_transactions

# Transform transactions
original_transactions = transform_to_desired_format(original_transactions)

# for rows in original_transactions:
#     print(rows)



# Define charge rates
stt_rate_buy = 0.001  # 0.1% STT on buy
stt_rate_sell = 0.001  # 0.1% STT on sell
transaction_charge_rate = 0.0000335  # 0.00335%
dp_charge_per_scrip = 20  # DP charges
dp_gst_rate = 0.18  # GST on DP charges
stamp_duty_rate = 0.000076  # 0.015%
sebi_turnover_fee_rate = 0.000001  # 0.0001%
gst_rate = 0.18  # GST on brokerage and transaction charges

# Function to calculate charges for a pair of transactions
def calculate_total_charges(buy_transaction, sell_transaction):
    buy_price, buy_quantity = buy_transaction[2], buy_transaction[3]
    sell_price, sell_quantity = sell_transaction[2], sell_transaction[3]
    
    # Ensure the quantities match for buy and sell transactions
    if buy_quantity != sell_quantity:
        raise ValueError("Buy and Sell quantities do not match.")
    
    buy_value = buy_price * buy_quantity
    sell_value = sell_price * sell_quantity
    
    # STT calculation
    stt = buy_value * stt_rate_buy + sell_value * stt_rate_sell
    
    # Transaction charges
    transaction_charges = (buy_value + sell_value) * transaction_charge_rate
    
    # DP charges on sell side only
    dp_charges = dp_charge_per_scrip
    dp_charges_gst = dp_charges * dp_gst_rate
    
    # Stamp duty
    stamp_duty = buy_value * stamp_duty_rate + sell_value * stamp_duty_rate
    
    # SEBI turnover fees
    sebi_turnover_fees = (buy_value + sell_value) * sebi_turnover_fee_rate
    
    # GST on transaction charges and DP charges
    gst = (transaction_charges + dp_charges + sebi_turnover_fees) * gst_rate
    
    # Total charges
    total_charges = stt + transaction_charges + dp_charges + dp_charges_gst + stamp_duty + sebi_turnover_fees + gst
    
    return {
        'Total STT': stt,
        'Total Transaction Charges': transaction_charges,
        'Total DP Charges': dp_charges,
        'Total DP Charges GST': dp_charges_gst,
        'Total Stamp Duty': stamp_duty,
        'Total SEBI Turnover Fees': sebi_turnover_fees,
        'Total GST': gst,
        'Total Charges': total_charges
    }

# Calculate and print charges for each pair of transactions
total_sum_charges = 0.0

for i in range(0, len(original_transactions), 2):
    buy_transaction = original_transactions[i]
    sell_transaction = original_transactions[i + 1]
    
    try:
        total_charges = calculate_total_charges(buy_transaction, sell_transaction)
        total_sum_charges += total_charges['Total Charges']
        
        print(f"Transaction Pair {i//2 + 1}:")
        print(f"  Total STT: {total_charges['Total STT']:.2f}")
        print(f"  Total Transaction Charges: {total_charges['Total Transaction Charges']:.2f}")
        print(f"  Total DP Charges: {total_charges['Total DP Charges']:.2f}")
        print(f"  Total DP Charges GST: {total_charges['Total DP Charges GST']:.2f}")
        print(f"  Total Stamp Duty: {total_charges['Total Stamp Duty']:.2f}")
        print(f"  Total SEBI Turnover Fees: {total_charges['Total SEBI Turnover Fees']:.2f}")
        print(f"  Total GST: {total_charges['Total GST']:.2f}")
        print(f"  Total Charges: {total_charges['Total Charges']:.2f}")
        print("------------------------------")
    
    except ValueError as e:
        print(f"Error processing Transaction Pair {i//2 + 1}: {e}")
        print("------------------------------")

# Print the summation of Total Charges
print(f"Summation of Total Charges: {total_sum_charges:.2f}")