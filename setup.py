from setuptools import setup, find_packages

__version__ = "0.1.2"
__author__ = "Tomáš Mikula"
__email__ = "mail@tomasmikula.cz"

setup(
    name="dutch_concepts",
    version=__version__,
    description="",
    long_description="",
    url="https://github.com/mikulatomas/dutch-concepts",
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
    ],
    classifiers=["Development Status :: 1 - Planning"],
)
