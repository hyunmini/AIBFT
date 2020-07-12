from keras import layers
from keras import models
from keras import metrics
from keras import losses
from keras import optimizers
from keras import datasets              
from keras.utils import np_utils
from keras.layers import Dropout
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import sys,os
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix


# data preprocessing
print("[*] Start")

datasets = np.loadtxt('./output/features_20190816.csv', delimiter=',',skiprows=1)
xy_data = datasets   # exclude header
train_set, test_set = train_test_split(xy_data, test_size=6000, random_state=93)   
print('Training Length : ', len(train_set), 'Test Length : ', len(test_set))

x_train_data = train_set.T[1:]
y_train_data = train_set.T[:1]

x_test_data = test_set.T[1:]
y_test_data = test_set.T[:1]

print("[x_train_data]",x_train_data.shape)
print("[y_train_data]", y_train_data.shape)
print("[x_test_data]", x_test_data.shape)
print("[y_test_data]", y_test_data.shape)

# modeling start
model = models.Sequential()
#============================================================
model.add(layers.Dense(39, activation='relu', input_shape=(39,)))
model.add(Dropout(0.1))
model.add(layers.Dense(40, activation='relu'))
model.add(Dropout(0.2))
model.add(layers.Dense(40, activation='relu'))
model.add(Dropout(0.2))
model.add(layers.Dense(1, activation='sigmoid'))  
#============================================================

# model compile
model.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'])  

hist = model.fit(x_train_data.T,
                    y_train_data.T,
                    epochs=20,
                    batch_size=1024,
                    validation_data = (x_test_data.T, y_test_data.T))


# Confusion Matrix    ####
y_pred_data = model.predict(x_test_data.T)
y_pred_data = [round(x[0]) for x in y_pred_data]
print("## predict data ##")
#print(y_pred_data)

cm = confusion_matrix(y_test_data.T, y_pred_data)
print("## Confusion Matrix ##")
print(cm)

# test
performace_test = model.evaluate(x_test_data.T, y_test_data.T, batch_size=1024)
print('Test Loss and Accuracy ->', performace_test)

# plot
fig, loss_ax = plt.subplots()
acc_ax = loss_ax.twinx()

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')
loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
loss_ax.legend(loc='upper right')

acc_ax.plot(hist.history['acc'], 'b', label='train acc')
acc_ax.plot(hist.history['val_acc'], 'g', label='val acc')
acc_ax.set_ylabel('accuracy')
acc_ax.legend(loc='upper left')

model.save('browser_model.h5')

#plt.show()