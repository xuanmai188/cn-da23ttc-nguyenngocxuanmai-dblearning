file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Settings.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "import { AuthContext } from '../context/AuthContext';",
    "import { useAuth } from '../context/AuthContext';"
)

content = content.replace(
    "const { user } = useContext(AuthContext);",
    "const { user } = useAuth();"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Settings.jsx fixed")
