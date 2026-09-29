# Touch the file to force Vite HMR to pick it up
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/LearningItem.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add a harmless comment to force file change detection
if "// v2-fixed" in content:
    content = content.replace("// v2-fixed", "// v3-fixed")
else:
    content = content.replace("export default function LearningItem() {", "// v2-fixed\nexport default function LearningItem() {")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

import os, time
# Also touch the file timestamp
os.utime(file_path, None)
print("File touched - Vite should pick up changes")
