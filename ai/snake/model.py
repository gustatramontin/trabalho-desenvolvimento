from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import pandas as pd
import numpy as np

import pickle

data = pd.read_csv('ai/snake/train.csv')
x = np.array(data.drop(['direction', '0x','0y','1x','1y','2x','2y','3x','3y','5x','5y','6x','6y','7x','7y','9x','9y','10x','10y','11x','11y','13x','13y','14x','14y','15x','15y','17x','17y','18x','18y','19x','19y'], 1))
y = np.array(data['direction'])

clf = SVC()

clf.fit(x, y)
acc = clf.score(x, y)

print(acc)

with open("ai/snake/model.pickle", "wb") as f:
    pickle.dump(clf, f)