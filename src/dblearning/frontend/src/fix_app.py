with open('D:/DemoCN2026/dblearning/frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('/>
        <Route', '/>\n        <Route')

with open('D:/DemoCN2026/dblearning/frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
