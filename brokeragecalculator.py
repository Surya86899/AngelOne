# Define the original transactions
original_transactions = [
    ('Buy', '2020-01-02', 1494.65, 26, 40000, 2),
('Sell (DEMA Condition)', '2020-01-28', 1677.75, 26, 44760.6, 2),
('Buy', '2020-01-29', 4419.0, 10, 44760.6, 6),
('Sell (DEMA Condition)', '2020-02-14', 4781.75, 10, 48388.1, 6),
('Buy', '2020-02-19', 1121.08, 43, 48388.1, 93),
('Sell (Updated Stop Loss)', '2020-03-09', 1035.5235, 43, 44709.17050000001, 93),
('Buy', '2020-03-20', 285.8, 156, 44709.17050000001, 98),
('Sell (Updated Stop Loss)', '2020-03-24', 291.516, 156, 45600.86650000001, 98),
('Buy', '2020-03-27', 262.58, 173, 45600.86650000001, 69),
('Sell (Updated Stop Loss)', '2020-04-03', 267.8316, 173, 46509.39330000001, 69),
('Buy', '2020-04-28', 104.1, 446, 46509.39330000001, 53),
('Sell (Updated Stop Loss)', '2020-05-04', 106.182, 446, 47437.96530000001, 53),
('Buy', '2020-05-13', 31.85, 1489, 47437.96530000001, 52),
('Sell (Updated Stop Loss)', '2020-05-15', 32.487, 1489, 48386.45830000001, 52),
('Buy', '2020-05-19', 35.3, 1370, 48386.45830000001, 52),
('Sell (Updated Stop Loss)', '2020-05-21', 36.006, 1370, 49353.67830000002, 52),
('Buy', '2020-05-28', 277.78, 177, 49353.67830000002, 69),
('Sell (DEMA Condition)', '2020-06-12', 327.75, 177, 58198.368300000024, 69),
('Buy', '2020-06-16', 356.48, 163, 58198.368300000024, 69),
('Sell (DEMA Condition)', '2020-06-30', 386.08, 163, 63023.16830000002, 69),
('Buy', '2020-07-03', 572.15, 110, 63023.16830000002, 19),
('Sell (Updated Stop Loss)', '2020-07-09', 583.593, 110, 64281.898300000015, 19),
('Buy', '2020-07-15', 262.75, 244, 64281.898300000015, 49),
('Sell (Updated Stop Loss)', '2020-07-22', 268.005, 244, 65564.11830000002, 49),
('Buy', '2020-07-23', 2397.45, 27, 65564.11830000002, 13),
('Sell (DEMA Condition)', '2020-08-14', 3089.8, 27, 84257.56830000003, 13),
('Buy', '2020-08-18', 213.7, 394, 84257.56830000003, 0),
('Sell (DEMA Condition)', '2020-08-31', 279.55, 394, 110202.46830000005, 0),
('Buy', '2020-09-16', 639.45, 172, 110202.46830000005, 31),
('Sell (Updated Stop Loss)', '2020-09-22', 652.239, 172, 112402.17630000005, 31),
('Buy', '2020-09-24', 1947.65, 57, 112402.17630000005, 2),
('Sell (DEMA Condition)', '2020-10-05', 2126.75, 57, 122610.87630000005, 2),
('Buy', '2020-10-07', 1254.0, 97, 122610.87630000005, 47),
('Sell (Updated Stop Loss)', '2020-10-29', 1164.4365, 97, 113923.21680000005, 47),
('Buy', '2020-10-30', 273.25, 416, 113923.21680000005, 62),
('Sell (DEMA Condition)', '2020-11-11', 304.35, 416, 126860.81680000006, 62),
('Buy', '2020-11-13', 2514.6, 50, 126860.81680000006, 15),
('Sell (Updated Stop Loss)', '2020-11-19', 2564.892, 50, 129375.41680000005, 15),
('Buy', '2020-11-24', 392.25, 329, 129375.41680000005, 1),
('Sell (DEMA Condition)', '2020-12-10', 471.0, 329, 155284.16680000006, 1),
('Buy', '2020-12-11', 96.8, 1604, 155284.16680000006, 35),
('Sell (DEMA Condition)', '2020-12-17', 101.5, 1604, 162822.96680000008, 35),
('Buy', '2020-12-18', 1731.8, 94, 162822.96680000008, 81),
('Sell (DEMA Condition)', '2021-01-06', 1795.4, 94, 168801.3668000001, 81),
('Buy', '2021-01-12', 14649.3, 11, 168801.3668000001, 60),
('Sell (Updated Stop Loss)', '2021-01-14', 14942.286, 11, 172024.21280000012, 60),
('Buy', '2021-01-21', 1131.95, 151, 172024.21280000012, 68),
('Sell (Updated Stop Loss)', '2021-01-29', 1154.5890000000002, 151, 175442.70180000013, 68),
('Buy', '2021-02-02', 1445.4, 121, 175442.70180000013, 50),
('Sell (Updated Stop Loss)', '2021-02-09', 1474.3080000000002, 121, 178940.56980000014, 50),
('Buy', '2021-02-10', 96.4, 1856, 178940.56980000014, 87),
('Sell (Updated Stop Loss)', '2021-02-12', 98.328, 1856, 182518.93780000013, 87),
('Buy', '2021-02-16', 126.87, 1438, 182518.93780000013, 36),
('Sell (Updated Stop Loss)', '2021-02-19', 129.4074, 1438, 186167.71900000013, 36),
('Buy', '2021-02-25', 705.0, 264, 186167.71900000013, 1),
('Sell (Updated Stop Loss)', '2021-03-04', 719.1, 264, 189890.11900000012, 1),
('Buy', '2021-03-09', 971.3, 195, 189890.11900000012, 38),
('Sell (Updated Stop Loss)', '2021-03-12', 910.83, 195, 178098.46900000013, 38),
('Buy', '2021-03-19', 129.49, 1375, 178098.46900000013, 36),
('Sell (Updated Stop Loss)', '2021-03-26', 119.5719, 1375, 164461.08150000012, 36),
('Buy', '2021-04-01', 508.75, 323, 164461.08150000012, 27),
('Sell (DEMA Condition)', '2021-04-16', 619.4, 323, 200201.0315000001, 27),
('Buy', '2021-04-20', 477.95, 418, 200201.0315000001, 71),
('Sell (DEMA Condition)', '2021-04-30', 521.95, 418, 218593.0315000001, 71),
('Buy', '2021-05-04', 95.83, 2281, 218593.0315000001, 66),
('Sell (DEMA Condition)', '2021-05-14', 101.8, 2281, 232210.60150000008, 66),
('Buy', '2021-05-20', 15845.8, 14, 232210.60150000008, 60),
('Sell (Max Holding Period)', '2021-07-12', 15219.8, 14, 223446.60150000008, 60),
('Buy', '2021-07-14', 4214.75, 53, 223446.60150000008, 29),
('Sell (Updated Stop Loss)', '2021-07-16', 4299.045, 53, 227914.2365000001, 29),
('Buy', '2021-07-20', 3159.05, 72, 227914.2365000001, 3),
('Sell (DEMA Condition)', '2021-09-08', 3336.6, 72, 240697.83650000006, 3),
('Buy', '2021-09-14', 104.0, 2314, 240697.83650000006, 66),
('Sell (Updated Stop Loss)', '2021-10-07', 106.08, 2314, 245510.95650000006, 66),
('Buy', '2021-10-13', 935.35, 262, 245510.95650000006, 31),
('Sell (Updated Stop Loss)', '2021-10-29', 866.21, 262, 227396.27650000007, 31),
('Buy', '2021-11-03', 1889.5, 120, 227396.27650000007, 30),
('Sell (DEMA Condition)', '2021-11-15', 1947.05, 120, 234302.27650000007, 30),
('Buy', '2021-11-16', 8050.35, 29, 234302.27650000007, 32),
('Sell (Updated Stop Loss)', '2021-11-26', 7308.998500000001, 29, 212803.08300000007, 32),
('Buy', '2021-12-07', 1537.3, 138, 212803.08300000007, 93),
('Sell', '2021-12-24', 1598.792, 138, 221288.97900000008, 93),
('Buy', '2021-12-31', 475.55, 465, 221288.97900000008, 21),
('Sell (DEMA Condition)', '2022-01-18', 496.0, 465, 230798.22900000008, 21),
('Buy', '2022-02-10', 122.75, 1880, 230798.22900000008, 52),
('Sell (Updated Stop Loss)', '2022-02-14', 125.205, 1880, 235413.62900000007, 52),
('Buy', '2022-03-09', 359.35, 655, 235413.62900000007, 98),
('Sell (Updated Stop Loss)', '2022-03-14', 366.53700000000003, 655, 240121.11400000006, 98),
('Buy', '2022-03-16', 731.08, 328, 240121.11400000006, 69),
('Sell (DEMA Condition)', '2022-04-19', 845.33, 328, 277595.11400000006, 69),
('Buy', '2022-04-26', 681.5, 407, 277595.11400000006, 90),
('Sell (Updated Stop Loss)', '2022-05-04', 633.5070000000001, 407, 258061.96300000008, 90),
('Buy', '2022-05-05', 2221.1, 116, 258061.96300000008, 50),
('Sell (Updated Stop Loss)', '2022-05-10', 2265.522, 116, 263214.91500000004, 50),
('Buy', '2022-05-20', 356.85, 737, 263214.91500000004, 98),
('Sell (Updated Stop Loss)', '2022-05-25', 363.987, 737, 268474.884, 98),
('Buy', '2022-05-26', 1816.2, 147, 268474.884, 76),
('Sell (Updated Stop Loss)', '2022-06-17', 1615.2440000000001, 147, 238934.352, 76),
('Buy', '2022-06-23', 2819.05, 84, 238934.352, 15),
('Sell (DEMA Condition)', '2022-07-14', 2955.1, 84, 250362.552, 15),
('Buy', '2022-07-21', 948.1, 264, 250362.552, 25),
('Sell (DEMA Condition)', '2022-08-04', 1050.2, 264, 277316.952, 25),
('Buy', '2022-08-17', 1684.03, 164, 277316.952, 7),
('Sell', '2022-09-01', 1751.3912, 164, 288364.1888, 7),
('Buy', '2022-09-06', 247.35, 1165, 288364.1888, 92),
('Sell (Updated Stop Loss)', '2022-09-22', 230.084, 1165, 268249.2988, 92),
('Buy', '2022-10-21', 900.4, 297, 268249.2988, 4),
('Sell (Max Holding Period)', '2022-12-13', 944.6, 297, 281376.6988, 4),
('Buy', '2022-12-21', 3518.75, 79, 281376.6988, 13),
('Sell (Updated Stop Loss)', '2023-02-03', 3251.0035000000003, 79, 260224.72530000002, 13),
('Buy', '2023-02-08', 54.3, 4792, 260224.72530000002, 97),
('Sell (Updated Stop Loss)', '2023-02-10', 55.385999999999996, 4792, 265428.8373, 97),
('Buy', '2023-02-15', 4487.9, 59, 265428.8373, 2),
('Sell (Updated Stop Loss)', '2023-02-17', 4577.657999999999, 59, 270724.5593, 2),
('Buy', '2023-03-01', 711.65, 380, 270724.5593, 53),
('Sell (DEMA Condition)', '2023-03-17', 897.75, 380, 341442.5593, 53),
('Buy', '2023-04-06', 841.4, 405, 341442.5593, 62),
('Sell (DEMA Condition)', '2023-05-12', 1005.05, 405, 407720.8093, 62),
('Buy', '2023-05-16', 1686.5, 241, 407720.8093, 104),
('Sell (DEMA Condition)', '2023-06-01', 1809.1, 241, 437267.4093, 104),
('Buy', '2023-06-06', 459.15, 952, 437267.4093, 54),
('Sell (Updated Stop Loss)', '2023-06-23', 426.8, 952, 406470.20930000005, 54),
('Buy', '2023-06-27', 664.95, 611, 406470.20930000005, 19),
('Sell (Max Holding Period)', '2023-08-17', 627.4, 611, 383527.1593, 19),
('Buy', '2023-08-22', 110.8, 3461, 383527.1593, 109),
('Sell (DEMA Condition)', '2023-09-11', 139.85, 3461, 484069.2093, 109),
('Buy', '2023-09-15', 5130.5, 94, 484069.2093, 5),
('Sell (DEMA Condition)', '2023-10-26', 5259.35, 94, 496181.1093, 5),
('Buy', '2023-10-27', 1935.2, 256, 496181.1093, 39),
('Sell (Updated Stop Loss)', '2023-11-07', 1973.904, 256, 506089.3333, 39),
('Buy', '2023-11-08', 1767.2, 286, 506089.3333, 112),
('Sell (DEMA Condition)', '2023-11-22', 1844.95, 286, 528325.8333, 112),
('Buy', '2023-11-24', 677.65, 779, 528325.8333, 79),
('Sell (DEMA Condition)', '2023-12-15', 796.15, 779, 620637.3333, 79),
('Buy', '2023-12-19', 2548.97, 243, 620637.3333, 34),
('Sell (DEMA Condition)', '2024-01-05', 2666.4, 243, 649172.8233000002, 34),
('Buy', '2024-01-11', 4342.2, 149, 649172.8233000002, 20),
('Sell', '2024-01-23', 4515.888, 149, 675052.3353000003, 20),
('Buy', '2024-01-25', 2467.65, 273, 675052.3353000003, 99),
('Sell (Updated Stop Loss)', '2024-01-31', 2517.003, 273, 688525.7043000002, 99),
('Buy', '2024-02-01', 1254.55, 548, 688525.7043000002, 67),
('Sell (Max Holding Period)', '2024-03-26', 1199.05, 548, 658111.7043000002, 67),
('Buy', '2024-03-27', 5475.55, 120, 658111.7043000002, 75),
('Sell (Updated Stop Loss)', '2024-04-03', 5585.061000000001, 120, 671253.0243000003, 75),
('Buy', '2024-04-04', 4645.05, 144, 671253.0243000003, 55),
('Sell (Updated Stop Loss)', '2024-04-12', 4737.951, 144, 684630.7683000002, 55),
('Buy', '2024-04-23', 216.85, 3157, 684630.7683000002, 101),
('Sell (Updated Stop Loss)', '2024-04-25', 221.187, 3157, 698322.6773000003, 101),
('Buy', '2024-04-26', 1278.75, 546, 698322.6773000003, 46),
('Sell (DEMA Condition)', '2024-05-24', 1321.75, 546, 721800.6773000003, 46),
('Buy', '2024-05-31', 755.8, 955, 721800.6773000003, 52),
('Sell (Updated Stop Loss)', '2024-06-04', 770.9159999999999, 955, 736236.4573000002, 52),
('Buy', '2024-06-07', 484.55, 1519, 736236.4573000002, 49),
('Sell (DEMA Condition)', '2024-07-05', 535.1, 1519, 813021.9073000002, 49)
]

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

# Transform transactions
def transform_transactions(transactions):
    transformed = []
    for i in range(0, len(transactions), 2):
        buy_transaction = transactions[i]
        sell_transaction = transactions[i + 1]
        transformed.append((buy_transaction[0], buy_transaction[1], buy_transaction[2], buy_transaction[3]))
        transformed.append((sell_transaction[0], sell_transaction[1], sell_transaction[2], sell_transaction[3]))
    return transformed

# Calculate charges for all pairs of transactions
transformed_transactions = transform_transactions(original_transactions)
total_sum_charges = 0

for i in range(0, len(transformed_transactions), 2):
    total_charges = calculate_total_charges(transformed_transactions[i], transformed_transactions[i+1])
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

# Print the summation of Total Charges
print(f"Summation of Total Charges: {total_sum_charges:.2f}")
