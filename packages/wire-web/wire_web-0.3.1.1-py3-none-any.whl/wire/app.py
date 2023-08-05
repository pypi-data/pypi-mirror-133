from wire.router import Router
from wire.request import Request
from wire.response import HTMLResponse, Response, PlainTextResponse, JsonResponse
from wire.groups import Group
from wire.static import StaticFiles
from wire.listener import EventListener
import inspect
import typing

class Wire:
    def __init__(self, strict: bool = True) -> None:
        self.router: Router = Router(strict=strict)
        self.__event_listener: EventListener = EventListener()

    async def __call__(self, scope: dict, receive, send) -> None:
        # lifespan handling
        if scope["type"] == "lifespan":
            while True:
                event = await receive()
                if event["type"] == "lifespan.startup":
                    await self.__event_listener("startup")
                    await send({'type': 'lifespan.startup.complete'})
                if event["type"] == "lifespan.":
                    pass
                elif event["type"] == "lifespan.shutdown":
                    await self.__event_listener("shutdown")
                    await send({'type': 'lifespan.shutdown.complete'})
                return 
        req = Request(scope, receive, send)
        try:
            func, params = await self.router.get_handler(req.path, req.method)
            if func:
                # async function
                if inspect.iscoroutinefunction(func):

                    response: typing.Union[Response, typing.Any] = await func(req, **params)
                    if not isinstance(response, Response):
                        if type(response) == str:
                            response = PlainTextResponse(response, 200)
                        elif type(response) == dict:
                            response = JsonResponse(response, 200)
                    await response(scope, receive, send)
                # static files
                elif isinstance(func, StaticFiles):
                    content, typ = func.provide(req.path)
                    resp = Response(content, headers={"content-type": typ})
                    await resp(scope, receive, send)
                 # sync function
                elif inspect.isfunction(func) and not inspect.iscoroutinefunction(func):
                    response: typing.Union[Response, typing.Any] = func(req, **params)
                    if not isinstance(response, Response):
                        if type(response) == str:
                            response = PlainTextResponse(response, 200)
                        elif type(response) == dict:
                            response = JsonResponse(response, 200)
                    await response(scope, receive, send)
        except Exception as e:
            response = HTMLResponse("Error occured", 404)
            await response(scope, receive, send)

    def get(self, path: str):
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> typing.Union[
            typing.Callable, typing.Awaitable]:
            self.router.add_route(path, handler, "get")
            return handler

        return wrapper

    def post(self, path: str):
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> typing.Union[
            typing.Callable, typing.Awaitable]:
            self.router.add_route(path, handler, "post")
            return handler

        return wrapper

    def put(self, path: str):
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> typing.Union[
            typing.Callable, typing.Awaitable]:
            self.router.add_route(path, handler, "put")
            return handler

        return wrapper

    def delete(self, path: str):
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> typing.Union[
            typing.Callable, typing.Awaitable]:
            self.router.add_route(path, handler, "delete")
            return handler

        return wrapper

    def mount(self, plugin: typing.Union[Group, StaticFiles], prefix: str = None):
        if isinstance(plugin, StaticFiles):
            self.router.add_route(prefix + "/*filename",  plugin, "get")
            return True
        if not prefix.startswith("/"):
            raise Exception(f"Invalid prefix for router {plugin}")
        else:
            for route in plugin.routes:
                self.router.add_route(prefix + route[0], route[1], route[2])
            return True


    def event(self, event: str) -> None:
        def wrapper(handler: typing.Union[typing.Callable, typing.Awaitable]) -> None:
            self.__event_listener.add(event, handler)
            return handler
        return wrapper