import pandas as pd

def load_data():
    users_df = pd.read_csv("../data/users.csv")
    hotels_df = pd.read_csv("../data/hotels.csv")
    return users_df, hotels_df

def clean_data(users_df, hotels_df):
    hotels_df["date"] = pd.to_datetime(hotels_df["date"], format="%m/%d/%Y")
    hotels_df["price"] = hotels_df["price"].astype(float)
    hotels_df["total"] = hotels_df["total"].astype(float)
    
    users_df["company"] = users_df["company"].str.lower().str.strip()
    
    return users_df, hotels_df

def save_cleaned_data(users_df, hotels_df):
    users_df.to_csv("../data/cleaned_users.csv", index=False)
    hotels_df.to_csv("../data/cleaned_hotels.csv", index=False)
    print("Cleaned datasets saved successfully!")

# Run Preprocessing
if __name__ == "__main__":
    users_df, hotels_df = load_data()
    users_df, hotels_df = clean_data(users_df, hotels_df)
    save_cleaned_data(users_df, hotels_df)