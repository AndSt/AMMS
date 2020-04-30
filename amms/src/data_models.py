from typing import List
from pydantic import BaseModel


class HealthStatusResponse(BaseModel):
    version: str
    generated_at: str


class ModelRequest(BaseModel):
    model_name: str
    version: str


class ModelResponse(BaseModel):
    model_name: str
    version: str
    train_date: str


class AllModelsStatusResponse(BaseModel):
    available_models: List[ModelResponse]
