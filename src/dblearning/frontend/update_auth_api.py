file_path = "D:/DemoCN2026/dblearning/frontend/src/api/authApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "updateProfile:" not in content:
    content = content.replace(
        "getCurrentUser: () => axiosClient.get('/auth/me'),",
        "getCurrentUser: () => axiosClient.get('/auth/me'),\n  updateProfile: (data) => axiosClient.put('/auth/me', data),"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("authApi.js updated")
