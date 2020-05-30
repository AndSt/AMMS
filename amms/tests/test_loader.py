import os
import pytest
from typing import List

from src.config import AspiredModel
from src.loader import Loader, LocalLoader, LoadType

dir_path = os.path.dirname(os.path.realpath(__file__))
model_dir = '{}/data/loaded'.format(dir_path)


@pytest.fixture()
def aspired_models() -> List[AspiredModel]:
    asp_1 = AspiredModel(model_name='hello_world', aspired_version='1.x', load_type='SHARE',
                         load_url='{}/data/model_load_dir'.format(dir_path), servable_name='name')
    asp_2 = AspiredModel(model_name='simple_text', aspired_version='1.x', load_type='SHARE',
                         load_url='{}/data/model_load_dir'.format(dir_path), servable_name='name')
    return asp_1, asp_2


@pytest.fixture()
def loaders(aspired_models) -> List[Loader]:
    asp_1, asp_2 = aspired_models
    return LocalLoader(asp_1, model_dir), LocalLoader(asp_2, model_dir)


@pytest.fixture()
def file_names() -> List[str]:
    return ['hello_world-1_0_1-1234.pbz2', 'simple_text-1_0_1-1588436916.135168.pbz2']


def test_from_aspired_model(aspired_models):
    asp_1, asp_2 = aspired_models
    asp_1.load_type = LoadType.local
    l = Loader.from_aspired_model(asp_1, '{}/data/model_load_dir'.format(dir_path))
    asp_2.load_type = 'TEST'
    with pytest.raises(NotImplementedError):
        l = Loader.from_aspired_model(asp_2, '{}/data/model_load_dir'.format(dir_path))


def test_abstract_methods(aspired_models, file_names):
    asp_1, asp_2 = aspired_models
    l = Loader(asp_1, '{}/data/model_load_dir'.format(dir_path))
    with pytest.raises(NotImplementedError):
        l.load_available_models()
    with pytest.raises(NotImplementedError):
        l.load(file_names[0])


def test_loader_dir_not_found(aspired_models):
    for aspired_model in aspired_models:
        with pytest.raises(NotADirectoryError):
            l = Loader(aspired_model, 'not/existing/dir')


def test_load_available_model_versions(loaders, file_names):
    for i in range(len(loaders)):
        loaded_file_names = loaders[i].load_available_models()
        assert loaded_file_names == [file_names[i]]


def test_load(loaders: List[Loader], file_names: List[str]):
    # Test wrong file name format
    wrong_file_name_format = 1234
    for i in range(len(loaders)):
        with pytest.raises(ValueError):
            loaders[i].load(wrong_file_name_format)

    # Test non existent file
    non_existing_file = 'non_existing_file.pbz2'
    for i in range(len(loaders)):
        with pytest.raises(FileNotFoundError):
            loaders[i].load(non_existing_file)

    # Test correct cases
    for i in range(len(file_names)):
        loaded = loaders[i].load(file_names[i])
