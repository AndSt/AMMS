import os
import time
from typing import Optional

from fastapi import FastAPI, Path
from fastapi_utils.tasks import repeat_every

from src.data_models import HealthStatusResponse, ModelStatusResponse, AllModelsStatusResponse, PredictionRequest, \
    PredictionResponse
from src.model_manager import ModelManager
from src.loader import Loader
import logging

app = FastAPI()
loader = Loader()
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


@app.get('/model_repository')
async def model_repository():
    if os.path.exists('/shared_volume'):
        return {
            'shared': 'exists',
            'path': '/shared_volume'
        }
    elif os.path.exists('../shared_volume'):
        return {
            'shared': 'exists',
            'path': 'shared_volume/'
        }
    else:
        return {
            'shared': 'non-existent'
        }


@app.get('/models', response_model=AllModelsStatusResponse)
async def available_models(model_name: str = None):
    result = manager.loaded_versions()
    logging.info(result)
    return result


@app.get('/models/{model_name}/{version}', response_model=ModelStatusResponse)
async def available_model(model_name: str = '',
                          version: Optional[str] = Path('', title='Ask info about the specific version', )):
    result = manager.version_details(model_name, version)
    return result


@app.post('/predict/', response_model=PredictionResponse)
async def text_predict(input: PredictionRequest):
    text = input.text
    print(text)
    start_time = time.time()
    result = manager.model_predict(text)
    result.update({'time': time.time() - start_time})

    return result
