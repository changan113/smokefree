from pydantic import BaseModel
from typing import Optional

class SurveyIn(BaseModel):
    age: int
    exposure_years: float
    hours_per_day: float
    main_environment: str  # "family"|"work"|"social"
    environment_enclosed: bool
    living_with_smoker: Optional[bool] = False
    extra_notes: Optional[str] = None

class ReportOut(BaseModel):
    overall_score: float
    overall_level: str
    scene_scores: dict
    ai_report: str

class CommentIn(BaseModel):
    nick: str
    content: str

class CommentOut(CommentIn):
    id: int
    created_at: str
