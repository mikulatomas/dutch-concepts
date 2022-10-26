import typing
import pkg_resources
import importlib.resources
import pathlib
import pandas as pd
import numpy as np

from functools import cache

from .loaders import load_exemplar_similarity, load_features, load_exemplar_judgements
from .enums import FeatureType, Language
from .constants import DATASET_NAME


class DutchConcepts:
    def __init__(
        self,
        language: Language = Language.ENGLISH,
        dataset_dir: typing.Optional[pathlib.Path] = None,
    ) -> None:
        self.language = language

        print(importlib.resources.files(""))

        if dataset_dir is None:
            self.dataset_dir = pathlib.Path(
                pkg_resources.resource_filename(__name__, "data")
            )
        else:
            self.dataset_dir = dataset_dir

        self.name = DATASET_NAME

        self.features = {
            feature_type: load_features(
                self.dataset_dir / self.language.value, feature_type
            )
            for feature_type in FeatureType
        }

        self.exemplar_judgements = load_exemplar_judgements(
            self.dataset_dir / self.language.value
        )

        self.exemplar_similarities = load_exemplar_similarity(
            self.dataset_dir / self.language.value
        )

    @cache
    def similarity_table(self) -> pd.DataFrame:
        data_dir = (
            pathlib.Path(pkg_resources.resource_filename(__name__, "data"))
            / self.language.value
        )

        dfs = [data.mean for data in load_exemplar_similarity(data_dir).values()]

        df = pd.concat(dfs)
        df = df.groupby(df.index).sum()
        df = df[sorted(df)]
        np.fill_diagonal(df.values, 1.0)

        return df

    def similarity(self, a: str, b: str) -> float:
        return self.similarity_table()[a][b]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.dataset_dir}, {self.language})"
