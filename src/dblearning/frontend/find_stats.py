import sys
import os

directory = "D:/DemoCN2026/dblearning/frontend/src/pages/admin"
if os.path.exists(directory):
    for filename in os.listdir(directory):
        if "Stat" in filename or "stat" in filename:
            print(f"Found: {filename}")
