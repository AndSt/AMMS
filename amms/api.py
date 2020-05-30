import os
import time
import logging
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from src.data_models import HealthStatusResponse, ModelsMetaDataResponse, ModelNotFoundResponse
from src.model_manager import ModelManager
from src.config import setup_logging
from src.prediction_router import get_routers, get_predict_router


def model_not_found_response():
    return {
        404: {"model": ModelNotFoundResponse, "description": "Model not found."}
    }


app = FastAPI()

# Set paths for model manager
dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = '{}/data/config/servables.json'.format(dir_path)
model_dir = '{}/data/models'.format(dir_path)
manager = ModelManager(config_file=config_file, model_dir=model_dir)
num = 0


@app.on_event("startup")
@repeat_every(seconds=10)  # 1 hour
def reload_models() -> None:
    print('Update the models')
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


@app.get('/meta', response_model=ModelsMetaDataResponse, responses=model_not_found_response())
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


# # TODO check whether input type can be set, if only one input type is available
# @app.post('/predict', responses=model_not_found_response())
# async def predict(input: Dict, model_name: str = None, version: str = None):
#     result = manager.predict(model_name=model_name, version=version, input=input)
#     logging.debug('PredictionResult {}'.format(result))
#     return result

app.include_router(get_predict_router(manager))

for tags, router in get_routers(manager):
    app.include_router(router, tags=tags)

# for route in app.routes:
#     print(route.matches('/health_status'))
#
# app.add_route()

if __name__ == "__main__":
    setup_logging()
    logging.info('Start App.')
    uvicorn.run("api:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
