#!/bin/bash

# Step 1: Extract a random sample of 7,500 rows
zcat arcos_all_washpost.tsv.gz | shuf -n 7500 > sample.tsv

# Step 2: Extract the TRANSACTION_DATE column (assuming it's column 30)
cut -f30 sample.tsv > dates.txt

# Step 3: Filter out rows with invalid or empty dates, and extract the year (YYYY)
awk '{if ($0 != "" && length($0) == 10) print substr($0, length($0)-3, 4)}' dates.txt > years.txt

# Step 4: Count the rows for each year
echo "Year Count (Sample)"
sort years.txt | uniq -c

# Step 5: Estimate the total rows for each year
total_rows=178598026
sample_size=7500

# Bash integer math (Git Bash doesn't support bc)
scaling_factor=$(( total_rows / sample_size ))

echo -e "\nEstimated Total Rows for Each Year:"
sort years.txt | uniq -c | awk -v scale="$scaling_factor" '{print $2, $1 * scale}'
