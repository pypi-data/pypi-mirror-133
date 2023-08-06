from timewarpy import datasets, core
from sklearn.preprocessing import MinMaxScaler


def test_UnivariateTS_fit():
    df = datasets.load_energy_data()
    TSprocessor = core.UnivariateTS(1680, 240, scaler=MinMaxScaler)
    TSprocessor.fit(df, 'Appliances')
    assert TSprocessor.scaler.data_max_ is not None


def test_UnivariateTS_transform():
    df = datasets.load_energy_data()
    TSprocessor = core.UnivariateTS(1680, 240, scaler=MinMaxScaler)
    TSprocessor.fit(df, 'Appliances')
    X, y = TSprocessor.transform(df, 'Appliances')
    assert X.shape == (17816, 1680, 1)


def test_UnivariateTS_fit_transform():
    df = datasets.load_energy_data()
    TSprocessor = core.UnivariateTS(1680, 240, scaler=MinMaxScaler)
    X, y = TSprocessor.fit_transform(df, 'Appliances')
    assert X.shape == (17816, 1680, 1)


def test_UnivariateTS_inverse_transform():
    df = datasets.load_energy_data()
    TSprocessor = core.UnivariateTS(1680, 240, scaler=MinMaxScaler)
    X, y = TSprocessor.fit_transform(df, 'Appliances')
    y_inv = TSprocessor.inverse_transform(y)
    X_inv = TSprocessor.inverse_transform(X)
    assert y_inv.max() > 1 and X_inv.max() > 1


def test_MultivariateTS_fit():
    df = datasets.load_energy_data()
    TSprocessor = core.MultivariateTS(1680, 240, scaler=MinMaxScaler)
    TSprocessor.fit(df, train_columns=['Appliances', 'T1', 'RH_1'], pred_columns=['Appliances', 'T1'])
    assert TSprocessor.scaler_dict['Appliances'].data_max_ is not None
    assert TSprocessor.scaler_dict['Appliances'].data_max_ != TSprocessor.scaler_dict['T1'].data_max_


def test_MultivariateTS_fit_transform():
    df = datasets.load_energy_data()
    TSprocessor = core.MultivariateTS(1680, 240, scaler=MinMaxScaler)
    X, y = TSprocessor.fit_transform(df, train_columns=['Appliances', 'T1', 'RH_1'], pred_columns=['Appliances', 'T1'])
    assert TSprocessor.scaler_dict['Appliances'].data_max_ is not None
    assert TSprocessor.scaler_dict['Appliances'].data_max_ != TSprocessor.scaler_dict['T1'].data_max_
    assert X.shape == (17816, 1680, 3)
