from typing import List, Union
from pydantic import BaseModel
from src.servable_base import ServableStatus


class HealthStatusResponse(BaseModel):
    version: str
    generated_at: str


class ModelRequest(BaseModel):
    model_name: str
    version: str


class ModelDescription(BaseModel):
    model_name: str
    version: str
    train_date: str


class ModelMetaDataResponse(BaseModel):
    status: ServableStatus
    meta_data: ModelDescription


class ModelsMetaDataResponse(BaseModel):
    models: List[ModelMetaDataResponse]


class ServableRequest(BaseModel):
    model: ModelRequest
    # TODO input has to be specified


class TextPredictionRequest(ServableRequest):
    input: Union[str, List[str]]


class LabelScoreExample(BaseModel):
    label: str
    score: float


class ServableResponse(BaseModel):
    model: ModelDescription
    result: List[List[LabelScoreExample]]


class PredictionErrorResponse(BaseModel):
    model: ModelMetaDataResponse
    error: str


class NonExistingModel(BaseModel):
    model_request: ModelRequest
    available_models = ModelsMetaDataResponse
