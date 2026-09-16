from typing import Annotated

from fastapi import Depends, Request, Response

from application.common.interfaces.current_user import ICurrentUser
from application.common.interfaces.sender import Sender
from application.dependency_injection import create_sender
from web.infrastructure.authentication import get_current_user


def get_sender(request: Request) -> Sender:
    return create_sender(
        request.app.state.context_factory,
        request.app.state.payment,
        request.app.state.identity,
        request.app.state.tokens,
    )


SenderDependency = Annotated[Sender, Depends(get_sender)]


def get_authenticated_sender(
    request: Request,
    response: Response,
    current_user: Annotated[ICurrentUser, Depends(get_current_user)],
) -> Sender:
    response.headers["Cache-Control"] = "no-store"
    return create_sender(
        request.app.state.context_factory,
        request.app.state.payment,
        request.app.state.identity,
        request.app.state.tokens,
        current_user,
    )


AuthenticatedSenderDependency = Annotated[Sender, Depends(get_authenticated_sender)]
