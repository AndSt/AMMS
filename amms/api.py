import time
from typing import Union
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from src.data_models.standard import HealthStatusResponse, ModelMetaDataResponse, ModelsMetaDataResponse, ModelNotFoundResponse
from src.model_manager import ModelManager
from src.config import setup_logging


def model_not_found_response():
    return {
        404: {"model": ModelNotFoundResponse, "description": "Model not found."}
    }

app = FastAPI()
manager = ModelManager()


@app.on_event("startup")
def load_models():
    logging.info('Initialize local_servables.')
    manager.init_servables()
    for servable in manager.servables:
        print(servable.meta_data)


@repeat_every(seconds=10)  # 1 hour
def reload_models() -> None:
    manager.update()
    logging.info('Updated models')


@app.get("/health_check", response_model=HealthStatusResponse)
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


@app.get('/local_servables', response_model=ModelsMetaDataResponse)
async def meta_data():
    result = manager.all_models_meta_data_response()
    logging.info(result)
    return result


@app.get('/local_servables/{model_name}', #response_model=Union[ModelsMetaDataResponse, ModelMetaDataResponse],
         responses=model_not_found_response())
async def model_version_meta_data(model_name: str):
    response = manager.model_meta_data_response(model_name)
    if response is False:
        response = {
            'error_message': 'Model is not found',
            'available_models': manager.all_models_meta_data_response()
        }
        return JSONResponse(status_code=404, content=response)
    return response


@app.get('/local_servables/{model_name}/{version}', response_model=ModelsMetaDataResponse,
         responses=model_not_found_response())
async def available_model(model_name: str, version: str):
    response = manager.model_meta_data_response(model_name, version)
    if response is False:
        response = {
            'error_message': 'Model or version is not found',
            'available_models': manager.all_models_meta_data_response()
        }
        return JSONResponse(status_code=404, content=response)
    return response


@app.post('/predict/')
async def predict(input):
    start_time = time.time()
    result = manager.predict(input)
    result.update({'time': time.time() - start_time})
    # TODO logging
    return result


if __name__ == "__main__":
    setup_logging()
    uvicorn.run("api:app", host="0.0.0.0", port=5000, log_level="info")
