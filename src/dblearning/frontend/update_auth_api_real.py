file_path = "D:/DemoCN2026/dblearning/frontend/src/api/authApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "updateProfile" not in content:
    content = content.replace(
        "getMe: () => {\n    return axiosClient.get('/auth/me');\n  },",
        "getMe: () => {\n    return axiosClient.get('/auth/me');\n  },\n\n  updateProfile: (data) => {\n    return axiosClient.put('/auth/me', data);\n  },"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("authApi.js updated correctly")
