from typing import Annotated

from fastapi import Depends, Request

from application.common.interfaces.sender import Sender
from application.dependency_injection import create_sender


def get_sender(request: Request) -> Sender:
    return create_sender(
        request.app.state.context_factory, request.app.state.payment, request.app.state.identity
    )


SenderDependency = Annotated[Sender, Depends(get_sender)]
