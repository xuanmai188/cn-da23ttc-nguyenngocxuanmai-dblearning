file_path = "D:/DemoCN2026/dblearning/backend/app/schemas/admin.py"
with open(file_path, "a", encoding="utf-8") as f:
    f.write("\n")
    f.write("""class ChartDataPoint(BaseModel):
    date: str
    count: int

class TopicAdminResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    item_count: int
    is_active: bool

    class Config:
        from_attributes = True

class TopicCreateUpdate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    is_active: bool = True
""")
print("Added schemas to admin.py")
