from typing import Union, List

from pydantic import BaseModel


class ModelRequest(BaseModel):
    model_name: str
    version: str


class PredictionRequest(BaseModel):
    model: ModelRequest


class TextPredictionRequest(PredictionRequest):
    input: Union[str, List[str]]