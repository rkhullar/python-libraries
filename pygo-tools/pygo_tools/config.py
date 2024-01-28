import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Self


def _read_config() -> tuple[Path, dict]:
    project_path = Path().absolute()
    setup_path, config_path = project_path / 'setup.py', project_path / 'config.json'
    if setup_path.exists() and config_path.exists():
        with config_path.open('r') as f:
            return project_path, json.load(f)
    else:
        raise EnvironmentError


@dataclass
class Config:
    package: str
    extension: str
    library: str
    signatures: list[str]
    project_path: Path

    @classmethod
    def load(cls) -> Self:
        # NOTE: could be done with pydantic model validate
        project_path, data = _read_config()
        return cls(project_path=project_path, **data)

    @property
    def platform(self) -> str:
        return sys.platform

    @property
    def library_path(self) -> Path:
        return self.project_path / self.package / 'lib'

    @property
    def header_path(self) -> Path:
        return self.library_path / f'lib{self.library}.h'

    @property
    def shared_object_path(self) -> Path:
        return self.library_path / f'lib{self.library}.so'
