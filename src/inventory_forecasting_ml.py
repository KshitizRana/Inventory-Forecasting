# create the following functions as instructed. Do not forget to follow best practices: add type hints, docstrings as required

# function 01: feature engineering -> return data
# read s3 data
data = read from s3
data =  data[~data['category'].isin(['spices and herbs'])]

# create a copy to be used later
df = data.copy()

# Convert 'timestamp' to datetime format
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Create new features: 'day', 'month', 'year'
data['day'] = data['timestamp'].dt.day
data['month'] = data['timestamp'].dt.month
data['year'] = data['timestamp'].dt.year

# Create dummy variables for 'category' column
data = pd.get_dummies(data, columns=['category'], drop_first=True)



# function 02: split data -> return X_train, X_test, y_train, y_test
from sklearn.model_selection import train_test_split

# Define target and features
X = data.drop(columns=['estimated_stock_pct', 'timestamp', 'product_id'])
y = data['estimated_stock_pct']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# function 03: Build xgboost model -> return preds & print rmse
import xgboost as xgb
from sklearn.metrics import mean_squared_error

# Initialize XGBoost regressor
xgboost_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.05, max_depth=6)

# Train the model
xgboost_model.fit(X_train, y_train)

# Predictions on the test set
y_pred = xgboost_model.predict(X_test)

# Evaluate the model
rmse = np.sqrt(mean_squared_error(y_test, y_pred)) #or use mae
print(f"RMSE: {rmse}") 




# function 04: forecast for next 3 months -> return forecasts
# Generate future dates (e.g., for 3 months)
future_dates = pd.date_range(start=data['timestamp'].max(), periods=90, freq='D')

# Create a DataFrame for future data
future_data = pd.DataFrame(future_dates, columns=['timestamp'])

# Assuming the product ID, unit_price, and temperature remain consistent, use the median or mode from historical data
future_data['product_id'] = data['product_id']
future_data['unit_price'] = data['unit_price']
future_data['quantity'] = 0  # Assuming no future sales
future_data['temperature'] = data['temperature'].median()  # Adjust as needed

# Create features for future data
future_data['day'] = future_data['timestamp'].dt.day
future_data['month'] = future_data['timestamp'].dt.month
future_data['year'] = future_data['timestamp'].dt.year

# Create dummy variables for 'category'
future_data['category'] = df['category']
future_data = pd.get_dummies(future_data, columns=['category'], drop_first=True)

# Predict estimated_stock_pct for the future data
future_data['estimated_stock_pct'] = xgboost_model.predict(future_data.drop(columns=['timestamp', 'product_id']))

# Add forecast flag
future_data['is_forecast'] = True




# function 05: to run all steps sequencially
def process():
  # step 1
  # step 2
  # step 3
  # step 4
  
  # and then
  # Prepare the historical data
  historical_data = df[['timestamp', 'estimated_stock_pct', 'product_id', 'unit_price', 'quantity', 'temperature']]
  # Add forecast flag to historical data
  historical_data['is_forecast'] = False
  
  # Ensure historical and future data have the same columns
  future_data = future_data[['timestamp', 'estimated_stock_pct', 'product_id', 'unit_price', 'quantity', 'temperature', 'is_forecast']]
  
  # Concatenate historical and future data
  final_data = pd.concat([historical_data, future_data], ignore_index=True)
  
  # Output final DataFrame for the dashboard
  print(final_data.head()) #-> upload to google sheet
