import os
import pytest
import logging

from src.config import Config, setup_logging, AspiredModel

dir_path = os.path.dirname(os.path.realpath(__file__))
model_dir = '{}/data/models'.format(dir_path)
config_dir = '{}/data/config'.format(dir_path)


# TODO aspired version equal

def test_config_init():
    correct_configs = ['config_1', 'config_2']
    correct_configs = ['{}/{}.json'.format(config_dir, config) for config in correct_configs]

    for config in correct_configs:
        c = Config(config, model_dir)
        assert True

    with pytest.raises(RuntimeError):
        config = '{}/config_empty.json'.format(config_dir)
        c = Config(config, model_dir)
    with pytest.raises(RuntimeError):
        config = '{}/config_duplicated_model_version.json'.format(config_dir)
        c = Config(config, model_dir)
    with pytest.raises(NotADirectoryError):
        config = '{}/config_empty.json'.format(config_dir)
        c = Config(config, 'ddd')


# for the sake of test coverage:

def test_aspired_model():
    json_dict = {
        "model_name": "simple_text",
        "aspired_version": "1.x",
        "load_type": "SHARE",
        "load_url": "data/models",
        "servable_name": "sklearn_text_input"
    }
    am = AspiredModel.from_json_dict(json_dict)
    assert True


def test_setup_logging():
    try:
        setup_logging('{}/logging.json'.format(config_dir))
        logging.debug('Logged')
        logging.info('Logged')
        logging.error('Logged')
        assert True
    except Exception as e:
        print(e)
        assert False
    with pytest.raises(FileNotFoundError):
        setup_logging('dream_path/')
