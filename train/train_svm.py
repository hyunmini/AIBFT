import numpy as np

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix 
from sklearn.svm import SVC  
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
np.set_printoptions(linewidth=200)


def load_dataset():

    datasets = np.loadtxt('output/features_20190812.csv', delimiter=',', skiprows=1, unpack=True)

    xy_data = datasets.T

    train_set, test_set = train_test_split(xy_data, test_size=6000, random_state=93)
    print('Training Length : ', len(train_set), 'Test Length : ', len(test_set))

    x_train_data = train_set[:,1:]
    y_train_data = train_set[:,[0]]

    x_test_data = test_set[:,1:]
    y_test_data = test_set[:,[0]]

    return x_train_data, y_train_data, x_test_data, y_test_data




load_dataset()


x_train_data, y_train_data, x_test_data, y_test_data = load_dataset()

svclassifier = SVC(kernel='linear')  
svclassifier.fit(x_train_data, y_train_data)

y_pred = svclassifier.predict(x_test_data)

print(confusion_matrix(y_test_data,y_pred))
print(classification_report(y_test_data,y_pred))
