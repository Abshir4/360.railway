import pandas as pd
from geopy.distance import distance
import json

# Read the CSV data into a Pandas DataFrame
data = pd.read_csv("20-09-01-del-2_latlon.csv")

# Initialize variables to store the initial coordinates
initial_lat = data['Latitude'].iloc[0]
initial_lon = data['Longitude'].iloc[0]

# Initialize an empty list to store the frame and movement information
frame_movements = []

# Iterate through the DataFrame to calculate distances and store the data
for index, row in data.iterrows():
    current_lat = row['Latitude']
    current_lon = row['Longitude']

    # Calculate the distance using the distance function from geopy
    coords_1 = (initial_lat, initial_lon)
    coords_2 = (current_lat, current_lon)
    distance_meters = distance(coords_1, coords_2).m

    # Create a dictionary for the current frame and movement
    frame_data = {
        "frame": int(row['frame']),
        "movement": distance_meters
    }

    # Append the frame data to the list
    frame_movements.append(frame_data)

    # Update the initial coordinates for the next iteration
    initial_lat = current_lat
    initial_lon = current_lon

# Save the frame and movement data to a JSON file
with open("frame_movements.json", "w") as json_file:
    json.dump(frame_movements, json_file, indent=4)

print("Data saved to frame_movements.json")
