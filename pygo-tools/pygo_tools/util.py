import functools
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


@contextmanager
def monkey_patch(original: type, extended: type, to_patch: list[str]):
    original_methods = {key: getattr(original, key) for key in to_patch}
    extended_methods = {key: getattr(extended, key) for key in to_patch}
    for key in to_patch:
        @functools.wraps(original_methods[key])
        def wrapper(*args, **kwargs):
            original_methods[key](*args, **kwargs)
            return extended_methods[key](*args, **kwargs)
        setattr(original, key, wrapper)
    try:
        yield
    finally:
        for key in to_patch:
            setattr(original, key, original_methods[key])


def monkey_patched(original: type, extended: type, to_patch: list[str]):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            with monkey_patch(original, extended, to_patch):
                return fn(*args, **kwargs)
        return wrapper
    return decorator
