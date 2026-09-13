from dataclasses import dataclass, field


@dataclass(frozen=True)
class AuthenticationResult:
    user_id: str
    access_token: str = field(repr=False)
    expires_in: int
    token_type: str = "Bearer"
