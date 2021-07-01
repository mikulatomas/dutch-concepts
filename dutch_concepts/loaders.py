import os
import re

from typing import NamedTuple

import pandas as pd
from glob import glob

from .enums import Category, Domain, FeatureType

EXEMPLAR_FEATURES_JUDGEMENTS_FOLDER = "exemplar_feature_judgments"
CATEGORY_FEATURES_FOLDER = "category_features"
EXEMPLAR_FEATURES_FOLDER = "exemplar_features"
PAIRWISE_SIMILARITY_FOLDER = "pairwise_similarities"
RESPONDENTS_FOLDER = "respondents"
FEATURE_FREQUENCY_FOLDER = "feature_generation_frequency"
FEATURE_IMPORTANCE_RATINGS_FOLDER = "feature_importance_ratings"


class ExemplarSimilarityData(NamedTuple):
    category: Category
    mean: pd.DataFrame
    respondents: dict

    def __repr__(self):
        return "ExemplarSimilarityData({})".format(self.category)


class FeaturesDomainData(NamedTuple):
    domain: Domain
    feature_matrix: pd.DataFrame
    feature_matrix_respondents: dict
    feature_frequency: pd.DataFrame
    feature_type: FeatureType

    def __repr__(self):
        return "FeaturesDomainData({}, {})".format(self.domain, self.feature_type)


class FeaturesCategoryData(NamedTuple):
    domain: Category
    feature_matrix: pd.DataFrame
    feature_matrix_respondents: dict
    feature_frequency: pd.DataFrame
    feature_importance_ratings: pd.DataFrame
    feature_type: FeatureType

    def __repr__(self):
        return "FeaturesCategoryData({}, {})".format(self.domain, self.feature_type)


class Features(NamedTuple):
    domain: dict
    category: dict
    feature_type: FeatureType

    def __repr__(self):
        return "Features({})".format(self.feature_type)


def load_respondents(source_folder):
    respondents = {}

    for respondent in glob(os.path.join(source_folder, "*.csv")):
        id = re.search(
            "^(.*)_respondent_(.*).csv$", os.path.basename(respondent)
        ).group(2)

        respondents[id] = pd.read_csv(respondent, index_col=0)

    return respondents


def load_features(dataset_folder, feature_type):
    if feature_type is FeatureType.CATEGORY:
        type_folder = CATEGORY_FEATURES_FOLDER
    else:
        type_folder = EXEMPLAR_FEATURES_FOLDER

    folder = os.path.join(
        dataset_folder, EXEMPLAR_FEATURES_JUDGEMENTS_FOLDER, type_folder
    )

    domain = load_domain_features(folder, feature_type)
    category = load_category_features(folder, feature_type)

    return Features(domain, category, feature_type)


def load_domain_features(source_folder, feature_type):
    domains = {}

    for domain_folder in glob(os.path.join(source_folder, "domains", "*")):
        domain = Domain.from_str(os.path.basename(domain_folder))

        feature_matrix = pd.read_csv(
            glob(os.path.join(domain_folder, "*.csv"))[0], index_col=0
        )

        respondents = load_respondents(os.path.join(domain_folder, RESPONDENTS_FOLDER))

        feature_frequency = load_feature_frequency(
            os.path.join(source_folder, FEATURE_FREQUENCY_FOLDER), domain
        )

        domains[domain] = FeaturesDomainData(
            domain, feature_matrix, respondents, feature_frequency, feature_type
        )

    return domains


def load_category_features(source_folder, feature_type):
    categories = {}

    for category_folder in glob(os.path.join(source_folder, "categories", "*")):
        category = Category.from_str(os.path.basename(category_folder))

        feature_matrix = pd.read_csv(
            glob(os.path.join(category_folder, "*.csv"))[0], index_col=0
        )

        respondents = load_respondents(
            os.path.join(category_folder, RESPONDENTS_FOLDER)
        )

        feature_frequency = load_feature_frequency(
            os.path.join(source_folder, FEATURE_FREQUENCY_FOLDER), category
        )

        feature_importance_ratings = load_feature_importance_ratings(
            os.path.join(source_folder, FEATURE_IMPORTANCE_RATINGS_FOLDER), category
        )

        categories[category] = FeaturesCategoryData(
            category,
            feature_matrix,
            respondents,
            feature_frequency,
            feature_importance_ratings,
            feature_type,
        )

    return categories


def load_feature_importance_ratings(source_folder, category):
    return pd.read_csv(
        glob(os.path.join(source_folder, f"{category.to_filename()}*.csv"))[0],
        index_col=0,
    )


def load_feature_frequency(source_folder, kind):
    if type(kind) is Domain:
        folder = os.path.join(source_folder, "domains")
    else:
        folder = os.path.join(source_folder, "categories")

    return pd.read_csv(
        glob(os.path.join(folder, f"{kind.to_filename()}*.csv"))[0], index_col=0
    )


def load_exemplar_similarity(dataset_folder):
    dataset = {}

    for category_folder in glob(
        os.path.join(dataset_folder, PAIRWISE_SIMILARITY_FOLDER, "*")
    ):
        category = Category.from_str(os.path.basename(category_folder))

        mean_similarities = pd.read_csv(
            glob(os.path.join(category_folder, "*.csv"))[0], index_col=0
        )

        respondents = load_respondents(
            os.path.join(category_folder, RESPONDENTS_FOLDER)
        )

        dataset[category] = ExemplarSimilarityData(
            category, mean_similarities, respondents
        )

    return dataset
