import json
import os

# Automatically get the script's directory and JSON file path
script_dir = os.path.dirname(os.path.abspath(__file__))
jsonpath = os.path.join(script_dir, "sample-data.json")

# Check if the file exists before opening
if not os.path.exists(jsonpath):
    print(f"Error: File not found at {jsonpath}")
    exit(1)

# Load JSON file
with open(jsonpath, "r") as file:
    data = json.load(file)

datatf = []  # Store parsed data

# Extract relevant data
for i in data['imdata']:
    attributes = i['l1PhysIf']['attributes']
    new_list = [
        attributes.get('dn', 'N/A'),
        attributes.get('descr', ''),  # Some descriptions might be empty
        attributes.get('speed', 'inherit'),  # Use "inherit" if speed is missing
        attributes.get('mtu', '9150')  # Use default MTU if missing
    ]
    datatf.append(new_list)

# Print the output in a formatted way
print("Interface Status")
print("=" * 100)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU':<10}")
print("-" * 100)

for i in datatf:
    print(f"{i[0]:<50} {i[1]:<20} {i[2]:<10} {i[3]:<10}")
