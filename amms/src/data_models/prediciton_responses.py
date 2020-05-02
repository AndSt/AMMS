from typing import List

from pydantic import BaseModel

from src.data_models.standard import ModelDescription


class LabelScoreExample(BaseModel):
    label: str
    score: float


class PredictionResponse(BaseModel):
    model: ModelDescription
    result: List[List[LabelScoreExample]]

