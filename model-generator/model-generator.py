import warnings
import pandas as pd
import numpy as np

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from numpy import mean

# ignore all warnings

df1 = pd.read_csv('history_data.csv')
df = df1[['Maximum Temperature','Minimum Temperature','Temperature','Relative Humidity','Conditions']]

df.replace("Rain, Partially cloudy",1,inplace=True)
df.replace("Clear",0,inplace=True)
df.replace("Rain",1,inplace=True)
df.replace("Partially cloudy",0,inplace=True)


col_names = df.columns



df.count().sort_values()


df = df1.drop(columns=['Name','Date time','Minimum Temperature','Maximum Temperature'
,'Wind Chill'	,'Heat Index',	'Precipitation'	,'Snow',	'Snow Depth'	,'Wind Speed'	,'Wind Direction',	'Wind Gust'	,'Visibility'	,'Cloud Cover'],axis=1)


#df.shape


df = df.dropna()



from sklearn import preprocessing

numerical = [var for var in df.columns if df[var].dtype=='float64']

for col in numerical:
    df[col] = preprocessing.scale(df[col])
    

# scipy is not necessary here since we have already scaled our data but provides an alternative way to scale data
from scipy import stats

z = np.abs(stats.zscore(df._get_numeric_data()))

df= df[(z < 3).all(axis = 1 )]


categorical = [var for var in df.columns if df[var].dtype=='object']




from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# set X to all features
X = df.loc[:,df.columns!='Conditions']
# set y to our target RainTomorrow
y = df.Conditions
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


logReg = LogisticRegression()
logReg.fit(X_train,y_train)



cv = KFold(n_splits=10, random_state=1, shuffle=True)

scores = cross_val_score(logReg, X, y, scoring='accuracy', cv=cv)
average_score = mean(scores)

print('Overall Accuracy:', average_score)

print(logReg.predict(X_test[0:50]))



import pickle
file = "model2.model"
pickle.dump(logReg,open(file,'wb'))



loaded_model = pickle.load(open(file, 'rb'))
result = loaded_model.predict([[50,20]])
print(X_test)
print(result)

