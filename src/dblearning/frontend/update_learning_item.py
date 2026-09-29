import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/LearningItem.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I want to add a toast message before navigate('/topics/' + item.topic_id).
# Wait, this project doesn't have a toast library explicitly configured in this file. I'll just use a simple JS alert for now or a state to show a overlay.
# Let's check if there is a toast library, or I'll just change the text of the button to "Đã hoàn thành!" and wait 1s.
if "setTimeout(() => {" not in content:
    old_handle = """  const handleFinish = async () => {
    if (session) {
      await learningApi.endSession(session.id);
    }
    navigate('/topics/' + item.topic_id);
  };"""
    new_handle = """  const [isCompleting, setIsCompleting] = useState(false);
  const handleFinish = async () => {
    setIsCompleting(true);
    if (session) {
      await learningApi.endSession(session.id);
    }
    setTimeout(() => {
      navigate('/topics/' + item.topic_id);
    }, 1000);
  };"""
    content = content.replace(old_handle, new_handle)
    
    # Update the button text
    content = content.replace(">Hoàn thành bài học</button>", ">{isCompleting ? 'Đã hoàn thành! ✅' : 'Hoàn thành bài học'}</button>")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("LearningItem.jsx updated")
