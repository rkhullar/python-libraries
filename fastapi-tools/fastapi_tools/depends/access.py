from fastapi import Security


def build_access_decorator(_type):
    def allowed_access(*data: str):
        def decorator(fn):
            def dependency(_: _type(data)):
                pass
            fn.api_route.dependencies.append(Security(dependency))
            return fn
        return decorator
    return allowed_access
