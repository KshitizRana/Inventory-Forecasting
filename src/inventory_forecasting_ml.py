import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from utils import convert_timestamp_to_hourly, download_from_s3, gcp


def feature_engg(data):
  """
  Performs feature engineering on the input dataset, including date extraction, categorical encoding, and filtering.
  Parameters
  ----------
  data : The input dataset containing a 'category' column, a 'timestamp' column, and other relevant features.
  
  Returns
  -------
  The transformed data with the following changes:
        - Rows with 'category' equal to 'spices and herbs' are removed.
        - The 'timestamp' column is converted to datetime format, and additional columns 'day', 'month', and 'year' are created based on the 'timestamp'.
        - The 'category' column is one-hot encoded (excluding the first category to avoid multicollinearity).
        - Missing values in the dataset are filled with 0.
  """
  data =  data[~data['category'].isin(['spices and herbs'])]
  # Convert 'timestamp' to datetime format
  data['timestamp'] = pd.to_datetime(data['timestamp'])
  
  # Create new features: 'day', 'month', 'year'
  data['day'] = data['timestamp'].dt.day
  data['month'] = data['timestamp'].dt.month
  data['year'] = data['timestamp'].dt.year
  data['hour'] = data['timestamp'].dt.hour
  
  # Create dummy variables for 'category' column
  data = pd.get_dummies(data, columns=['category'], drop_first=True)
  return data.fillna(0)


def split_data(data):
  """
  Splits the input data into training and testing sets for model development, excluding certain columns.
  Parameters
  ----------
  data : The input dataset containing features and target variables

  Returns
  -------
  X_train : Training set features.
    
    X_test : Testing set features.
    
    y_train : Training set target variable ('estimated_stock_pct').
    
    y_test : Testing set target variable ('estimated_stock_pct').
  """
  # Define target and features
  X = data.drop(columns=['estimated_stock_pct','timestamp', 'product_id'])
  y = data['estimated_stock_pct']
  
  # Split data into train and test sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  return X_train, X_test, y_train, y_test


def rf_mod(X_train, X_test, y_train, y_test):
  """Trains a Random Forest Regressor model on the provided training data, scales the features, and evaluates the model using RMSE on the test set.

  Parameters
  ----------
  X_train : The training input samples.
  X_test : The testing input samples for which predictions are made.
  y_train : The target values for training the model.
  y_test : The target values for evaluating the model's predictions.

  Returns
  -------
  The trained Random Forest model.
  The fitted StandardScaler used to transform the data.
  Predicted target values for the test set.
  """
  rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  rf_model.fit(X_train_scaled, y_train)

  # Make predictions on the test set
  y_pred = rf_model.predict(X_test_scaled)
  rmse = np.sqrt(mean_squared_error(y_test, y_pred)) #or use mae
  print(f"RMSE: {rmse}")
  return rf_model, scaler, y_pred


def forecast_for_three_months(data):
  """
  Function to forecast for the next three months on the hourly basis .
  Parameters
  ----------
  data : The historical data required to forecast.

  Returns
  -------
  Returns forecasted data after applying the RandomForestRegressor Model.
  """
  # Generate future dates (e.g., for 3 months)
  future_dates = pd.date_range(start=data['timestamp'].max(), periods=90, freq='D')
  future_data = pd.DataFrame(future_dates, columns=['timestamp'])
  future_data['timestamp'] = convert_timestamp_to_hourly(future_data,'timestamp') #conveting to hourly basis
  
  # Assuming the product ID, unit_price, and temperature remain consistent, use the median or mode from historical data
  future_data['product_id'] = data['product_id']
  future_data = future_data.merge(data,how='inner',on='product_id')\
                           .drop(['timestamp_y','estimated_stock_pct','temperature'],axis=1)\
                            .rename(columns={'timestamp_x':'timestamp'})
    
  future_data['quantity'] = 0  # Assuming no future sales
  future_data['temperature'] = data['temperature'].median()  # Adjust as needed
  
  # Add forecast flag
  future_data['is_forecast'] = True  
  return  future_data


def process():
  """Function Run whole script step by step
  """
  # step 1
  s3_df = download_from_s3(bucket='inventory-agg-data', key_name = 'Inventory_historical_data.csv')
  
  # step 2
  df_feat = feature_engg(s3_df)
  
  # step 3
  X_train, X_test, y_train, y_test =split_data(df_feat)
  X_train.shape, X_test.shape, y_train.shape, y_test.shape
  
  # step 4
  rf_model, scaler, y_pred = rf_mod(X_train, X_test, y_train, y_test)
  future_data = forecast_for_three_months(s3_df)
  future_data = feature_engg(future_data).drop(columns=['product_id','timestamp'])
  forecast_pred = rf_model.predict(scaler.transform(future_data[X_train.columns]))
  future_data['estimated_stock_pct'] = forecast_pred
  final_data = pd.concat([df_feat.drop(columns=['timestamp','product_id']), future_data], ignore_index=True)

  # cat_df = final_data[final_data.columns[pd.Series(final_data.columns).str.startswith('category_')]]
  cat_df = final_data.filter(like='category_')
  final_data['category'] = cat_df.idxmax(axis=1).str.replace('category_','')
  final_data['timestamp'] = pd.to_datetime(final_data[['year','month','day','hour']])
  final_df = final_data.drop(columns=cat_df.columns,axis=1).fillna(0)
  
  gcp(final_df,'1vhmJcfz7DINZPha-y7TR4gB5pe-h_GwdFy-FfqIrUgk','Forecasting-data')
  
process()