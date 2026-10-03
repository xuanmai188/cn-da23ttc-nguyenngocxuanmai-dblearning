file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Insert schema imports at the beginning of the appended blocks
fix_items_block = """
# ==========================================
# LESSONS (ITEMS) MANAGEMENT
# ==========================================
from app.schemas.learning import LearningItem as LearningItemSchema, LearningItemCreate, LearningItemUpdate
from app.models.models import LearningItem as LearningItemModel

@router.get("/items", response_model=List[LearningItemSchema])
def get_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    topic_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:"""

content = re.sub(
    r"# ==========================================\n# LESSONS \(ITEMS\) MANAGEMENT\n# ==========================================\n\nfrom app\.models\.models import LearningItem as LearningItemModel\n\n@router\.get\(\"/items\", response_model=List\[LearningItem\]\)\ndef get_items\(",
    fix_items_block.strip(),
    content
)
content = content.replace("@router.post(\"/items\", response_model=LearningItem)", "@router.post(\"/items\", response_model=LearningItemSchema)")
content = content.replace("@router.put(\"/items/{item_id}\", response_model=LearningItem)", "@router.put(\"/items/{item_id}\", response_model=LearningItemSchema)")

fix_quizzes_block = """
# ==========================================
# QUIZ MANAGEMENT
# ==========================================
from app.schemas.quiz import Quiz as QuizSchema, QuizCreate, QuizUpdate
from app.models.models import Quiz as QuizModel

@router.get("/quizzes", response_model=List[QuizSchema])
def get_quizzes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    item_id: Optional[int] = None,
    current_admin: User = Depends(deps.get_current_active_admin)
) -> Any:"""

content = re.sub(
    r"# ==========================================\n# QUIZ MANAGEMENT\n# ==========================================\n\nfrom app\.models\.models import Quiz as QuizModel\n\n@router\.get\(\"/quizzes\", response_model=List\[Quiz\]\)\ndef get_quizzes\(",
    fix_quizzes_block.strip(),
    content
)
content = content.replace("@router.post(\"/quizzes\", response_model=Quiz)", "@router.post(\"/quizzes\", response_model=QuizSchema)")
content = content.replace("@router.put(\"/quizzes/{quiz_id}\", response_model=Quiz)", "@router.put(\"/quizzes/{quiz_id}\", response_model=QuizSchema)")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed schemas imports in admin.py")
