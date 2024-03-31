import json
import sys
from dataclasses import dataclass
from pathlib import Path

import toml


@dataclass
class Config:
    package: str
    extension: str
    library: str
    signatures: list[str]
    project_path: Path

    @property
    def platform(self) -> str:
        return sys.platform

    @staticmethod
    def get_path(child: str = None) -> Path:
        path = Path().absolute()
        if child:
            path = path / child
        return path

    @property
    def library_path(self) -> Path:
        return self.project_path / self.package / 'lib'

    @property
    def header_path(self) -> Path:
        return self.library_path / f'lib{self.library}.h'

    @property
    def shared_object_path(self) -> Path:
        return self.library_path / f'lib{self.library}.so'

    @property
    def extension_path(self) -> Path:
        return self.project_path / self.package / f'{self.extension}.abi3.so'

    @property
    def library_source_path(self) -> Path:
        return self.project_path / self.package / 'go'

    @classmethod
    def from_json(cls) -> 'Config':
        setup_path = cls.get_path('setup.py')
        config_path = cls.get_path('config.json')
        if setup_path.exists() and config_path.exists():
            with config_path.open('r') as f:
                data = json.load(f)
                data['project_path'] = setup_path.parent
                # TODO: validate data?
                return cls(**data)
        else:
            raise EnvironmentError

    @classmethod
    def from_toml(cls) -> 'Config':
        toml_path = cls.get_path('pyproject.toml')
        if toml_path.exists():
            with toml_path.open('r') as f:
                data = toml.load(f)
                data = data.get('tool', {}).get('pygo-tools', {})
                data['project_path'] = toml_path.parent
                # TODO: validate data?
                return cls(**data)
        else:
            raise EnvironmentError

    @classmethod
    def load(cls, mode: str = None) -> 'Config':
        mapping = {'json': cls.from_json, 'toml': cls.from_toml}
        if mode:
            return mapping[mode]()
        else:
            for mode in mapping:
                try:
                    return mapping[mode]()
                except EnvironmentError:
                    pass
            else:
                raise EnvironmentError

# TODO:
# - adopt `from typing import Self` once min python version raised to 3.11
