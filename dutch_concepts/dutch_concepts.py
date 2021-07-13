import logging
import os
import urllib.request
import zipfile

from .loaders import load_exemplar_similarity, load_features, load_exemplar_judgements
from .enums import FeatureType

URL = "https://github.com/mikulatomas/dutch-concepts/raw/master/data/dutch_data.zip"


class DutchConcepts:
    def __init__(self, root, language="en"):
        self.root = os.path.abspath(root)

        if language not in ["en", "nl"]:
            raise ValueError("Wrong language only 'en' and 'nl' is supported.")

        self.language = language
        self.dataset_dir = os.path.join(self.root, "dutch_data", language)
        self.zip_file = URL.rsplit("/", 1)[-1]

        
        if not os.path.exists(self.dataset_dir) or not os.listdir(self.dataset_dir):
            logging.info("Downloading dataset.")
            self.__download()
            logging.info("Downloading is done.")
            logging.info("Extracting dataset.")
            self.__extract()
            logging.info("Extracting done.")
        else:
            logging.info("Dataset directory is not empty, skipping download.")

        self.category_features = load_features(self.dataset_dir, FeatureType.CATEGORY)

        self.exemplar_features = load_features(self.dataset_dir, FeatureType.EXEMPLAR)

        self.exemplar_judgements = load_exemplar_judgements(self.dataset_dir)

        self.exemplar_similarities = load_exemplar_similarity(self.dataset_dir)

    def __download(self):
        with urllib.request.urlopen(URL) as f:
            with open(os.path.join(self.root, self.zip_file), "wb") as out_f:
                out_f.write(f.read())

    def __extract(self):
        with zipfile.ZipFile(os.path.join(self.root, self.zip_file), "r") as zip_f:
            zip_f.extractall(self.root)

        logging.info("Removing downloaded ZIP file.")
        os.remove(os.path.join(self.root, self.zip_file))
