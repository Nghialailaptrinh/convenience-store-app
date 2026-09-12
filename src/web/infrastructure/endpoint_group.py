from typing import Protocol

from fastapi import APIRouter


class EndpointGroup(Protocol):
    router: APIRouter
