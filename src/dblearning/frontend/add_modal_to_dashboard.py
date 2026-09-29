file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import_statement = "import OnboardingModal from '../components/OnboardingModal';"
if import_statement not in content:
    content = content.replace("import { recommendationApi } from '../api/recommendationApi';", "import { recommendationApi } from '../api/recommendationApi';\n" + import_statement)

# find the return (
#   <div className="max-w-5xl mx-auto pt-8 pb-20 space-y-12">
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

  if (loading) return <div className="p-8 text-center text-gray-500">Đang tải dữ liệu...</div>;

  return (
    <div className="max-w-5xl mx-auto pt-8 pb-20 space-y-12">
      {profile && profile.is_onboarded === false && (
        <OnboardingModal onComplete={handleOnboardingComplete} />
      )}
"""
content = content.replace("  if (loading) return <div className=\"p-8 text-center text-gray-500\">Đang tải dữ liệu...</div>;\n\n  return (\n    <div className=\"max-w-5xl mx-auto pt-8 pb-20 space-y-12\">", modal_injection)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Dashboard.jsx updated with modal")
