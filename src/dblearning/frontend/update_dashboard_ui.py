file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Update stat.increase rendering
old_increase = """                  <span className="flex items-center text-sm font-semibold text-green-600 mb-0.5">
                    <ArrowTrendingUpIcon className="w-4 h-4 mr-0.5" />
                    {stat.increase}%
                  </span>"""

new_increase = """                  {stat.increase > 0 && (
                    <span className="flex items-center text-sm font-semibold text-green-600 mb-0.5">
                      <ArrowTrendingUpIcon className="w-4 h-4 mr-0.5" />
                      +{stat.increase} mới
                    </span>
                  )}"""

content = content.replace(old_increase, new_increase)

# Also fix the session increase (which might still be a percentage from backend or absolute)
# Let's verify what session_growth_rate is.
# In admin.py, let's check session_growth_rate.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated AdminDashboard.jsx increase text")
