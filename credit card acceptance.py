#### Loading Modules

# loading neccessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

#### Loading Data

# loading the data
data = pd.read_csv("C:/Users/HP/Desktop/mll/ML Batch/credit_card.csv")
data.head(10)

#Observing the shape of the dataframe.
data.shape

#  information of the whole dataset
data.info()

#### Plots

#plotting heatmaps to see if there exists any null value in the dataframe

sns.heatmap(data.isnull(),cbar=True,cmap='BuPu')
plt.title("Heat Map for null values")

#plotting the countplot to see how many people has the card

sns.set_style('whitegrid')
sns.countplot(x='card',data=data,palette='Blues')
plt.title("Count plot for card")

#countplot is a histogram or a bar graph for some categorical area


sns.countplot(x='card',hue='selfemp',data=data,palette='mako')
plt.title("Count plot for card on basis of self emp")

# distplot is also a histogram like the countplot
# distplot for age
sns.distplot(data['age'],kde=True,color='red',bins=10)
plt.title("Distplot for age")

# distplot for income

sns.distplot(data['income'],kde=True,color='green',bins=10)
plt.title("Distplot for Income")

#  boxplots: measure of how well distributed the data in the dataset
#            the graph represents the minimum,maximum,median,
#            first quartile, 3rd quartile iin the dataset.

plt.figure(figsize=(9,3))
sns.boxplot(x='card',y='dependents',data=data,palette='winter')
plt.title("Boxplots for dependents vs card")

#     scatterplot= is a plot that shows the data as a collection of points
#                  the position of a poinyt depends on its two dimensional value   





sns.scatterplot(x="age", y="reports", hue="card", data=data)
plt.title("Scatter plot between reports and age on basis of card")

sns.lmplot('age','income',data=data,hue='card',fit_reg=True)
plt.title("scatter plot with regresson line for income and age")

g=sns.PairGrid(data,hue="card")
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter)
plt.legend()

#### Organising Data

# replacing the values of the column of card (yes,no) with (credit_yes,credit_no)
# replacing the values of the column owner (yes,no) with (owner_yes,owner_no)
# replacing the values of the column selfemp (yes,no) with (self_emp_yes,self_emp_no)

data.card.replace(['yes','no'],['credit_yes','credit_no'],inplace=True)
data.owner.replace(['yes','no'],['owner_yes','owner_no'],inplace=True)
data.selfemp.replace(['yes','no'],['self_emp_yes','self_emp_no'],inplace=True)
data.head()

## Convert categorical variable into dummy/indicator variables
# creating dummy of the column card,owner and selfemp and replacing the categorical(no,yes) data 
# to numerical(0,1)

Card=pd.get_dummies(data['card'],drop_first=True)
Owner=pd.get_dummies(data['owner'],drop_first=True)
self_emp=pd.get_dummies(data['selfemp'],drop_first=True)
print(Card.head())
print(Owner.head())
print(self_emp.head())

data.drop(['card','owner','selfemp'],inplace=True,axis=1)
data.head()

data=pd.concat([data,Card,Owner,self_emp],axis=1)
data.head()

data.drop(['dependents'],axis=1,inplace=True)
data.head()

#### Co-Relations and plots between different attributes :

# correlation heatmap between all the feature attributes
corr = data.corr()
plt.figure(figsize=(12,8))
sns.heatmap(corr, annot=True, annot_kws={"size": 12})
plt.title("Heat Map showing correlation between all attributes")

# Scatter Pairplot between all the attributes
sns.pairplot(data, kind ='scatter')

# Pairplot showing regression line between all attributes
sns.pairplot(data, kind = 'reg')
plt.show()

# exploratory analysis
def draw_histograms(dataframe, features, rows, cols):
    fig=plt.figure(figsize=(20,20))
    plt.title("Exploratory Analysis")
    for i, feature in enumerate(features):
        ax=fig.add_subplot(rows,cols,i+1)
        dataframe[feature].hist(bins=20,ax=ax,facecolor='midnightblue')
        ax.set_title(feature+" Distribution",color='DarkRed')
        
    fig.tight_layout()  
    plt.show()
draw_histograms(data,data.columns,6,2)

# loading libraries to create train and test set
from sklearn.model_selection import train_test_split
# dividing the training and test set randomly into 7:3 ratio
x_train,x_test,y_train,y_test=train_test_split(data.drop('credit_yes',axis=1),data['credit_yes'],train_size=0.7,random_state=16)
# showing length of train and test data
print("No. of Train rows -> ",len(y_train))
print("No. of Test rows -> ",len(y_test))

## K-NN Classifier

# K-NN for Classification using Scikit-learn
#Let's create numpy arrays for features and target
X = data.drop('credit_yes',axis=1).values
Y = data['credit_yes'].values

"""
Our data has both numerical and Categorial Data and the Scale of all the features are not similar,
As a result features with larger values will have more impact on the outcome and the features
with small values will be neglected.
This can be bad, because a variable having larger values doesn't necessarily make it better at
predicting what rows are important.
"""
# To overcome this problem we will normalize the data using the scalar facility of sklearn preprocessing
#module.
#Importing preprocessing module
from sklearn.preprocessing import StandardScaler
# Standardize Data
# Create standardizer
standardizer = StandardScaler()

# Standardize features
normalized_x = standardizer.fit_transform(X)
print (normalized_x)

#### Creating Training and Test Set

#Let's split the data randomly into training and test set.
#We will fit/train a classifier on the training set and make predictions
#on the test set. Then we will compare the predictions with the known labels.
#Scikit-learn provides facility to split data into train and test set using 
#train_test_split method.
#Importing the train_test_split method from Scikit-learn.
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(normalized_x,Y,test_size=0.3,random_state=16, stratify=Y)

#### Selecting the best Value of K

#Let's create a classifier using k-Nearest Neighbors algorithm.
#Importing KNeighborsClassifier from sklearn.
from sklearn.neighbors import KNeighborsClassifier
#First let us first observe the accuracies for different values of k.
#Setup arrays to store training and test accuracies
neighbors = np.arange(1,9)
train_accuracy =np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

for i,k in enumerate(neighbors):
    #Setup a knn classifier with k neighbors
    knn = KNeighborsClassifier(n_neighbors=k)
    
    #Fit the model
    knn.fit(X_train, Y_train)
    
    #Compute accuracy on the training set
    train_accuracy[i] = knn.score(X_train, Y_train)
    
    #Compute accuracy on the test set
    test_accuracy[i] = knn.score(X_test, Y_test) 

#### Generate plot of Accuracy Vs Number of neighbors for Training and Testing Data

#Generate plot
plt.title('K - number of neighbors')
plt.plot(neighbors, test_accuracy, label='Testing Accuracy')
plt.plot(neighbors, train_accuracy, label='Training accuracy')
plt.legend()
plt.xlabel('Number of neighbors')
plt.ylabel('Accuracy')
plt.show()

#### We can observe above that we get maximum testing accuracy for k=6. So lets create a KNeighborsClassifier with number of neighbors as 6.

#Setup a knn classifier with k neighbors
knn = KNeighborsClassifier(n_neighbors=6)

#Fit the model
knn.fit(X_train,Y_train)

#let us get the predictions using the classifier we had fit above
Y_pred = knn.predict(X_test)

#### Accuracy Test

#Get accuracy
knn_score=knn.score(X_test,Y_test)
knn_score

#### Accuracy Obtained from the model, trained using the created train and test data set is 87%. 

#import confusion_matrix
from sklearn.metrics import confusion_matrix
con_df=confusion_matrix(Y_test,Y_pred)
con_df

#                 predicted     
# actual    class-0      class-1
# class-0      TN           FP   
# class-1      FN           TP

##### Considering confusion matrix above:
##### True negative = 57
##### False positive = 32
##### False negative= 16
##### True postive = 291

#### Confusion Matrix

pd.crosstab(Y_test, Y_pred, rownames=['True'], colnames=['Predicted'], margins=True)

plt.figure(figsize = (8,5))
sns.heatmap(con_df, annot=True,fmt='d',cmap="summer")
plt.title("K-NN Confusion Matrix Heatmap")

#### Classification Report

# classification report visualiser dislays the precision,recall etc.
# Precision = TP/(TP + FP)
# Precision measures how many of the samples 
# predicted as positive are actually positive
# Precision is also known as positive predictive value (PPV)

# Recall = TP/(TP + FN)
# measures how many of the positive samples are captured
# by the positive predictions:
# Other names for recall are sensitivity, hit rate,
# or true positive rate (TPR).

#import classification_report
from sklearn.metrics import classification_report
print(classification_report(Y_test,Y_pred))

#### ROC Curve

# ROC is a plot of the true positive rate against the false positive rate 
# for the different possible cutpoints of a diagnostic test.
from sklearn.metrics import roc_curve
y_pred_proba = knn.predict_proba(X_test)[:,1]
fpr, tpr, thresholds = roc_curve(Y_test, y_pred_proba)
plt.plot([0,1],[0,1],'k--')
plt.plot(fpr,tpr, label='Knn')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Knn(n_neighbors=6) ROC curve')
plt.show()

#### Cross Validation

#import GridSearchCV
from sklearn.model_selection import GridSearchCV
#In case of classifier like knn the parameter to be tuned is n_neighbors
param_grid = {'n_neighbors':np.arange(1,50)}

knn = KNeighborsClassifier()
knn_cv= GridSearchCV(knn,param_grid,cv=5)
knn_cv.fit(X_train,Y_train)

knn_cv.best_score_

knn_cv.best_params_



## Naive Baye's Classifier

# Naive Bayes classifiers are a family of simple "probabilistic classifiers"
# based on applying Bayes' theorem 
# with strong (naive) independence assumptions between the features
"""
p(class|data) = [p(data|class)*p(class)]/p(data)
where:
 *class is particular class(e.g. male,female)
 *data is an observation data(e.g. height,weight,foot_size)
 *p(class|data) is called the posterior
 *p(data|class) is called the likelihood
 *p(class) is called the prior
 *p(data) is called the marginal probability

N:B : Baye's Theorem
"""
print("")

# In this case gaussian model of Naive Bayes is used.
# Gaussian: It is used in classification and it assumes that features follow a normal distribution.

# loading library for Gaussian naive bayes classifier

from sklearn.naive_bayes import GaussianNB

# implementing  GaussianNaive Bayes 

GausNB = GaussianNB()
nb=GausNB.fit(x_train,y_train)
y_expect = y_test
nb_pred = GausNB.predict(x_test)

#### Accuracy Test

# to check the accuracy of our model
nb_score=nb.score(x_test,y_test)
nb_score

#### Confusion Matrix

#creating confusion matrix to evaluate the accuracy of the prediction

con_df=pd.DataFrame(confusion_matrix(y_test,nb_pred),
                   columns=['predicted value'+str(class_name) for class_name in [0,1]],
                           index=['actual value' + str(class_name) for class_name in[0,1]])
con_df

#                 predicted     
# actual    class-0      class-1
# class-0      TN           FP   
# class-1      FN           TP

plt.figure(figsize = (8,5))
sns.heatmap(con_df, annot=True,fmt='d',cmap="summer")
plt.title("Naive Baye's Confusion Matrix Heatmap")

#### Classification Report

# classification report visualiser dislays the precision,recall etc.
# Precision = TP/(TP + FP)
# Precision measures how many of the samples 
# predicted as positive are actually positive
# Precision is also known as positive predictive value (PPV)

# Recall = TP/(TP + FN)
# measures how many of the positive samples are captured
# by the positive predictions:
# Other names for recall are sensitivity, hit rate,
# or true positive rate (TPR).

# loading libraries analysis of result
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# classification report
print(classification_report(y_test,nb_pred))

# ROC is a plot of the true positive rate against the false positive rate 
# for the different possible cutpoints of a diagnostic test.
from sklearn.metrics import roc_curve
y_pred_proba = nb.predict_proba(x_test)[:,1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot([0,1],[0,1],'k--')
plt.plot(fpr,tpr, label='nb')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title("Naive Baye's ROC curve")
plt.show()

## Logistic Regression

# Logistic regression is a statistical method for analyzing a 
# dataset in which there are one or more independent variables
# that determine an outcome. The outcome is measured with a 
# dichotomous variable (in which there are only two possible
# outcomes).
# loading library for logistic regression

from sklearn.linear_model import LogisticRegression

# implementing logistic regression

lm=LogisticRegression()
# training the model
lr=lm.fit(x_train,y_train)
lr_pred=lm.predict(x_test)

#### Accuracy Test

lr_score=lr.score(x_test,y_test)
lr_score

#### Confusion Matrix

#creating confusion matrix to evaluate the accuracy of the prediction

con_df=pd.DataFrame(confusion_matrix(y_test,lr_pred),
                   columns=['predicted value'+str(class_name) for class_name in [0,1]],
                           index=['actual value' + str(class_name) for class_name in[0,1]])
con_df

plt.figure(figsize = (8,5))
sns.heatmap(con_df, annot=True,fmt='d',cmap="summer")
plt.title("Logistic Regression Confusion Matrix Heatmap")

#### Classification Report

# loading libraries analysis of result
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# classification report
print(classification_report(y_test,lr_pred))

#### ROC Curve

# ROC is a plot of the true positive rate against the false positive rate 
# for the different possible cutpoints of a diagnostic test.
from sklearn.metrics import roc_curve
y_pred_proba = lm.predict_proba(x_test)[:,1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot([0,1],[0,1],'k--')
plt.plot(fpr,tpr, label='lr')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Logistic Regression ROC curve')
plt.show()

## Desicion Tree

# A decision tree is a decision support tool that uses a tree-like model
# of decisions and their possible consequences, including chance event outcomes
# resource costs, and utility.
# It is one way to display an algorithm that only contains conditional control statements.
# loading neccessary libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

### Assigning Decision Tree Classifier in Train_gini variable

dt=DecisionTreeClassifier(criterion='gini',random_state=101,min_samples_leaf=4,max_depth=5)

# training the model
dt.fit(x_train,y_train)
dt_pred=dt.predict(x_test)

### Accuracy Score

dt_score=dt.score(x_test,y_test)
dt_score

### Confusion Matrix

con_df=pd.DataFrame(confusion_matrix(y_test,dt_pred),
                   columns=['predicted value'+str(class_name) for class_name in [0,1]],
                           index=['actual value' + str(class_name) for class_name in[0,1]])
con_df

plt.figure(figsize = (8,5))
sns.heatmap(con_df, annot=True,fmt='d',cmap="summer")
plt.title("Decision Tree Confusion Matrix Heatmap")

### Classification Report

print(classification_report(y_test,dt_pred))

#### ROC Curve

# ROC is a plot of the true positive rate against the false positive rate 
# for the different possible cutpoints of a diagnostic test.
from sklearn.metrics import roc_curve
y_pred_proba = dt.predict_proba(x_test)[:,1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot([0,1],[0,1],'k--')
plt.plot(fpr,tpr, label='nb')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title("Decision Tree ROC curve")
plt.show()

### output txt file 

with open("dt1.txt", "w") as f:
    f = tree.export_graphviz(dt, out_file=f)

# This step create a text file dt_train_gini.txt in the default folder.
#We can give full path as well.
#We can copy the context of this text file and put into the box on 
# http://www.webgraphviz.com/

### Comparision between accuracy of all Models

plt.style.use('fivethirtyeight')
figsize=(8, 6)

# Dataframe to hold the results
model_comparison = pd.DataFrame({'model': ['K-NN','Logistic Regression',
                                           'Naive Bayes', 'Decision Tree'],
                                 'score': [knn_score, lr_score,nb_score,dt_score]})

# Horizontal bar chart of test mae
model_comparison.sort_values('score', ascending = True).plot(x = 'model', y = 'score', kind = 'barh',
                                                           color = 'red', edgecolor = 'black')

# Plot formatting
plt.ylabel(''); plt.yticks(size = 14); plt.xlabel('Accuracy'); plt.xticks(size = 14)
plt.title('Model Comparison on Score', size = 20);

