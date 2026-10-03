files = {
    "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx": [
        ("{user?.full_name?.charAt(0) || 'A'}", "{(user?.full_name || '').split(' ').pop().charAt(0).toUpperCase() || 'A'}")
    ],
    "D:/DemoCN2026/dblearning/frontend/src/components/Layout.jsx": [
        ("{user?.full_name?.charAt(0) || 'U'}", "{(user?.full_name || '').split(' ').pop().charAt(0).toUpperCase() || 'U'}")
    ],
    "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx": [
        ("{details?.full_name?.charAt(0)}", "{(details?.full_name || '').split(' ').pop().charAt(0).toUpperCase()}")
    ],
    "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserTable.jsx": [
        ("{u.full_name.charAt(0)}", "{(u.full_name || '').split(' ').pop().charAt(0).toUpperCase()}")
    ],
    "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx": [
        ("{student.full_name.charAt(0)}", "{(student.full_name || '').split(' ').pop().charAt(0).toUpperCase()}")
    ]
}

import os

for filepath, replacements in files.items():
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        modified = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True
                
        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {os.path.basename(filepath)}")
        else:
            print(f"Target not found in {os.path.basename(filepath)}")
    else:
        print(f"File not found: {filepath}")
