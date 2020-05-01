from typing import Union, List, Optional

from src.model_wrapper import ModelWrapper
from pydantic import BaseModel


class HelloWorldRequest(BaseModel):
    sample: Optional[str]


class HelloWorldResponse(BaseModel):
    sample: Optional[str]


class HelloWorldModel(ModelWrapper):
    def __init__(self, file_name: str):
        super(HelloWorldModel, self).__init__(file_name) # base class loads file and makes a test prediction

    def validate_input(self, samples: Union[str, List[str]]) -> bool:
        return True

    def predict(self, samples: HelloWorldRequest):
        # Here is supposed to be a prediction
        return {
            'model_name': self.meta_data.model_name,
            "version": self.meta_data.version,
            'timestamp': self.meta_data.timestamp,
            "classes": 'Hello World!',
            "classes_proba": [('Hello World!', 0.9), ('Not Hello World!', 0.1)]
        }

    def test_predict(self, text: str = 'This is a text prediction; hopefully it works.'):
        try:
            return True
        except Exception as e:
            # TODO logging
            return False
