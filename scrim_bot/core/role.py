from enum import Enum, unique


class RoleIsInvalid(Exception):
    """
    Exception raised if the role is invalid.
    """
    def __init__(self, role: str):
        self.role = role

    def __str__(self):
        return repr(self.role)


@unique
class Role(Enum):
    """
    Enumeration implementation of the possible roles along with a validator.
    """

    TOP = 1
    JUNGLE = 2
    MID = 3
    BOT = 4
    SUPPORT = 5
    INVALID = 6

    # Validator that returns the correct enum value for the respective role
    @classmethod
    def validateRole(cls, role: str):
        if role in ["Top", "top", "TOP"]:
            return cls.TOP
        if role in ["Jungle", "jungle", "JUNGLE", "jg", "JG", "Jg", "Jgl", "jgl", "JGL"]:
            return cls.JUNGLE
        if role in ["Mid", "mid", "MID"]:
            return cls.MID
        if role in ["Bot", "bot", "BOT", "AD", "ad", "ADC", "adc"]:
            return cls.BOT
        if role in ["Support", "support", "SUPPORT", "Supp", "supp", "SUPP", "Sup", "sup", "SUP"]:
            return cls.SUPPORT
        return cls.INVALID
