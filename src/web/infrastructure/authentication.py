from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.common.exceptions.unauthenticated import UnauthenticatedError
from application.common.interfaces.current_user import ICurrentUser
from web.services.current_user import CurrentUser

bearer = HTTPBearer(auto_error=False, description="Access token returned by POST /identity/login")


def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> ICurrentUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthenticatedError()
    user_id = request.app.state.tokens.validate(credentials.credentials)
    if user_id is None:
        raise UnauthenticatedError()
    return CurrentUser(user_id)
