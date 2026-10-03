import os
for root, dirs, files in os.walk("D:/DemoCN2026/dblearning/frontend/src"):
    for file in files:
        if file == "Settings.jsx":
            print(os.path.join(root, file))
