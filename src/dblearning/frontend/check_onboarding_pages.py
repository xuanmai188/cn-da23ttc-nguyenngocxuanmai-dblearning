import os

directory = "D:/DemoCN2026/dblearning/frontend/src/pages/admin"
for filename in os.listdir(directory):
    if "Onboarding" in filename:
        print(filename)
