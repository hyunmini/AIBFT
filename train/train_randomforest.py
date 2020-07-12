import numpy as np
import matplotlib.pyplot as plt
import pickle 

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix 

# data preprocessing
print("[*] Start : RandomForest Classification")

datasets = np.loadtxt('output/features_20190816.csv', delimiter=',',skiprows=1)
xy_data = datasets   # exclude header
train_set, test_set = train_test_split(xy_data, test_size=6000, random_state=93)   
print('Training Length : ', len(train_set), 'Test Length : ', len(test_set))

x_train_data = train_set[:,1:]
y_train_data = train_set[:,:1].reshape(-1,)

# 8 x 8
x_test_data = test_set[:,1:]
y_test_data = test_set[:,:1].reshape(-1,)

print("[x_train_data]",x_train_data.shape)
print("[y_train_data]", y_train_data.shape)
print("[x_test_data]", x_test_data.shape)
print("[y_test_data]", y_test_data.shape)


rf = RandomForestClassifier(n_estimators=10,max_features=20)
classifier = rf.fit(x_train_data, y_train_data)

y_pred = classifier.predict_proba(x_test_data)

for yy in y_pred:
	print(yy)
	
# model save
pickle.dump(rf, open('rf.model', 'wb'))