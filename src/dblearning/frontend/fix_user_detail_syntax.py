file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the last two </div> with one </div>
content = content.replace(
"""      </div>
    </div>
  );
}""",
"""      </div>
  );
}"""
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed syntax error in UserDetailPanel.jsx")
