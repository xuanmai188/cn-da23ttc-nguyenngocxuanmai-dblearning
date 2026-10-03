file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserStatsCards.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_increase = """              {card.increase !== null && (
                <span className={`flex items-center text-sm font-semibold mb-0.5 ${card.increase >= 0 ? 'text-green-600' : 'text-red-500'}`}>
                  {card.increase >= 0 ? <ArrowTrendingUpIcon className="w-4 h-4 mr-0.5" /> : <ArrowTrendingDownIcon className="w-4 h-4 mr-0.5" />}
                  {Math.abs(card.increase)}%
                </span>
              )}"""

new_increase = """              {card.increase !== null && card.increase > 0 && (
                <span className={`flex items-center text-sm font-semibold mb-0.5 text-green-600`}>
                  <ArrowTrendingUpIcon className="w-4 h-4 mr-0.5" />
                  +{card.increase} mới
                </span>
              )}"""

content = content.replace(old_increase, new_increase)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserStatsCards.jsx increase rendering")
