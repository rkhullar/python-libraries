[0.1.7] - 2024-04-09
- workaround to simplify wheel structure when building with `pyproject.toml`
- marks distribution as having extension module
- https://peps.python.org/pep-0427/#what-s-the-deal-with-purelib-vs-platlib

[0.1.6] - 2024-04-03

[0.1.5] - 2024-04-02

[0.1.4] - 2024-03-31

[0.1.3] - 2024-03-27

[0.1.2] - 2024-02-25
- fix entrypoint for `build-ffi`
- start support for `pyproject.toml`
- update command from `python setup.py bdist_wheel` to `python -m build -n --wheel`
- refactor `build-ffi` script
- add util for runtime monkey pathing

[0.1.1] - 2024-01-28
- test example from readme

[0.1.0] - 2024-01-28
- initial version with support for `setup.py` and `config.json`
