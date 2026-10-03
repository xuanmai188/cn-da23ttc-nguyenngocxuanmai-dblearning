file_path = "D:/DemoCN2026/dblearning/frontend/src/index.css"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "::-ms-reveal" not in content:
    css_to_add = """
/* Hide native password reveal icon in Edge */
input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
  display: none;
}
"""
    content += css_to_add
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added CSS to hide native eye icon")
else:
    print("CSS already exists")
