import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load Cleaned Data
users_df = pd.read_csv("../data/cleaned_users.csv")
hotels_df = pd.read_csv("../data/cleaned_hotels.csv")

# EDA: Visualizing Hotel Price Distribution
sns.histplot(hotels_df["price"], bins=30, kde=True, color="blue")
plt.title("Hotel Price Distribution")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.savefig("../reports/figures/hotel_price_distribution.png")  # Save plot
plt.show()

# Train a Simple Price Prediction Model
X = hotels_df[["days"]]
y = hotels_df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate Model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model Performance: MAE = {mae:.2f}, R² = {r2:.2f}")