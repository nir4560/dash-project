from sklearn.metrics import confusion_matrix
import pickle
from xgboost import XGBClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)

bst = XGBClassifier(max_depth=1, silent=True, objective='multi:softprob')
bst.fit(X_train, y_train)
predictions = bst.predict(X_test)

with open("./data/model.txt", "rb") as f:
    model = pickle.loads(f.read())
calculated_confusion_matrix = confusion_matrix(y_test, predictions)
