# dutch-concepts
Cleaned version of *Exemplar by feature applicability matrices and other Dutch normative data for semantic concept* dataset [1].

## Python wrapper
For easier manipulation, you can download data as Python wrapper:

```bash
pip3 install git+https://github.com/mikulatomas/dutch-concepts.git
```

## Example

```python
import dutch_concepts as dc

data = dc.DutchConcepts()

# typicality ratings for birds
data.exemplar_judgements.typicality_ratings[dc.Category.BIRD]

# category based features for birds
data.features[dc.FeatureType.CATEGORY].category[dc.Category.BIRD]
```

## Original dataset
[1] De Deyne, Simon, et al. "Exemplar by feature applicability matrices and other Dutch normative data for semantic concepts." Behavior research methods 40.4 (2008): 1030-1048.

Original data can be downloaded here: https://link.springer.com/article/10.3758/BRM.40.4.1030
