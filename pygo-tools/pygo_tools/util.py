from pathlib import Path
from contextlib import contextmanager


@contextmanager
def temp_copy(source: Path, target: Path):
    with source.open('rb') as s, target.open('wb') as t:
        t.write(s.read())
        try:
            yield
        finally:
            target.unlink()
