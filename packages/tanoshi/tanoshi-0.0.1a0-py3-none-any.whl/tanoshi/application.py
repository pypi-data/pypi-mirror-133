import warnings
from typing import (
    List,
    Callable,
    Optional,
    Dict
)

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles

from . import fglobals
from .exception_handlers import default_http_exception_handler


class Tanoshi(Starlette):
    def __init__(
        self,
        *,
        name: str = "TanoshiApplication",
        debug: bool = False,
        exception_handlers: Dict[Exception, Callable] = {},
        templates_directory: Optional[str] = None,
        static_files_directory: Optional[str] = None,
        static_path: Optional[str] = None
    ):
        super().__init__(
            debug=debug
        )

        self.name = name
        self.debug = debug

        # override with custom exception handlers
        self.exception_handlers = exception_handlers
        self.exception_handlers.setdefault(HTTPException, default_http_exception_handler)

        if templates_directory is not None:
            # update templating globals
            fglobals.templates_directory = templates_directory
            fglobals._update_templating_engine(directory=templates_directory)

        if static_files_directory is not None:
            if static_path is None:
                warnings.warn("static_path has not been set, defaulting to /static")
                static_path = "/static"
            # mount static files
            sf_app = StaticFiles(directory=static_files_directory)
            self.router.mount(
                path=static_path,
                app=sf_app,
                name="static"
            )
    
    def route(
        self,
        path: str,
        *,
        name: Optional[str] = None,
        methods: List[str] = ["GET"]
    ):
        def decorator(func: Callable):
            route_name = name or func.__name__
            self.router.add_route(
                path=path,
                endpoint=func,
                methods=methods,
                name=route_name
            )
        
        return decorator