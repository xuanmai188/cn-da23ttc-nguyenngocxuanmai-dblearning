file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

import re
start = -1
end = -1
for i, line in enumerate(lines):
    if "Đặt lại mật khẩu" in line:
        for j in range(i, -1, -1):
            if "<button" in lines[j]:
                start = j
                break
        for j in range(i, len(lines)):
            if "</button>" in lines[j]:
                end = j
                break
        break

if start != -1 and end != -1:
    del lines[start:end+1]
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Successfully removed button.")
else:
    print("Could not find button bounds.")
