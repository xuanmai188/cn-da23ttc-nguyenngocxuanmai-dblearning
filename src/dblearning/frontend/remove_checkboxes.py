file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserTable.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove header checkbox
content = content.replace(
"""              <th className="px-4 py-3">
                <input type="checkbox" className="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
              </th>
""", "")

# Remove row checkbox
content = content.replace(
"""                  <td className="px-4 py-3">
                    <input type="checkbox" className="rounded border-slate-300 text-blue-600 focus:ring-blue-500" />
                  </td>
""", "")

# Adjust colSpan from 8 to 7
content = content.replace('colSpan="8"', 'colSpan="7"')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed checkboxes from UserTable.jsx")
