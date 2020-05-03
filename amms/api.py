import time
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from src.data_models import HealthStatusResponse, ModelsMetaDataResponse, \
    ModelNotFoundResponse, LabelScoreResponse
from src.model_manager import ModelManager
from src.config import setup_logging
from src.prediction_router import get_routers


def model_not_found_response():
    return {
        404: {"model": ModelNotFoundResponse, "description": "Model not found."}
    }


app = FastAPI()
manager = ModelManager()


@app.on_event("startup")
def startup():
    logging.info('App is about to start up.')


@repeat_every(seconds=10)  # 1 hour
def reload_models() -> None:
    logging.info('Update models')
    manager.update()


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


@app.get('/meta/', response_model=ModelsMetaDataResponse, responses=model_not_found_response())
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


@app.post('/predict/', response_model=LabelScoreResponse, responses=model_not_found_response())
async def predict(input, model_name: str = None, version: str = None):
    result = manager.predict(model_name=model_name, version=version, input=input)
    logging.debug('PredictionResult {}'.format(result))
    return result


for tags, router in get_routers(manager):
    app.include_router(router, tags=tags)

if __name__ == "__main__":
    setup_logging()
    logging.info('Start App.')
    uvicorn.run("api:app", host="0.0.0.0", port=8090, log_level="debug", reload=True)
