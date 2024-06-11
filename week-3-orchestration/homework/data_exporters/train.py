if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    numerical = ['trip_distance']

    dv = DictVectorizer()

    # Feature matrix for my model training
    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)

    # Feature matrix for my model training
    val_dicts = df_val[categorical + numerical].to_dict(orient='records')
    X_val = dv.transform(val_dicts)

    # Training part
    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    # Prediction part
    y_predict = lr.predict(X_val)

    # Evaluation part
mean_squared_error(y_val, y_predict, squared=False)


