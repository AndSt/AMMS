from typing import List, Tuple

from fastapi import APIRouter
from src.model_manager import ModelManager
from src.data_models import ModelNotFoundResponse, LabelScoreResponse
import logging


def model_not_found_response():
    return {
        404: {"model": ModelNotFoundResponse, "description": "Model not found."}
    }


def get_routers(manager: ModelManager):
    model_names = []
    for servable in manager.servables:
        model_names.append(servable.meta_data.model_name)
    model_names = list(set(model_names))

    tag_router_tuples = []
    for model_name in model_names:
        tag_router_tuples.append(get_model_router(manager, model_name))

    return tag_router_tuples


def get_model_router(manager: ModelManager, model_name: str) -> Tuple[List[str], APIRouter]:
    # TODO correctness checks?

    # set up versions
    versions = []
    for servable in manager.servables:
        if servable.meta_data.model_name == model_name:
            versions.append(str(servable.meta_data.version))

    # set router
    router = APIRouter()

    async def predict_newest_version(input):
        result = manager.predict(model_name=model_name, input=input)
        return result

    # only set up route, if model version is unique
    if len(versions) == 1:
        router.post('/predict/{}'.format(model_name), response_model=LabelScoreResponse,
                    responses=model_not_found_response())(predict_newest_version)

    for version in versions:
        async def predict_with_specific_version(input):
            logging.info('predict', model_name, version, input)
            result = manager.predict(model_name=model_name, version=version, input=input)
            return result

        router.post('/predict/{}/{}'.format(model_name, version), response_model=LabelScoreResponse,
                    responses=model_not_found_response())(predict_with_specific_version)

    return [model_name], router
