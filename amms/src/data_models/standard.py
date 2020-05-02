from typing import List, Union, Dict
from pydantic import BaseModel
from src.servable_base import ServableStatus


class HealthStatusResponse(BaseModel):
    version: str
    generated_at: str


class ModelDescription(BaseModel):
    model_name: str
    version: str
    train_date: str


class ModelMetaDataResponse(BaseModel):
    status: ServableStatus
    meta_data: ModelDescription
    request_format: Union[str, Dict]
    response_format: Union[str, Dict]


class ModelsMetaDataResponse(BaseModel):
    models: List[ModelMetaDataResponse]


class ModelNotFoundResponse(BaseModel):
    error_message: str
    available_models: List[ModelMetaDataResponse]
