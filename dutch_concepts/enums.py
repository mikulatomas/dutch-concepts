from enum import Enum

__all__ = ["Category", "Domain"]


class FeatureType(Enum):
    EXEMPLAR = "exemplar"
    CATEGORY = "category"


class Category(Enum):
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

    def __repr__(self):
        return f"Category.{self.name}"

    def to_filename(self):
        return self.value.replace(" ", "_")

    @staticmethod
    def from_str(label):
        label = label.lower()
        if label[-1] == "s":
            label = label[:-1]

        label = label.upper()
        label = label.replace(" ", "_")

        return Category[label]


class Domain(Enum):
    ANIMAL = "animal"
    ARTIFACT = "artifact"
    OTHERS = "others"

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

    def __repr__(self):
        return f"Domain.{self.name}"

    def to_filename(self):
        return self.value.replace(" ", "_")

    @staticmethod
    def from_str(label):
        label = label.lower()
        if label[-1] == "s":
            label = label[:-1]

        label = label.upper()

        return Domain[label]
