import csv

compiled_cases = {}  # Declare dictionary to store each date count in
with open('cases.csv') as csv_file:  # Open CSV
    csv_reader = csv.reader(csv_file, delimiter=',')  # Parse CSV file
    line_count = 0  # Initiate a line count
    for row in csv_reader:  # Loop through rows in CSV file
        if line_count != 0:  # If not the header row
            print(row[4])
            if row[0] in compiled_cases:  # If record for date already exists
                compiled_cases[row[0]]["Cases"] += int(row[4])  # Add number of cases to existing record
                compiled_cases[row[0]]["Countries"] += 1  # Increment how many countries cases have been added to record
            else:  # If record for date does not exist
                compiled_cases[row[0]] = {}  # Declare dictionary inside date object
                compiled_cases[row[0]]["Cases"] = int(row[4])  # Set initial number of cases
                compiled_cases[row[0]]["Countries"] = 1  # Set initial number of countries

        else:  # If it is the header row, then skip
            line_count += 1
    print(f'Processed {line_count} lines.')

csv_columns = ['Date', 'Cases', 'NumberOfCountries']  # Set headers
dict_data = []  # Declare array to store formatted dictionaries in
for key in compiled_cases:  # Loop through processed data
    dict_data.append(
        {"Date": key, "Cases": compiled_cases[key]["Cases"],
         "NumberOfCountries": compiled_cases[key]["Countries"]})  # Compile into format that can be written to CSV

csv_file = "processed.csv"  # Set CSV file to write data to
print(dict_data)
try:
    with open(csv_file, 'w', newline='') as file:  # Open CSV file in write mode
        writer = csv.DictWriter(file, fieldnames=csv_columns)  # Declare CSV writer class
        writer.writeheader()  # Write header data
        for data in dict_data:  # Loop through formatted data
            writer.writerow(data)  # Add to CSV file
except IOError:
    print("I/O error")  # Report error if file doesn't exist
