import os

folder = "data/raw"

print("Checking CSV files...\n")

for file in os.listdir(folder):
    print(file)