file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re
# The button might look like:
# <button className="w-full ..."> <KeyIcon /> Đặt lại mật khẩu </button>
# Let's find exactly how it's written.
lines = content.split('\n')
start = -1
end = -1
for i, line in enumerate(lines):
    if "Đặt lại mật khẩu" in line:
        # Find where the button starts
        for j in range(i, -1, -1):
            if "<button" in lines[j]:
                start = j
                break
        # Find where it ends
        for j in range(i, len(lines)):
            if "</button>" in lines[j]:
                end = j
                break
        break

if start != -1 and end != -1:
    print("Found button from line", start, "to", end)
    for j in range(start, end+1):
        print(lines[j])
else:
    print("Button not found")
