from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(role.value, role.name.title()) for role in cls]
