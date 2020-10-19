from __future__ import annotations

from typing import Union, Dict
from enum import Enum


class VersionManager:
    """
    Version naming convention:
    Main version - incompatible to code
    Sub version - compatible code, even though the model is different
    Sub sub version - Additional changes, for instance retraining
    """

    def __init__(self, version_str: str):
        if isinstance(version_str, str) is False:
            raise ValueError('No string given: {}'.format(version_str))

        # Scenario 1: Only main version number is given
        if version_str.isdigit():
            self.main_version = int(version_str)
            self.sub_version = 0
            self.sub_sub_version = 0
            self.is_exact_specification = True
            return

        # Determine, whether '.' or '_' format is used to describe versions.
        if '.' in version_str:
            version_str = version_str.split('.')
        elif '_' in version_str:
            version_str = version_str.split('_')
        else:
            raise ValueError('TODO; only . or _ allowed for model versions')
        # correctness checks
        # First version is not allowed to be arbitrary
        if version_str[0].isdigit() is False:
            raise ValueError('The top-level version needs to be set, as it marks breaking model changes.')
        # Only numbers or 'x' allowed
        for x in version_str:
            if x.isdigit() is False and x != 'x':
                raise ValueError(
                    'A correct version is only allowed to hold numbers and \'x\' to describe an arbitrary number ')

        # First version is not allowed to be arbitrary
        self.main_version = int(version_str[0])

        # Scenario 2: First sublevel is set to x. Then it doesn't matter how the third level is designed
        if version_str[1] == 'x':
            self.sub_version = 'x'
            self.sub_sub_version = 'x'
            self.is_exact_specification = False
            return

        # Now we know, we can set the first subversion as number
        self.sub_version = int(version_str[1])

        # Scenario 3: Only top and sublevel version are defined
        if len(version_str) == 2:
            self.sub_sub_version = 0
            self.is_exact_specification = True
            return

        # Scenario 4: All levels are specified, but maybe as 'x'
        if version_str[2] == 'x':
            self.sub_sub_version = 'x'
            self.is_exact_specification = False
        else:
            self.sub_sub_version = int(version_str[2])
            self.is_exact_specification = True

    def __eq__(self, other: Union[str, VersionManager]) -> bool:
        if isinstance(other, str):
            other = VersionManager(other)

        if self.main_version != other.main_version:
            return False
        elif self.sub_version != other.sub_version:
            return False
        elif self.sub_sub_version != other.sub_sub_version:
            return False
        return True

    def is_compatible_and_newer(self, other: Union[str, VersionManager]) -> bool:
        # TODO rewrite; what does compatible and newer mean anyway??
        if isinstance(other, str):
            other = VersionManager(other)

        if self.is_exact_specification is False or other.is_exact_specification is False:
            raise ValueError('Only versions with an exact specification, i.e. no \'x\' can be compared.')

        if other.main_version != self.main_version:
            return False
        elif other.sub_version > self.sub_version:
            return True
        elif other.sub_version == self.sub_version and other.sub_sub_version > self.sub_sub_version:
            return True
        else:
            return False

    def is_newer(self, other: Union[str, VersionManager], compatible: bool = True) -> bool:
        if isinstance(other, str):
            other = VersionManager(other)

        if self.is_exact_specification is False or other.is_exact_specification is False:
            raise ValueError('Only versions with an exact specification, i.e. no \'x\' can be compared.')

        if not compatible and other.main_version > self.main_version:
            return True
        if compatible and other.main_version != self.main_version:
            return False

        if other.sub_version > self.sub_version:
            return True
        elif other.sub_version == self.sub_version and other.sub_sub_version > self.sub_sub_version:
            return True
        else:
            return False

    @staticmethod
    def from_file_name(file_name: str) -> VersionManager:
        split = file_name.split('-')
        if len(split) != 3:
            raise ValueError('File format is incorrect. Make sure you use only 2 `-` in your model names. '
                             'Go to README.md to understand the file naming and versioning conventions.')
        return VersionManager(split[1])

    def __str__(self):
        return "{}.{}.{}".format(self.main_version, self.sub_version, self.sub_sub_version)

    def to_file_str(self):
        return "{}_{}_{}".format(self.main_version, self.sub_version, self.sub_sub_version)


# Substitute load_type str with enum
class LoadType(Enum):
    local = 'LOCAL'
    shared = 'SHARE'


class AspiredModel:
    """Container holding information about a model version we want to load and how to load it.
    Aspired version format:

    """

    def __init__(self, model_name: str, aspired_version: str, load_type: str, load_url: str, servable_name: str):
        self.model_name = model_name
        self.aspired_version = VersionManager(aspired_version)
        self.load_type = LoadType(load_type)
        self.load_url = load_url

        self.servable_name = servable_name

    @staticmethod
    def from_json_dict(json_dict: Dict[str, str]) -> AspiredModel:
        fields = ['model_name', 'aspired_version', 'load_type', 'load_url', 'servable_name']
        for field in fields:
            if field not in json_dict:
                raise ValueError('The configuration needs to hold a parameter `{}`.'.format(field))
            if isinstance(json_dict[field], str) is False:
                raise ValueError(
                    'Field `{}` has to be of type `str`, but is `{}`.'.format(field, type(json_dict[field])))

        return AspiredModel(json_dict['model_name'], json_dict['aspired_version'], json_dict['load_type'],
                            json_dict['load_url'], json_dict['servable_name'])

    def is_compatible(self, file_name: str) -> bool:
        # TODO maybe use as Servable MetaData -> two way import maybe problem
        if isinstance(file_name, str) is False:
            raise ValueError(
                'is_compatible only accepts type `str`, given is {} of type {}'.format(file_name, type(file_name)))

        split = file_name.split('-')
        if split[0] == self.model_name:
            return True  # TODO
        else:
            return False

    # def __str__(self):
    #     return "{}-{}-"

    # TODO
    # - this equality test
    # - test whether 2 aspire same version here?
    # def __eq__(self, other: AspiredModel) -> bool:
    #
    #     if self.model_name == other.model_name and self.aspired_version == other.aspired_version and \
    #             self.load_type == other.load_type and self.load_url == other.load_url and \
    #             self.servable_name == other.servable_name:
    #         return True
    #     return False
