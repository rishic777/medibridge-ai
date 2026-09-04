"""Consistent API response envelope used by every endpoint."""
from __future__ import annotations

import uuid
from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel


def _jsonable(data: Any) -> Any:
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json")
    if isinstance(data, list):
        return [_jsonable(item) for item in data]
    return data


def success(data: Any = None, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "data": _jsonable(data),
            "error": None,
            "meta": {"request_id": str(uuid.uuid4())},
        },
    )


def error(code: str, message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "data": None,
            "error": {"code": code, "message": message},
            "meta": {"request_id": str(uuid.uuid4())},
        },
    )
