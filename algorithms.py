import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor
from dateutil import parser

def mean_absolute_percentage_error(y_true, y_pred):
    _sum = 0
    _count = 0
    _y_max = max(y_true) - min(y_true)
    for index, y in enumerate(y_true):
        if y != 0:
            _sum += abs(y-y_pred[index])/_y_max*100
            _count += 1
    return _sum/_count

def accuracy_percentage(y_true, y_pred):
    _count = 0
    for i in range(len(y_true)):
        if abs(round(y_pred[i]) - y_true[i]) <= 0:
            _count += 1
    return _count/len(y_true)

def get_data(df):
    count = int(len(df)*2/3)
    df_train = df[:count]
    df_test = df[count:]
    np_x_train = np.asarray(df_train[['Hour', 'Carbo', 'GlucoseBefore', 'GlucoseAfter']])
    np_y_train = np.asarray(df_train['Insulin'])
    np_x_test = np.asarray(df_test[['Hour', 'Carbo', 'GlucoseBefore', 'GlucoseAfter']])
    np_y_test = np.asarray(df_test['Insulin'])
    return np_x_train, np_y_train, np_x_test, np_y_test

def get_accuracy(y_true, y_pred):
    return r2_score(y_true, y_pred)

def get_json(name, value, accuracy):
    return {
        'Accuracy': round(accuracy,2),
        'Name' : name,
        'Value': round(value)
    }

def algorithm(model, df, input_dose):
    np_x_train, np_y_train, np_x_test, np_y_test = get_data(df)
    model.fit(np_x_train, np_y_train)
    accuracy = get_accuracy(np_y_test, model.predict(np_x_test))
    model.fit(np.concatenate([np_x_train, np_x_test]), np.concatenate([np_y_train, np_y_test]))
    value = model.predict([input_dose])[0]
    return value, accuracy

algorithms = {
    'Linear' : LinearRegression(),
    'KNN' : KNeighborsRegressor(n_neighbors=5),
    'Tree' : ExtraTreesRegressor(n_estimators=50, max_features ='sqrt'),
    'Forest' : RandomForestRegressor(n_estimators=50, max_features ='sqrt'),
    'Gradient' : GradientBoostingRegressor()
}

def run_algorithms(dose, doses):
    df = json_normalize(doses)
    df['Time'] = list(map(lambda x: parser.parse(str(x)), df['Time']))
    df['Hour'] = list(map(lambda t: t.hour + t.minute/60, df['Time']))
    dose['Time'] = parser.parse(dose['Time'])
    input_dose = [
        dose['Time'].hour + dose['Time'].minute/60,
        dose['Carbo'],
        dose['GlucoseBefore'],
        dose['GlucoseAfter']
    ]
    forecasts = []
    for name, model in algorithms.items():
        value, accuracy = algorithm(model, df, input_dose)
        forecasts.append(get_json(name, value, accuracy))
    forecasts = list(filter(lambda x: x['Value'] >= 0, forecasts))
    forecasts.sort(key=lambda x: x['Accuracy'], reverse=True)
    return forecasts
