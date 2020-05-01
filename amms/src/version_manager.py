from __future__ import annotations

from typing import Union


class VersionManager:
    """
    Version naming convention:
    Main version - incompatible to code
    Sub version - compatible code, even though the model is different
    Sub sub version - Additional changes, for instance retraining
    """

    def __init__(self, version: str):
        self.set_version(version)

    def set_version(self, version: str):
        if '.' in version:
            version = version.split('.')
        elif '_' in version:
            version = version.split('_')
        else:
            raise ValueError('TODO; only . or _ allowed for model versions')
        main_version = int(version[0])
        if version[1] == 'x':
            sub_version = 'x'
            sub_sub_version = 'x'
        else:
            sub_version = int(version[1])
            sub_sub_version = int(version[2]) if len(version) > 2 else 'x'

        self.version = '_'.join(version)
        self.main_version = main_version
        self.sub_version = sub_version
        self.sub_sub_version = sub_sub_version

    def is_equal(self, version: Union[str, VersionManager]) -> bool:
        if isinstance(version, VersionManager):
            version = version.tostr()

        if self.tostr() == version:
            return True
        return False

    def is_compatible_and_newer(self, version: Union[str, VersionManager]) -> bool:
        if isinstance(version, str):
            version = VersionManager(version)

        if isinstance(version, VersionManager) is False:
            raise ValueError('You need to provide a version string or a object of type `Version`.')

        if version.main_version != self.main_version:
            return False
        elif version.sub_version > self.sub_version:
            return True
        elif version.sub_version == self.sub_version and version.sub_sub_version > self.sub_sub_version:
            return True
        else:
            return False

    @staticmethod
    def from_file_name(file_name: str) -> VersionManager:
        # TODO link to model naming convention/description
        split = file_name.split('-')
        if len(split) != 3:
            raise ValueError('File format is incorrect. Make sure you use only 2 `-` in your model names.')
        return VersionManager(split[1])

    def tostr(self):
        return "{}_{}_{}".format(self.main_version, self.sub_version, self.sub_sub_version)
