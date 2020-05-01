import time
from typing import Union

import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from src.data_models import HealthStatusResponse, ModelMetaDataResponse, ModelsMetaDataResponse
from src.model_manager import ModelManager
from src.config import setup_logging
import logging

app = FastAPI()
manager = ModelManager()


@app.on_event("startup")
@repeat_every(seconds=10)  # 1 hour
def reload_model() -> None:
    manager.update()
    logging.info('First model load finished')


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


# @app.get('/model_repository')
# async def model_repository():
#     if os.path.exists('/shared_volume'):
#         return {
#             'shared': 'exists',
#             'path': '/shared_volume'
#         }
#     elif os.path.exists('../examples/retrained_model/shared_volume'):
#         return {
#             'shared': 'exists',
#             'path': 'shared_volume/'
#         }
#     else:
#         return {
#             'shared': 'non-existent'
#         }


@app.get('/servables', response_model=ModelsMetaDataResponse)
async def meta_data():
    result = manager.all_models_meta_data_response()
    logging.info(result)
    return result


@app.get('/servables/{model_name}', response_model=ModelsMetaDataResponse)
async def model_meta_data(model_name: str):
    return manager.model_meta_data_response(model_name)


@app.get('/servables/{model_name}', response_model=Union[ModelsMetaDataResponse, ModelMetaDataResponse])
async def model_version_meta_data(model_name: str):
    return manager.model_meta_data_response(model_name)


@app.get('/servables/{model_name}/{version}', response_model=ModelsMetaDataResponse)
async def available_model(model_name: str, version: str):
    result = manager.model_meta_data_response(model_name, version)
    return result


@app.post('/predict/')
async def predict(input):
    text = input.text
    start_time = time.time()
    result = manager.model_predict(text)
    result.update({'time': time.time() - start_time})

    return result


if __name__ == "__main__":
    setup_logging()
    uvicorn.run("api:app", host="0.0.0.0", port=5000, log_level="info")
