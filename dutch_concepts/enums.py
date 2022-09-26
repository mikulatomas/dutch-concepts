from enum import Enum

__all__ = ["Category", "Domain", "Language", "FeatureType"]


class Language(Enum):
    ENGLISH = "en"
    DUTCH = "nl"

    def __str__(self):
        return self.name.title()


class FeatureType(Enum):
    EXEMPLAR = "exemplar"
    CATEGORY = "category"

    def __str__(self):
        return self.name.title()


class StringMixin:
    @classmethod
    def from_str(cls, label):
        label = label.lower()
        label = label.rstrip("s")
        label = label.replace("_", " ")

        return cls(label)

    def to_filename(self):
        return self.value.replace(" ", "_")

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def __str__(self):
        return self.value.title().replace(" ", "")


class Category(StringMixin, Enum):
    BIRD = "bird"
    CLOTHING = "clothing"
    FRUIT = "fruit"
    FISH = "fish"
    INSECT = "insect"
    KITCHEN_UTENSIL = "kitchen utensil"
    MAMMAL = "mammal"
    MUSICAL_INSTRUMENT = "musical instrument"
    PROFESSION = "profession"
    REPTILE = "reptile"
    SPORT = "sport"
    TOOL = "tool"
    VEGETABLE = "vegetable"
    VEHICLE = "vehicle"
    WEAPON = "weapon"


class Domain(StringMixin, Enum):
    ANIMAL = "animal"
    ARTIFACT = "artifact"
    OTHER = "other"

    @property
    def members(self):
        if self == Domain.ANIMAL:
            return (
                Category.BIRD,
                Category.FISH,
                Category.INSECT,
                Category.MAMMAL,
                Category.REPTILE,
            )
        elif self == Domain.ARTIFACT:
            return (
                Category.CLOTHING,
                Category.KITCHEN_UTENSIL,
                Category.MUSICAL_INSTRUMENT,
                Category.TOOL,
                Category.VEHICLE,
                Category.WEAPON,
            )
        else:
            return (
                Category.VEGETABLE,
                Category.SPORT,
                Category.PROFESSION,
                Category.FRUIT,
            )
