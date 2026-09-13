from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticationResult:
    """Step 2: credentials verified. This is not a token or an authenticated session."""

    user_id: str
