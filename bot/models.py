from dataclasses import dataclass


@dataclass
class UserState:
    id: int | None
    is_authorized: bool = False
    is_wait_phone: bool = False

    def __init__(self,
                 id: int | None = None,
                 is_authorized: bool = False,
                 is_wait_phone: bool = False,
                 **_):
        self.id = id
        self.is_authorized = is_authorized
        self.is_wait_phone = is_wait_phone

    def to_dict(self):
        return {
            "id": self.id,
            "is_authorized": self.is_authorized,
            "is_wait_phone": self.is_wait_phone,
        }

    def clear(self):
        self.is_authorized = False
        self.is_wait_phone = False
