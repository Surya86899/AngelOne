import csv

company_names = 'niftymidcap50.csv'
i=100
with open(company_names, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        for company in row:
            # if company == 'LTF':
                # continue
            print(f'r"C:\Documents\GitHub\AngelOne\historical files\ONE_DAY\{company}-EQ_ONE_DAY_candle_data.csv",  #{i}')
            i = i + 1