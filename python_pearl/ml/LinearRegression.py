#Import Library
#Import other necessary libraries like pandas, numpy...
from sklearn import linear_model
import numpy as np
#Load Train and Test datasets
#Identify feature and response variable(s) and values must be numeric and numpy arrays
# x_train=input_variables_values_training_datasets
# y_train=target_variables_values_training_datasets
# x_test=input_variables_values_test_datasets

# x_train=np.array([1,2,3,4,5,6,7])
# y_train=np.array([2,4,6,8,10,12,14])
x_train=np.array((999,1))
y_train=np.array((999,1))
x_test=np.array([8,9,10,11])
 
# Create linear regression object
linear = linear_model.LinearRegression()
 
# Train the model using the training sets and check score
linear.fit(x_train, y_train)
linear.score(x_train, y_train)

# regr = LinearRegression()
# regr.fit(df2.iloc[1:1000, 5].values, df2.iloc[1:1000, 2].values)
 
#Equation coefficient and Intercept
print('Coefficient: n', linear.coef_)
print('Intercept: n', linear.intercept_)
 
#Predict Output
predicted= linear.predict(x_test)



#Import Library
from sklearn.linear_model import LogisticRegression
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create logistic regression object
model = LogisticRegression()
 
# Train the model using the training sets and check score
model.fit(X, y)
model.score(X, y)
 
#Equation coefficient and Intercept
print('Coefficient: n', model.coef_)
print('Intercept: n', model.intercept_)
 
#Predict Output
predicted= model.predict(x_test)









#Import Library
#Import other necessary libraries like pandas, numpy...
from sklearn import tree
 
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create tree object 
model = tree.DecisionTreeClassifier(criterion='gini') 
# for classification, here you can change the algorithm as gini or entropy (information gain) by default it is gini  
 
# model = tree.DecisionTreeRegressor() for regression
# Train the model using the training sets and check score
model.fit(X, y)
model.score(X, y)
 
#Predict Output
predicted= model.predict(x_test)



#Import Library
from sklearn import svm
 
#Assumed you have, X (predic
tor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create SVM classification object 
model = svm.svc() 
# there is various option associated with it, this is simple for classification. You can refer link, for mo# re detail.
# Train the model using the training sets and check score
model.fit(X, y)
model.score(X, y)
 
#Predict Output
predicted= model.predict(x_test)





#Import Library
from sklearn.naive_bayes import GaussianNB
 
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create SVM classification object model = GaussianNB() # there is other distribution for multinomial classes like Bernoulli Naive Bayes, Refer link
# Train the model using the training sets and check score
model.fit(X, y)
 
#Predict Output
predicted= model.predict(x_test)







#Import Library
from sklearn.neighbors import KNeighborsClassifier
 
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create KNeighbors classifier object model 
KNeighborsClassifier(n_neighbors=6) 
# default value for n_neighbors is 5
 
# Train the model using the training sets and check score
model.fit(X, y)
 
#Predict Output
predicted= model.predict(x_test)




#Import Library
from sklearn.cluster import KMeans
 
#Assumed you have, X (attributes) for training data set and x_test(attributes) of test_dataset
# Create KNeighbors classifier object model 
k_means = KMeans(n_clusters=3, random_state=0)
 
# Train the model using the training sets and check score
model.fit(X)
 
#Predict Output
predicted= model.predict(x_test)






#Import Library
from sklearn.ensemble import RandomForestClassifier
 
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create Random Forest object
model= RandomForestClassifier()
 
# Train the model using the training sets and check score
model.fit(X, y)
 
#Predict Output
predicted= model.predict(x_test)





#Import Library
from sklearn import decomposition
 
#Assumed you have training and test data set as train and test
# Create PCA obeject pca= decomposition.PCA(n_components=k) #default value of k =min(n_sample, n_features)
# For Factor analysis
#fa= decomposition.FactorAnalysis()
# Reduced the dimension of training dataset using PCA
train_reduced = pca.fit_transform(train)
 
#Reduced the dimension of test dataset
test_reduced = pca.transform(test)
 
#For more detail on this, please refer  this link.




#Import Library
from sklearn.ensemble import GradientBoostingClassifier
 
#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create Gradient Boosting Classifier object
model= GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
 
# Train the model using the training sets and check score
model.fit(X, y)
 
#Predict Output
predicted= model.predict(x_test)



















