#!C:\Users\programmer\AppData\Local\Programs\Python\Python37-32\python.exe

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import warnings
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")

data = pd.read_csv("dataset.csv")
data = np.array(data)

X = data[1:, 1:-1]
y = data[1:, -1]
y = y.astype('int')
X = X.astype('float')
#print(X,y)
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25,random_state = 0,shuffle=False)
log_reg =  LogisticRegression()

sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


log_reg.fit(X_train, y_train)


inputt=[float(x) for x in "0.682284 14780 5".split(' ')]
final=[np.array(inputt)]

#print(final)
b = log_reg.predict_proba(final)

y_pred = log_reg.predict(X_test)

#print(b)
#print(y_pred)
accuracy=accuracy_score(y_test,y_pred)
print(accuracy)

pickle.dump(log_reg,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))


