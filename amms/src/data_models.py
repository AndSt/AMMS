from typing import List
from pydantic import BaseModel


class HealthStatusResponse(BaseModel):
    version: str
    generated_at: str


class Input(BaseModel):
    text: str


class TextInput(BaseModel):
    text: str


class ModelStatusResponse(BaseModel):
    model_name: str
    version: str
    train_date: str


class AllModelsStatusResponse(BaseModel):
    available_models: List[ModelStatusResponse]


class PredictionRequest(BaseModel):
    examples: List[Input]


class LabelScoreExample(BaseModel):
    label: str
    score: float


class PredictionResponse(BaseModel):
    model: ModelStatusResponse
    result: List[List[LabelScoreExample]]
