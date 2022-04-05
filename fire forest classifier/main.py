import pandas as pd
df = pd.read_csv('forestfires.csv')
# print(df.head())
df.month.replace(('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'),(1,2,3,4,5,6,7,8,9,10,11,12), inplace=True)
df.day.replace(('mon','tue','wed','thu','fri','sat','sun'),(1,2,3,4,5,6,7), inplace=True)
# print(df.head())
df['area'].values[df['area'].values > 0] = 1
df = df.rename(columns={'area': 'label'})
print(df.head())
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
scaler.fit(df.drop('label',axis=1))
scaled_features = scaler.transform(df.drop('label',axis=1))
df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1])

X = df_feat
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.30,random_state=101)

model = LogisticRegression(solver='liblinear')
model.fit(X_train,y_train)
predictions = model.predict(X_test)
from sklearn import metrics
model.score(X_train,y_train)
print("Accuracy:",metrics.accuracy_score(y_test, predictions))
print("Precision:",metrics.precision_score(y_test, predictions))
print("Recall:",metrics.recall_score(y_test, predictions))

from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from yellowbrick.model_selection import CVScores

def make_cross_validation(model, X, y):
    # prepare the cross-validation procedure
    cv = KFold(n_splits=10, random_state=1, shuffle=True)
    # evaluate model
    scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
    visualizer = CVScores(model, cv=cv, scoring='accuracy')
    # Fit the data to the visualizer
    visualizer.fit(X, y)    
    # Display the visualizer
    visualizer.show()
    # Return the scores of the cross validation
    return scores

make_cross_validation(model, X, y)