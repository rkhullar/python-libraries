from fastapi import APIRouter as DefaultRouter


class APIRouter(DefaultRouter):
    """custom base api router for allowing route handlers to be decorated"""

    def api_route(self, *args, **kwargs):
        parent_decorator = super().api_route(*args, **kwargs)

        def decorator(fn):
            parent_decorator(fn)
            fn.api_route = self.routes[-1]
            assert fn == fn.api_route.endpoint
            return fn

        return decorator
