# MortgageDefault

This Flask application utilizes IBM's Watson Machine Learning APIs to make predictions against a deployed machine learning
model created using Spark MLlib. The application provides the option to store the prediction in a backend database, which can then
queried to analyze mortgage application patterns.

The model utilizes a Decision Tree classifier to predict whether a mortgage loan will default based on a number of features
regarding the loan and loan applicant.

An instance of the application running on IBM Bluemix can be accessed at http://mortgagedefault.mybluemix.net/
