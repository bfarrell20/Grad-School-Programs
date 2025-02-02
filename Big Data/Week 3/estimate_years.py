import gzip
import random
from datetime import datetime

def estimate_years(file_path, sample_size=7500, total_rows=178598026):
    # Step 1: Read the file and extract a random sample
    with gzip.open(file_path, 'rt') as f:
        header = f.readline()  # Read the header row
        print("Header:", header.strip())  # Debug: Print the header
        columns = header.strip().split('\t')
        transaction_date_index = columns.index('TRANSACTION_DATE')  # Find the column index
        print(f"TRANSACTION_DATE column index: {transaction_date_index}")  # Debug: Print the column index
        
        # Extract a random sample of rows
        sample = []
        for i, line in enumerate(f):
            if random.random() < sample_size / total_rows:
                fields = line.strip().split('\t')
                if len(fields) > transaction_date_index:  # Ensure the column exists
                    date_str = fields[transaction_date_index]  # Extract the date
                    # print(f"Processing row {i + 1}: Date = {date_str}")  # Debug: Print the date being processed
                    try:
                        # Parse the date in "Month/Day/Year" format and extract the year
                        date = datetime.strptime(date_str, '%m%d%Y')  # Adjust the format to match the data
                        year = date.year
                        sample.append(year)
                    except ValueError:
                        # Skip invalid dates
                        print(f"Skipping invalid date: {date_str}")  # Debug: Print invalid dates
                        continue
                else:
                    print(f"Skipping row {i + 1}: Missing TRANSACTION_DATE")  # Debug: Print rows with missing dates
                if len(sample) >= sample_size:
                    break

    # Step 2: Count the occurrences of each year in the sample
    year_counts = {}
    for year in sample:
        year_counts[year] = year_counts.get(year, 0) + 1

    # Step 3: Estimate the total rows for each year
    scaling_factor = total_rows / sample_size
    estimated_counts = {year: count * scaling_factor for year, count in year_counts.items()}

    # Step 4: Print the results
    print("\nYear\tEstimated Rows")
    for year, count in sorted(estimated_counts.items()):
        print(f"{year}\t{count:.0f}")

if __name__ == "__main__":
    file_path = 'arcos_all_washpost.tsv.gz'  # Path to the dataset
    estimate_years(file_path)