from pathlib import Path


def read_data(name: str) -> str:
    path = Path(__file__).parent / 'local' / name
    with path.open('r') as f:
        return f.read().strip()


def write_data(name: str, data: str):
    path = Path(__file__).parent / 'local' / name
    with path.open('w') as f:
        f.write(data.strip())


example_payload = {'message': 'hello world', 'count': 4, "nested": {"x": 1, "a": 2}}
