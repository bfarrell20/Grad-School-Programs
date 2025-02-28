import pandas as pd
import numpy as np

# Load the data for June and July 2024 (assuming CSV format)
june_data = pd.read_csv("june_2024_flight_data.csv")
july_data = pd.read_csv("july_2024_flight_data.csv")

# Combine the datasets
data = pd.concat([june_data, july_data], ignore_index=True)

# Drop undocumented columns (assuming they are in positions B to C)
data.drop(data.columns[1:5], axis=1, inplace=True)

# Rename columns for clarity (assuming original schema names)
data.columns = ["Airline", "FlightDate", "Origin", "Destination", "DepartureTime", "ArrivalTime", "DelayMinutes"]

# Map airline codes to full names
airline_names = {
    "DL": "Delta Airlines",
    "AA": "American Airlines",
    "UA": "United Airlines",
    "WN": "Southwest Airlines",
    "AS": "Alaska Airlines",
    "B6": "JetBlue Airways"
}
data["Airline"] = data["Airline"].map(airline_names)

# 1. Find the airline with the least average delays
least_delayed_airline = data.groupby("Airline")["DelayMinutes"].mean().idxmin()

# 2. Determine best departure time of day to avoid delays
def get_time_block(hour):
    if 22 <= hour or hour < 6:
        return "Night"
    elif 6 <= hour < 10:
        return "Morning"
    elif 10 <= hour < 14:
        return "Mid-day"
    elif 14 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"

data["DepartureHour"] = pd.to_datetime(data["DepartureTime"]).dt.hour
data["TimeBlock"] = data["DepartureHour"].apply(get_time_block)
best_time_block = data.groupby("TimeBlock")["DelayMinutes"].mean().idxmin()

# 3. Find the airports with the most delays
most_delayed_airports = data.groupby("Origin")["DelayMinutes"].sum().nlargest(5)

# Map airport codes to full names
airport_names = {
    "EWR": "Newark Liberty International",
    "LAX": "Los Angeles International",
    "ORD": "Chicago O'Hare International",
    "ATL": "Hartsfield-Jackson Atlanta International",
    "DFW": "Dallas/Fort Worth International"
}
most_delayed_airports.index = most_delayed_airports.index.map(airport_names)

# 4. Find the busiest airports by flight count
busiest_airports = data["Origin"].value_counts().nlargest(5)
busiest_airports.index = busiest_airports.index.map(airport_names)

# Print results
print("Airline with the least delays:", least_delayed_airline)
print("Best departure time block to avoid delays:", best_time_block)
print("Airports with the most delays:")
print(most_delayed_airports)
print("Top 5 busiest airports:")
print(busiest_airports)
