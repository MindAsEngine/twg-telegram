from dataclasses import dataclass


@dataclass
class UserState:
    username: str | None
    is_authorized: bool = False
    is_wait_phone: bool = False
    is_agent: bool = False
    access_token: str | None = None
    refresh_token: str | None = None

    def __init__(self,
                 username: str | None = None,
                 is_authorized: bool = False,
                 is_wait_phone: bool = False,
                 is_agent: bool = False,
                 access_token: str | None = None,
                 refresh_token: str | None = None,
                 **_):
        self.username = username
        self.is_authorized = is_authorized
        self.is_wait_phone = is_wait_phone
        self.is_agent = is_agent
        self.access_token = access_token
        self.refresh_token = refresh_token

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "is_authorized": self.is_authorized,
            "is_wait_phone": self.is_wait_phone,
            "is_agent": self.is_agent,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }

    def clear(self) -> None:
        self.is_authorized = False
        self.access_token = None
        self.refresh_token = None
        self.is_wait_phone = False
