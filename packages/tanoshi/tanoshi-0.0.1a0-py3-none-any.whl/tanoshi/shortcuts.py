# Common shortcuts such as redirects and rendering templates
from __future__ import annotations

from typing import (
    Optional,
    TYPE_CHECKING,
    Dict,
    Any
)

from starlette.responses import RedirectResponse
from starlette.templating import _TemplateResponse

from . import fglobals

if TYPE_CHECKING:
    from starlette.requests import Request


def redirect(
    url: str,
    headers: Optional[dict] = None
) -> RedirectResponse:
    # we could alter the status code but this ruins the point of the redirect
    # since we need a 307 to redirect.
    
    return RedirectResponse(
        url=url,
        headers=headers
    )

def render(
    request: Request,
    template_name: str,
    context: Dict[str, Any] = {},
    *,
    headers: Optional[dict] = None,
    status_code: int = 200,
    media_type: Optional[str] = None
) -> _TemplateResponse:
    context["request"] = request
    engine = fglobals.templating_engine
    response = engine.TemplateResponse(
        name=template_name,
        context=context,
        status_code=status_code,
        headers=headers,
        media_type=media_type
    )

    return response
