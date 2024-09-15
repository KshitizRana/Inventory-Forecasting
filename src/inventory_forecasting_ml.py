# create the following functions as instructed. Do not forget to follow best practices: add type hints, docstrings as required

# function 01: feature engineering -> return data
# read s3 data
import numpy as np
import pandas as pd

from src.utils import download_from_s3,gcp

def feature_engg(data):
  """
  
  Returns
  -------
 
  """
  data =  data[data['category'].isin(['spices and herbs'])]
  df = data.copy()
  data['timestamp'] = pd.to_datetime(data['timestamp'])
  data['day'] = data['timestamp'].dt.day
  data['month'] = data['timestamp'].dt.month
  data['year'] = data['timestamp'].dt.year
  data = pd.get_dummies(data, columns=['category'], drop_first=True)
  
  return data

# create a copy to be used later

# Convert 'timestamp' to datetime format

# Create new features: 'day', 'month', 'year'

# Create dummy variables for 'category' column



# function 02: split data -> return X_train, X_test, y_train, y_test
from sklearn.model_selection import train_test_split
def split_data(data):
  """_summary_

  Returns
  -------
 
  """
  X = data.drop(columns=['estimated_stock_pct', 'timestamp', 'product_id'])
  y = data['estimated_stock_pct']
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  return X_train, X_test, y_train, y_test
  
# Define target and features

# Split data into train and test sets


# function 03: Build xgboost model -> return preds & print rmse
import xgboost as xgb
from sklearn.metrics import mean_squared_error


def xgboost_mod(X_train, X_test, y_train, y_test):
  xgboost_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, max_depth=6)
  xgboost_model.fit(X_train, y_train)
  y_pred = xgboost_model.predict(X_test)
  rmse = np.sqrt(mean_squared_error(y_test, y_pred)) #or use mae
  print(f"RMSE: {rmse}")
  return y_pred
   
# Initialize XGBoost regressor

# Train the model

# Predictions on the test set

# Evaluate the model




# function 04: forecast for next 3 months -> return forecasts
# Generate future dates (e.g., for 3 months)

def forecast_for_three_months(data):
  future_dates = pd.date_range(start=data['timestamp'].max(), periods=90, freq='D')
  future_data = pd.DataFrame(future_dates, columns=['timestamp'])
  future_data['product_id'] = data['product_id']
  future_data['unit_price'] = data['unit_price']
  future_data['quantity'] = 0  # Assuming no future sales
  future_data['temperature'] = data['temperature'].median()  # Adjust as needed
  future_data['day'] = future_data['timestamp'].dt.day
  future_data['month'] = future_data['timestamp'].dt.month
  future_data['year'] = future_data['timestamp'].dt.year
  future_data['category'] = data['category']
  future_data = pd.get_dummies(future_data, columns=['category'], drop_first=True)
  future_data['is_forecast'] = True
  
  return  future_data

# Create a DataFrame for future data

# Assuming the product ID, unit_price, and temperature remain consistent, use the median or mode from historical data

# Create features for future data

# Create dummy variables for 'category'

# Predict estimated_stock_pct for the future data

# Add forecast flag




# function 05: to run all steps sequencially
def process():
  # step 1
  s3_df = download_from_s3(bucket='inventory-agg-data', key_name = 'Inventory_historical_data.csv')
  # step 2
  df_features = feature_engg(s3_df)
  # step 3
  Xtrain, ytrain, xtest, ytest =split_data(df_features)
  # step 4
  y_pred = xgboost_mod(Xtrain, xtest, ytrain, ytest)
  future_data = forecast_for_three_months(y_pred)
  # and then
  # Prepare the historical data
  historical_data = s3_df[['timestamp', 'estimated_stock_pct', 'product_id', 'unit_price', 'quantity', 'temperature']]
  # Add forecast flag to historical data
  historical_data['is_forecast'] = False
  
  # Ensure historical and future data have the same columns
  future_data = future_data[['timestamp', 'estimated_stock_pct', 'product_id', 'unit_price', 'quantity', 'temperature', 'is_forecast']]
  
  # Concatenate historical and future data
  final_data = pd.concat([historical_data, future_data], ignore_index=True)
  
  gcp(final_data,'1vhmJcfz7DINZPha-y7TR4gB5pe-h_GwdFy-FfqIrUgk','Forecasting-data')
  # Output final DataFrame for the dashboard
  print(final_data.head()) #-> upload to google sheet
