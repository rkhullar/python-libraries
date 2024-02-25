from contextlib import contextmanager
from pathlib import Path


@contextmanager
def temp_copy(source: Path, target: Path):
    # TODO: may be unused; return file handles?
    with source.open('rb') as s, target.open('wb') as t:
        t.write(s.read())
        try:
            yield
        finally:
            target.unlink()
