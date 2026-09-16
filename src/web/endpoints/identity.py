from fastapi import APIRouter, Response
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from application.common.models.authentication_result import AuthenticationResult
from application.identity.commands.login_user.login_user import LoginUserCommand
from application.identity.commands.register_user.register_user import RegisterUserCommand
from application.identity.queries.get_current_user.current_user_dto import CurrentUserDto
from application.identity.queries.get_current_user.get_current_user import GetCurrentUserQuery
from web.dependency_injection import AuthenticatedSenderDependency, SenderDependency

router = APIRouter(prefix="/identity", tags=["identity"])


class RegisterUserRequest(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    model_config = ConfigDict(extra="forbid", strict=True)
    email: str = Field(max_length=254)
    password: SecretStr = Field(max_length=128)


class LoginUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    email: str = Field(max_length=254)
    password: SecretStr = Field(max_length=128)


class UserCreatedResponse(BaseModel):
    user_id: str


@router.post("/register", status_code=201, response_model=UserCreatedResponse)
def register(request: RegisterUserRequest, sender: SenderDependency, response: Response):
    user_id = sender.send(
        RegisterUserCommand(request.email, request.password.get_secret_value(), request.name)
    )
    response.headers["Cache-Control"] = "no-store"
    return UserCreatedResponse(user_id=user_id)


@router.post(
    "/login",
    response_model=AuthenticationResult,
    description="Verify credentials and issue a Bearer token. See expires_in for its lifetime.",
)
def login(request: LoginUserRequest, sender: SenderDependency, response: Response):
    result = sender.send(LoginUserCommand(request.email, request.password.get_secret_value()))
    response.headers["Cache-Control"] = "no-store"
    return result


@router.get("/me", response_model=CurrentUserDto)
def current_user(sender: AuthenticatedSenderDependency, response: Response):
    response.headers["Cache-Control"] = "no-store"
    return sender.send(GetCurrentUserQuery())
