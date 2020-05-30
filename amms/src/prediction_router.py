from typing import List, Tuple, Dict

from fastapi import APIRouter
from src.model_manager import ModelManager
from src.servable_base import Servable
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


def get_predict_router(manager):

    request_types = [servable.model.request_format() for servable in manager.servables]
    request_format = request_types[0] if len(set(request_types)) == 1 else Dict

    async def predict_using_newest_version(input: request_format, model_name: str = None, version: str = None):
        result = manager.predict(model_name=model_name, version=version, input=input)
        return result

    # set up main model_name route to newest servable

    response_types = [servable.model.response_format() for servable in manager.servables]
    response_format = response_types[0] if len(set(response_types)) == 1 else Dict

    router = APIRouter()
    router.post('/predict', response_model=response_format, responses=model_not_found_response())(
        predict_using_newest_version)

    return router


def get_model_router(manager: ModelManager, model_name: str) -> Tuple[List[str], APIRouter]:
    # set up versions
    versions = []
    servables = [servable for servable in manager.servables if servable.meta_data.model_name == model_name]
    newest_servable = Servable.newest_servable(servables)
    for servable in manager.servables:
        if servable.meta_data.model_name == model_name:
            versions.append(str(servable.meta_data.version))

    # set router
    router = APIRouter()

    async def predict_using_newest_version(input: newest_servable.model.request_format()):
        result = manager.predict(model_name=model_name, input=input)
        return result

    # set up main model_name route to newest servable
    router.post('/predict/{}'.format(model_name), response_model=newest_servable.model.response_format(),
                responses=model_not_found_response())(predict_using_newest_version)

    for servable in servables:
        version = servable.meta_data.version

        async def predict_with_specific_version(input: servable.model.request_format()):
            logging.info('predict', model_name, version, input)
            result = manager.predict(model_name=model_name, version=version, input=input)
            return result

        router.post('/predict/{}/{}'.format(model_name, version), response_model=LabelScoreResponse,
                    responses=model_not_found_response())(predict_with_specific_version)

    return [model_name], router
