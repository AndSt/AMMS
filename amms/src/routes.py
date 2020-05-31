import logging
import time
from typing import List, Tuple, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.model_manager import ModelManager
from src.servable_base import Servable
from src.data_models import ModelNotFoundResponse, LabelScoreResponse, HealthStatusResponse, ModelsMetaDataResponse


def model_not_found_response():
    return {
        404: {"model": ModelNotFoundResponse, "description": "Model not found."}
    }


def health_status_router():
    async def health_check():
        logging.info('/Health check')
        try:
            response = {
                'version': '0.0.1',
                'generated_at': str(time.time())
            }
            return response
        except Exception as e:
            # status_code=500 causes the health check to fail
            return {'status': 'error', "message": e}

    router = APIRouter()
    #router.post("/health_check", response_model=HealthStatusResponse)(health_check)
    router.get("/health_check", response_model=HealthStatusResponse)(health_check)

    return router


def meta_data_router(manager: ModelManager):
    async def available_model(model_name: str = None, version: str = None):
        if model_name is None:
            result = manager.all_models_meta_data_response()
            logging.info(result)
            return result
        response = manager.model_meta_data_response(model_name, version)
        if response is False:
            response = {
                'error_message': 'Model or version is not found',
                'available_models': manager.all_models_meta_data_response()
            }
            return JSONResponse(status_code=404, content=response)
        return response

    router = APIRouter()
    #router.post('/meta', response_model=ModelsMetaDataResponse, responses=model_not_found_response())(available_model)
    router.get('/meta', response_model=ModelsMetaDataResponse, responses=model_not_found_response())(available_model)

    return router


def predict_router(manager):
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


def model_predict_routers(manager: ModelManager):
    model_names = [servable.meta_data.model_name for servable in manager.servables]
    model_names = list(set(model_names))

    tag_router_tuples = []
    for model_name in model_names:
        tag_router_tuples.append(model_predict_router(manager, model_name))

    return tag_router_tuples


def model_predict_router(manager: ModelManager, model_name: str) -> Tuple[List[str], APIRouter]:
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
        version = str(servable.aspired_model.aspired_version)

        async def predict_with_specific_version(input: servable.model.request_format()):
            result = manager.predict(model_name=model_name, version=version, input=input)
            return result

        router.post('/predict/{}/{}'.format(model_name, version), response_model=LabelScoreResponse,
                    responses=model_not_found_response())(predict_with_specific_version)

    return [model_name], router
