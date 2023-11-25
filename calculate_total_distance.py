import pandas as pd
from geopy.distance import great_circle
import json

data = pd.read_csv("20-09-01-del-2_latlon.csv")

# Initialize variables to store the initial coordinates
initial_lat = data['Latitude'].iloc[0]
initial_lon = data['Longitude'].iloc[0]

# Initialize an empty list to store the frame and movement information
frame_movements = []

# Initialize a variable to track the total distance
total_distance = 0

# Iterate through the DataFrame to calculate distances and store the data
for index, row in data.iterrows():
    current_lat = row['Latitude']
    current_lon = row['Longitude']
    
    # Calculate the distance using the Haversine formula
    distance = great_circle((initial_lat, initial_lon), (current_lat, current_lon)).meters
    
    # Create a dictionary for the current frame and movement
    frame_data = {
        "frame": int(row['frame']),
        "movement": distance
    }
    
    # Append the frame data to the list
    frame_movements.append(frame_data)
    
    # Update the total distance
    total_distance += distance
    
    # Update the initial coordinates for the next iteration
    initial_lat = current_lat
    initial_lon = current_lon

# Save the frame and movement data to a JSON file
with open("frame_movements.json", "w") as json_file:
    json.dump(frame_movements, json_file, indent=4)

# Create a dictionary for the total distance
total_distance_data = {
    "total_distance_meters": total_distance,
    "total_distance_kilometers": total_distance / 1000  # Convert to kilometers
}

# Save the total distance data to a separate JSON file
with open("total_distance.json", "w") as total_distance_file:
    json.dump(total_distance_data, total_distance_file, indent=4)

print("Data saved to frame_movements.json and total_distance.json")
