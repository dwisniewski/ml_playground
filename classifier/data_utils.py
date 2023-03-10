import gzip
import json
import pandas as pd


def read_reviews(path: str, max_lines: int = 1000) -> pd.DataFrame:
    """Read {max_lines} from gzipped file located in {path} and
       transform them into a Pandas DataFrame object.

    Args:
        path (str):  path to a file with reviews
        max_lines (int): maximum number of lines to read (default is 1000)

    Returns:
        pd.DataFrame: DataFrame representation of read data.
    """
    with gzip.open(path, "r") as f:
        read_data = []
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            read_data.append(json.loads(line))
        return pd.DataFrame.from_records(read_data)


def mark_positive(dataframe: pd.DataFrame) -> pd.DataFrame:
    def is_positive(stars: float) -> bool:
        return True if stars >= 4.0 else False

    dataframe["target"] = dataframe["overall"].apply(lambda x: is_positive(x))
    return dataframe


if __name__ == "__main__":
    data = read_reviews("data/reviews_Video_Games_5.json.gz", max_lines=1)
    data = mark_positive(data)
    print(data)
