from uuid import uuid4, UUID

from .event import Event


class Entity():
    id: UUID = uuid4()
    events: list[Event] = []

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
