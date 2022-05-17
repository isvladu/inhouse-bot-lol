import logging

from scrim_bot.core.role import Role, RoleIsInvalid

logger = logging.getLogger(__name__)


class Player:
    """
    Represents a player taking part in inhouse games
    """

    _id: int
    _name: str
    roles: list[Role]
    elo: float
    summoner_name: str

    def __init__(self, _id: int, name: str, roles: list[str] = None, elo: float = None, summoner_name: str = None):
        self._id = _id
        self._name = name
        self.roles = []
        self.elo = elo
        self.summoner_name = summoner_name

        if roles is not None:
            self.addRoles(roles)

    def addRole(self, role: str):
        validated_role = Role.validateRole(role)
        if validated_role == Role.INVALID:
            logger.error(f"Role {role} is invalid")
            raise RoleIsInvalid(role)
        if validated_role in self.roles:
            logger.error(f"Role {validated_role.name} is already registered")
            return
        logger.info(f"Role {validated_role.name} has been registered")
        self.roles.append(validated_role)

    def addRoles(self, role_list: list[str]):
        for role in role_list:
            self.addRole(role)

    def removeRole(self, role: str):
        validated_role = Role.validateRole(role)
        if validated_role == Role.INVALID:
            logger.error(f"Role {role} is invalid")
            raise RoleIsInvalid(role)
        if validated_role not in self.roles:
            logger.error(f"Role {validated_role.name} is not registered")
            return
        logger.info(f"Role {validated_role} has been removed")
        self.roles.remove(validated_role)

    def removeRoles(self, role_list: list[str]):
        for role in role_list:
            self.removeRole(role)

    def getRoles(self):
        return [role.name for role in self.roles]

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    # Encoding Player() object for MongoDB queries
    def encode_player(self):
        return {"_id": self._id, "name": self._name, "roles": self.getRoles(), "elo": self.elo,
                "summoner_name": self.summoner_name}
