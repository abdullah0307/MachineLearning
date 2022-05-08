# # import modules
# from sklearn import datasets
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns
#
# # load data
# wine = datasets.load_wine()
#
# # this dataset has 13 features, we will only choose a subset of these
# df_wine = pd.DataFrame(wine.data, columns=wine.feature_names)
# selected_features = ['alcohol', 'flavanoids', 'color_intensity', 'ash']
#
# # extract the data as numpy arrays of features, X, and target, y
# X = df_wine[selected_features].values
# y = wine.target
#
# wine = pd.concat([pd.DataFrame(X, columns=selected_features), pd.Series(y, name='class')], axis=1)
# sns.pairplot(wine, hue="class", height=2.5)
# plt.show()
#
# iris = datasets.load_iris()
# iris = pd.concat([pd.DataFrame(iris.data, columns=['a', 'b', 'c', 'd']), pd.Series(iris.target, name='species')],
#                  axis=1)
# sns.pairplot(iris, hue="species", height=2.5)
# plt.show()
