import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


def r2_score(y, y_hat):
    y_bar = y.mean()
    ss_tot = ((y - y_bar) ** 2).sum()
    ss_res = ((y - y_hat) ** 2).sum()
    return 1 - (ss_res / ss_tot)


def scalerselector_regression(X, y):
    # split into train and test sets

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
    # summarize
    print('Train Data Size', X_train.shape, y_train.shape)
    print('Test Data Size', X_test.shape, y_test.shape)
    print('\n')

    col_list = list(X.columns.values)

    # fit scaler on training data
    norm = MinMaxScaler().fit(X_train)

    # transform training data
    X_train_norm = norm.transform(X_train)

    # transform testing dataabs
    X_test_norm = norm.transform(X_test)

    # copy of datasets
    X_train_stand = X_train.copy()
    X_test_stand = X_test.copy()

    # numerical features

    # apply standardization on numerical features
    for i in col_list:
        # fit on training data column
        scale = StandardScaler().fit(X_train_stand[[i]])

        # transform the training data column
        X_train_stand[i] = scale.transform(X_train_stand[[i]])

        # transform the testing data column
        X_test_stand[i] = scale.transform(X_test_stand[[i]])

    # copy of datasets
    X_train_rob = X_train.copy()
    X_test_rob = X_test.copy()

    # numerical features

    # apply standardization on numerical features
    for i in col_list:
        # fit on training data column
        scale = RobustScaler().fit(X_train_rob[[i]])

        # transform the training data column
        X_train_rob[i] = scale.transform(X_train_rob[[i]])

        # transform the testing data column
        X_test_rob[i] = scale.transform(X_test_rob[[i]])

    # LR
    LR = LinearRegression()

    rmse_LR = []
    r2_LR = []

    # raw, normalized and standardized training and testing data
    trainX = [X_train, X_train_norm, X_train_stand, X_train_rob]
    testX = [X_test, X_test_norm, X_test_stand, X_test_rob]

    # model fitting and measuring RMSE
    for i in range(len(trainX)):
        # fit
        LR.fit(trainX[i], y_train)
        # predict
        pred = LR.predict(testX[i])
        # RMSE
        rmse_LR.append(rmse(y_test, pred))
        # rmse_LR.append(np.sqrt(mean_squared_error(y_test,pred)))
        # r2
        r2_LR.append(r2_score(y_test, pred))

    # visualizing the result
    df_LR = pd.DataFrame({'RMSE': rmse_LR, 'R2': r2_LR},
                         index=['Original', 'Normalized', 'Standardized', 'RobustScaler'])
    print("\nLinear Regression Results\n", df_LR)
    print('\n')

    # rfr = RandomForestRegressor(n_estimators = 100, max_depth = 5, min_samples_leaf= 5, max_features = 'sqrt')  # using GridSearch
    rfr = RandomForestRegressor()

    rmse_rfr = []
    r2_rfr = []

    # raw, normalized and standardized training and testing data
    trainX = [X_train, X_train_norm, X_train_stand, X_train_rob]
    testX = [X_test, X_test_norm, X_test_stand, X_test_rob]

    # model fitting and measuring RMSE
    for i in range(len(trainX)):
        # fit
        rfr.fit(trainX[i], y_train)
        # predict
        pred = rfr.predict(testX[i])
        # RMSE
        rmse_rfr.append(rmse(y_test, pred))
        # rmse_rfr.append(np.sqrt(mean_squared_error(y_test,pred)))
        # R2
        r2_rfr.append(r2_score(y_test, pred))

    # visualizing the result
    df_rfr = pd.DataFrame({'RMSE': rmse_rfr, 'R2': r2_rfr, },
                          index=['Original', 'Normalized', 'Standardized', 'RobustScaler'])
    print("\nRandom Forest Results\n", df_rfr)
    print('\n')


    svr = SVR(kernel='rbf')

    rmse_svr = []
    r2_svr = []

    # raw, normalized and standardized training and testing data
    trainX = [X_train, X_train_norm, X_train_stand, X_train_rob]
    testX = [X_test, X_test_norm, X_test_stand, X_test_rob]

    # model fitting and measuring RMSE
    for i in range(len(trainX)):
        # fit
        svr.fit(trainX[i], y_train)
        # predict
        pred = svr.predict(testX[i])
        # RMSE
        rmse_svr.append(rmse(y_test, pred))
        # rmse_svr.append(np.sqrt(mean_squared_error(y_test,pred)))
        # R2
        r2_svr.append(r2_score(y_test, pred))

    # visualizing the result
    print("\nSVR Results\n")
    df_svr = pd.DataFrame({'RMSE': rmse_svr, 'R2': r2_svr},
                          index=['Original', 'Normalized', 'Standardized', 'RobustScaler'])
    print(df_svr)
    print('\n')

# python setup.py sdist bdist_wheel
# pip install -e C:\Users\neloy\OneDrive\GitHub\data-scaler
# twine upload dist/*

