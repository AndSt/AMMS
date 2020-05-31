import os
import logging

import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from src.model_manager import ModelManager
from src.config import setup_logging
from src.routes import model_predict_routers, predict_router, health_status_router, meta_data_router

# Set paths for model manager
dir_path = os.path.dirname(os.path.realpath(__file__))
config_file = '{}/data/config/servables.json'.format(dir_path)
model_dir = '{}/data/models'.format(dir_path)
manager = ModelManager(config_file=config_file, model_dir=model_dir)

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=10)  # 1 hour
def reload_models() -> None:
    print('Update the models')
    logging.info('Update models')
    manager.update()


app.include_router(health_status_router())
app.include_router(meta_data_router(manager))

app.include_router(predict_router(manager))
for tags, router in model_predict_routers(manager):
    app.include_router(router, tags=tags)

if __name__ == "__main__":
    setup_logging()
    logging.info('Start App.')
    uvicorn.run("api:app", host="0.0.0.0", port=5000, log_level="debug", reload=True)
