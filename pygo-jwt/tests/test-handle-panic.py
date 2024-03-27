import pygo_jwt

adapter = pygo_jwt.ExtensionAdapter()

for i in range(4):
    try:
        print(adapter.maybe_error(i))
        print(adapter.maybe_error(-i))
    except pygo_jwt.errors.CorePyGoJWTError as err:
        print('caught pygo error:', err)

for i in range(94, 106):
    try:
        print(adapter.maybe_error(i))
    except pygo_jwt.errors.CorePyGoJWTError as err:
        print(f'caught pygo error on {i=}:', err)
