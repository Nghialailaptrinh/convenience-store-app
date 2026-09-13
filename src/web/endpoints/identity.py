from fastapi import APIRouter, Response
from pydantic import BaseModel, ConfigDict, Field, SecretStr

from application.common.models.authentication_result import AuthenticationResult
from application.identity.commands.login_user.login_user import LoginUserCommand
from application.identity.commands.register_user.register_user import RegisterUserCommand
from web.dependency_injection import SenderDependency

router = APIRouter(prefix="/identity", tags=["identity"])


class RegisterUserRequest(BaseModel):
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
    user_id = sender.send(RegisterUserCommand(request.email, request.password.get_secret_value()))
    response.headers["Cache-Control"] = "no-store"
    return UserCreatedResponse(user_id=user_id)


@router.post(
    "/login",
    response_model=AuthenticationResult,
    description="Step 2: verify credentials only. No token or session is issued yet.",
)
def login(request: LoginUserRequest, sender: SenderDependency, response: Response):
    result = sender.send(LoginUserCommand(request.email, request.password.get_secret_value()))
    response.headers["Cache-Control"] = "no-store"
    return result
