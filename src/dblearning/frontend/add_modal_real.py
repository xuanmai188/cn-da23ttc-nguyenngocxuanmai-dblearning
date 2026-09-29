file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

modal_injection = """
  const handleOnboardingComplete = () => {
    // Reload profile and recommendations
    setLoading(true);
    Promise.all([
      recommendationApi.getProfile(),
      recommendationApi.getRecommendations()
    ]).then(([profData, recData]) => {
      setProfile(profData);
      setRecommendations(recData.recommendations || []);
    }).finally(() => setLoading(false));
  };

  if (loading) {
"""

content = content.replace("  if (loading) {", modal_injection)

modal_render = """
  return (
    <div className="space-y-6 pt-6">
      {profile && profile.is_onboarded === false && (
        <OnboardingModal onComplete={handleOnboardingComplete} />
      )}
"""

content = content.replace("  return (\n    <div className=\"space-y-6 pt-6\">", modal_render)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Dashboard.jsx successfully injected with modal")
