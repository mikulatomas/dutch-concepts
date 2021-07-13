import logging
import os
import urllib.request
import zipfile

from .loaders import load_exemplar_similarity, load_features, load_exemplar_judgements
from .enums import FeatureType

URL = "https://github.com/mikulatomas/dutch-concepts/raw/master/data/dutch_data.zip"


class DutchConcepts:
    def __init__(self, download_dir, language="en"):
        self.download_dir = os.path.abspath(download_dir)

        if language not in ["en", "nl"]:
            raise ValueError("Wrong language only 'en' and 'nl' is supported.")

        self.language = language
        dataset_dir = os.path.join(self.download_dir, "dutch_data", language)
        zip_file = URL.rsplit("/", 1)[-1]
        
        if not os.path.exists(dataset_dir) or not os.listdir(dataset_dir):
            logging.info("Downloading dataset.")
            self.__download(zip_file)
            logging.info("Downloading is done.")
            logging.info("Extracting dataset.")
            self.__extract(zip_file)
            logging.info("Extracting done.")
        else:
            logging.info("Dataset directory is not empty, skipping download.")

        self.category_features = load_features(dataset_dir, FeatureType.CATEGORY)

        self.exemplar_features = load_features(dataset_dir, FeatureType.EXEMPLAR)

        self.exemplar_judgements = load_exemplar_judgements(dataset_dir)

        self.exemplar_similarities = load_exemplar_similarity(dataset_dir)
    
    def __repr__(self):
        return f"DutchConcepts({self.download_dir}, {self.language})"

    def __download(self, zip_file):
        with urllib.request.urlopen(URL) as f:
            with open(os.path.join(self.download_dir, zip_file), "wb") as out_f:
                out_f.write(f.read())

    def __extract(self, zip_file):
        with zipfile.ZipFile(os.path.join(self.download_dir, zip_file), "r") as zip_f:
            zip_f.extractall(self.download_dir)

        logging.info("Removing downloaded ZIP file.")
        os.remove(os.path.join(self.download_dir, zip_file))
