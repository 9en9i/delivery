from delivery.core.enums.actors import ActorEnum


class ActorService:
    actor_type: ActorEnum

    async def auth(self, email: str, password: str) -> ActorEnum | None:
        raise NotImplementedError

    class Validation:
        @staticmethod
        def to_many_scopes(scopes: set[ActorEnum]) -> bool:
            return len(scopes) > 1
