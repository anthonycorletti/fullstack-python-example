from typing import Any, Callable, Dict, List

from fastapi import Request, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from app.settings import ResponseFormat


class RespondWith(BaseModel):
    data: Dict | List | BaseModel | None = None
    page: Callable | None = None


async def respond_to(
    request: Request,
    response_options: Dict[ResponseFormat, Dict] | None,
) -> Any:
    if response_options is None:
        response_options = {}
        response_options[ResponseFormat.default] = {}

    if ResponseFormat.default not in response_options:
        response_options[ResponseFormat.default] = response_options.get(
            ResponseFormat.html, {}
        )

    _format = await format_method(request=request)
    if response_options is None:
        _with = RespondWith(data=None, page=None)
    else:
        _with = RespondWith(**response_options.get(_format, {}))
    if _format == ResponseFormat.json:
        return _with.data
    elif _format == ResponseFormat.html or _format == ResponseFormat.default:
        if _with.page:
            if len(_with.page.__annotations__) > 0:
                p = await _with.page(_with.data)
            else:
                p = _with.page()
            return await p.doc.render_html()
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"respond_to: no page provided for {_format} format.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Unsupported accept header: {_format}",
        )


async def format_method(request: Request) -> ResponseFormat:
    v = request.headers.get("accept")
    if not v:
        return ResponseFormat.default
    _accept = v.split(";")[0].split(",")[0]
    if _accept == ResponseFormat.html.value:
        return ResponseFormat.html
    elif _accept == ResponseFormat.json.value:
        return ResponseFormat.json
    else:
        return ResponseFormat.default
