from sklearn.metrics import confusion_matrix
import pickle
from xgboost import XGBClassifier

bst = XGBClassifier(max_depth=1, silent=True, objective='multi:softprob')
bst.fit(X_train, y_train)
predictions = bst.predict(X_test)

with open("./data/model.txt", "rb") as f:
    model = pickle.loads(f.read())
calculated_confusion_matrix = confusion_matrix(y_test, predictions)
