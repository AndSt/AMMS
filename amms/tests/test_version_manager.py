import pytest

from src.version_manager import VersionManager, AspiredModel


# TODO: Add more examples: How to handle .x comparisons?

def test_init():
    examples = ['1_0', '1_x', '1_0_1']
    for example in examples:
        version = VersionManager(example)


def test_is_equal():
    examples = [
        ('1.0', '1_0'),
        ('1', '1_0_0'),
        ('1.1.0', '1.1'),
        ('1.x', '1.x.5'),
        ('1.x', '1.x.x')
    ]
    for example in examples:
        version = VersionManager(example[0])
        other = VersionManager(example[1])
        assert version == other
        assert version.__eq__(example[1])


def test_is_compatible_and_newer():
    # test whether 2nd entry is compatible and newer than first entry
    examples = [
        ('1.0', '1_0', False),
        ('1', '2.0', False),
        ('1.3', '1.5.2', True),
        ('1.3', '1.3.2', True),
        ('1.3.4', '1.3.8', True)
    ]
    for example in examples:
        version = VersionManager(example[0])
        other = VersionManager(example[1])
        assert version.is_compatible_and_newer(other) == example[2]

    x_test = ('1.x', '1.5.7')
    try:
        VersionManager(x_test[1]).is_compatible_and_newer(x_test[0])
        assert False
    except ValueError:
        assert True


def test_from_file_name():
    examples = [
        ('simple_text-1_0_2-1588436916.135168.pbz2', '1.0.1'),
        ('simple_text-1_x-1588110709.491364.pbz2', '1.x')
    ]
    for example in examples:
        version = VersionManager.from_file_name(example[0])
        assert version.__eq__(VersionManager(example[1]))
        assert version.__eq__(example[1])


@pytest.fixture()
def aspired_model_dict():
    return {
        'model_name': 'test_name',
        'aspired_version': '1.x',
        'load_type': 'SHARE',
        'load_url': 'data/model_load_dir',
        'servable_name': 'hello_world'
    }


def test_aspired_model_from_file_name(aspired_model_dict):
    with pytest.raises(ValueError):
        AspiredModel.from_json_dict({})
        bad_json_dict = aspired_model_dict.copy()
        bad_json_dict['name'] = 1234
        AspiredModel.from_json_dict(bad_json_dict)
    try:
        am = AspiredModel.from_json_dict(aspired_model_dict)
        assert True
    except:
        assert False


# TODO test stringifiers

def test_aspired_model_is_compatible(aspired_model_dict):
    am = AspiredModel.from_json_dict(aspired_model_dict)
    compatible_file_name = 'test_name-1.2.3-1234.pbz2'
    incompatible_file_name = 'test_name-1'


