import re
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/Layout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Cog6ToothIcon
if "Cog6ToothIcon" not in content:
    content = content.replace(
        "MapIcon } from '@heroicons/react/24/outline'",
        "MapIcon, Cog6ToothIcon } from '@heroicons/react/24/outline'"
    )

# Add navigation entry
if "href: '/settings'" not in content:
    content = re.sub(
        r"({[^}]*href:\s*'/my-path'[^}]*},)",
        r"\1\n  { name: 'Cài đặt', href: '/settings', icon: Cog6ToothIcon },",
        content
    )

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Layout.jsx updated successfully!")
