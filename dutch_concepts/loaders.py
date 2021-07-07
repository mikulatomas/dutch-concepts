import os
import re

from typing import NamedTuple

import pandas as pd
from glob import glob

from .enums import Category, Domain, FeatureType

EXEMPLAR_FEATURES_JUDGEMENTS_FOLDER = "exemplar_feature_judgments"
CATEGORY_FEATURES_FOLDER = "category_features"
EXEMPLAR_FEATURES_FOLDER = "exemplar_features"
EXEMPLAR_JUDGMENTS_FOLDER = "exemplar_judgments"
PAIRWISE_SIMILARITY_FOLDER = "pairwise_similarities"
RESPONDENTS_FOLDER = "respondents"
FEATURE_FREQUENCY_FOLDER = "feature_generation_frequency"
FEATURE_IMPORTANCE_RATINGS_FOLDER = "feature_importance_ratings"


class ExemplarSimilarityData(NamedTuple):
    category: Category
    mean: pd.DataFrame
    respondents: dict
    name: str

    def __repr__(self):
        return f"ExemplarSimilarityData({self.category})"


class FeaturesDomainData(NamedTuple):
    domain: Domain
    feature_matrix: pd.DataFrame
    feature_matrix_respondents: dict
    feature_frequency: pd.DataFrame
    feature_type: FeatureType
    name: str

    def __repr__(self):
        return f"FeaturesDomainData({self.domain}, {self.feature_type})"


class FeaturesCategoryData(NamedTuple):
    domain: Category
    feature_matrix: pd.DataFrame
    feature_matrix_respondents: dict
    feature_frequency: pd.DataFrame
    feature_importance_ratings: pd.DataFrame
    feature_type: FeatureType
    name: str

    def __repr__(self):
        return f"FeaturesCategoryData({self.domain}, {self.feature_type})"


class ExemplarJudgementsData(NamedTuple):
    type: str
    category: Category
    data: pd.DataFrame
    name: str

    def __repr__(self):
        return f"ExemplarJudgements({self.type}, {self.category})"


class Features(NamedTuple):
    domain: dict
    category: dict
    feature_type: FeatureType

    def __repr__(self):
        return f"Features({self.feature_type})"


class ExemplarJudgements(NamedTuple):
    acquisition_ratings: dict
    associative_strength: dict
    exemplar_generation_frequency: dict
    familiarity_ratings: dict
    goodness_rank_order: dict
    goodness_ratings: dict
    imageability_ratings: dict
    typicality_ratings: dict
    word_frequency: dict

    def __repr__(self):
        return "ExemplarJudgements()"


def load_exemplar_judgements(dataset_folder):
    judgments = [
        "acquisition_ratings",
        "associative_strength",
        "exemplar_generation_frequency",
        "familiarity_ratings",
        "goodness_rank_order",
        "goodness_ratings",
        "imageability_ratings",
        "typicality_ratings",
        "word_frequency",
    ]

    loaded_judgments = []

    for judgment_name in judgments:
        judgment_folder = os.path.join(dataset_folder, EXEMPLAR_JUDGMENTS_FOLDER, judgment_name)

        judgment_dict = {}

        for file in glob(os.path.join(judgment_folder, '*.csv')):
            category = Category.from_str(os.path.basename(file).replace(f"_{judgment_name}.csv", ""))
            
            df = pd.read_csv(file, index_col=0)

            judgment_dict[category] = ExemplarJudgementsData(judgment_name, category, df, os.path.basename(file))
        
        loaded_judgments.append(judgment_dict)

    return ExemplarJudgements(*loaded_judgments)


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
            domain, feature_matrix, respondents, feature_frequency, feature_type, f"{feature_type.value}_features_{domain.value}_domain"
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
            f"{feature_type.value}_features_{category.value}_category"
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
            category, mean_similarities, respondents, f"{category.value}_pairwise_similarities"
        )

    return dataset
