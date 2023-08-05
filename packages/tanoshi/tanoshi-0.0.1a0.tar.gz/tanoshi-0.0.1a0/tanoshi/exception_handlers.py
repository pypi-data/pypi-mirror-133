from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse


async def default_http_exception_handler(
    _: Request,
    exc: HTTPException
) -> HTMLResponse:
    content = "<h1>{status_code}: {detail}</h1>"

    return HTMLResponse(
        content=content,
        status_code=exc.status_code
    )
