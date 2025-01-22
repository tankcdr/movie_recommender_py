# Movie Recommender Experiment

Uses tensorflow to create a movie recommender.
...more to be added, currently in the data engineering phase

## Scripts

| name            | what it does                                                                                               |
| --------------- | ---------------------------------------------------------------------------------------------------------- |
| prepare_data.py | Merges the three raw data files, enriches the dataset, and creates the `data/movies_transformed.csv` file. |

## Dependency Installation

### MacOS

I'm using `conda` and followed these steps:

```
conda install -c apple tensflow-deps
pip install -r requirements.txt
```

## Data

Data is contained in the data directory.

**Raw data:** these are the files containing the base data:

- `movies.csv`
- `users.csv`
- `ratings.csv`

**Metadata:** the `enum.md` documents the catagorical features used in the data.
