file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/OnboardingStats.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("const [loading, setLoading] = useState(true);", "const [loading, setLoading] = useState(true);\n  const [totalCompleted, setTotalCompleted] = useState(0);")

content = content.replace("""const data = await adminApi.getSurveys();
      setSurveys(data);""", """const [surveyData, statsData] = await Promise.all([
        adminApi.getSurveys(),
        adminApi.getSurveyStats()
      ]);
      setSurveys(surveyData);
      setTotalCompleted(statsData.total_completed || 0);""")

content = content.replace("<p className=\"text-2xl font-bold text-slate-900\">0</p>", "<p className=\"text-2xl font-bold text-slate-900\">{totalCompleted}</p>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated OnboardingStats.jsx with dynamic total completed count")
