from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np



def baseline_regression(data,raw_data):


    lr = LinearRegression()
    x = np.array(data['Values']['x']).reshape(-1,1)
    y = np.array(data['Values']['y']).reshape(-1,1)

    lr.fit(x, y)
    ypred = lr.predict(x)
    return lr.coef_,ypred

def baseline_correction_function(data,bsl_coefficient):

    corrected_current_value = []

    for index, row in data.iterrows():


        corrected_y = row['WE(1).Current (A)'] - row['Time (s)'] * bsl_coefficient
        corrected_current_value.append(corrected_y)


    corrected_dataframe = pd.DataFrame({'Time (s)':data['Time (s)'],'Corrected Current (A)':np.array(corrected_current_value).flatten()})
    return corrected_dataframe







def calibration_mean(data_selection) -> pd.DataFrame:
    data = data_selection

    data['Concentration'] = pd.to_numeric(data['Concentration'])
    df = data.groupby('Concentration', as_index=False).mean()
    df = df.rename(columns={'Concentration': 'Concentration Mean', 'Time': 'Time Mean', 'Signal': 'Signal Mean'})


    return df


def calibration_regression(data):
    calib_mean = calibration_mean(data_selection=data)

    lr = LinearRegression()
    x = np.array(calib_mean['Concentration Mean']).reshape((-1, 1))
    y = np.array(calib_mean['Signal Mean']).reshape((-1, 1))

    lr.fit(x, y)
    ypred = lr.predict(x)


    return lr.coef_, lr.intercept_,ypred


def signal_to_concentration(regression_parameters,truncated_data):

    a, b, ypred = regression_parameters
    col_names = [col for col in truncated_data.columns]

    h2o2_y = [float((i -b) / a) for i in truncated_data[col_names[1]]]


    return truncated_data[col_names[0]], h2o2_y
