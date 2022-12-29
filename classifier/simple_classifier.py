from classifier.data_utils import *
from sklearn.model_selection import train_test_split


DATA_PATH = "data/reviews_Video_Games_5.json.gz"
data = mark_positive(read_reviews(DATA_PATH, max_lines=10000))
y = data.pop("target")
X = data
X_train, X_test, y_train, y_test = train_test_split(X.index, y, test_size=0.2)
