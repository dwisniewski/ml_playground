import pytest
from classifier.data_utils import *

def test_size():
    for data_size in [0, 1, 200, 500]:
        data = read_reviews(
            "data/reviews_Video_Games_5.json.gz", max_lines=data_size)
        assert data.shape[0] == data_size

def test_columns():
    data = read_reviews("data/reviews_Video_Games_5.json.gz")
    columns = {'reviewerID', 'asin', 'reviewerName', 'helpful',
               'reviewText', 'overall', 'summary', 'unixReviewTime',
               'reviewTime'}
    data_columns = set([column for column in data.columns])
    assert columns == data_columns