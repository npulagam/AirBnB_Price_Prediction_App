import streamlit as st
import pickle
from io import BytesIO
import requests
import pandas as pd 
# Code from Best Pipeline.py here


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('https://raw.githubusercontent.com/npulagam/AirBnB_Price_Prediction_App/master/Test_Guild_6/prepared_data.csv')
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -30402.36212898424
exported_pipeline = RandomForestRegressor(bootstrap=True, max_features=0.55, min_samples_leaf=2, min_samples_split=6, n_estimators=100)

exported_pipeline.fit(training_features, training_target)


######################
# User defined values
title = 'NewYork AirBnB Price Prediction '
encoder_location = 'https://github.com/npulagam/AirBnB_Price_Prediction_App/blob/master/Test_Guild_6/encoder.pkl?raw=true'
target_encoder_location = ''
if len(encoder_location) > 5:
    mfile = BytesIO(requests.get(encoder_location).content)
    encoder = pickle.load(mfile)
    df = encoder.inverse_transform(features)
else:
    df = features.copy()
if len(target_encoder_location) > 5:
    mfile = BytesIO(requests.get(target_encoder_location).content)
    target_encoder = pickle.load(mfile)
st.title(title)
st.sidebar.header('User Input Parameters')
st.subheader('User Input parameters')
selected_data = dict()
for column in df.columns:
    if column != 'target':
        label = column.replace('_id.','')
        label = label.replace('_',' ').title()
        if df[column].dtype == 'O':
            selected_value = st.sidebar.selectbox(label, list(df[column].unique()))
        elif df[column].dtype == 'int64':
            selected_value = st.sidebar.number_input(label, min_value=df[column].min(), max_value=df[column].max(), value=df[column].iloc[0], step=1)
        elif df[column].dtype == 'float64':
            selected_value = st.sidebar.number_input(label, min_value=df[column].min(), max_value=df[column].max(), value=df[column].iloc[0])
        
        selected_data[column] = selected_value
test_data = pd.DataFrame(selected_data, index=[0])
st.write(test_data)
st.subheader('Prediction')
if len(encoder_location) > 5:
    test_data = encoder.transform(test_data) 
prediction = exported_pipeline.predict(test_data)
if len(target_encoder_location) > 5:
    prediction = target_encoder.inverse_transform(prediction)
if 'float' in str(type(prediction[0])):
    st.write(round(prediction[0],2))
else:
    st.write(prediction[0])
    