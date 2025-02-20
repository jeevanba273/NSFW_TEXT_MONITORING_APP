import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
import os

# Load data from CSV files
df1 = pd.read_csv('hatespeech/dataset/final_training.csv')
df2 = pd.read_csv('hatespeech/dataset/labeled_data.csv')
df3 = pd.read_csv('hatespeech/dataset/test.csv')

# Print column names for debugging
print("Columns in df1:", df1.columns)
print("Columns in df2:", df2.columns)
print("Columns in df3:", df3.columns)

# Preprocess each dataframe
def preprocess_df(df, text_col, label_col):
    df = df[[text_col, label_col]].copy()
    df.columns = ['text', 'label']
    df['text'] = df['text'].fillna('')
    df['label'] = df['label'].fillna(-1)  # Fill NaN with -1
    return df

df1 = preprocess_df(df1, 'Review', 'Label')
df2 = preprocess_df(df2, 'tweet', 'class')
df3 = preprocess_df(df3, 'comment_text', 'id')  # Assuming 'id' as a placeholder label

# Combine dataframes
df = pd.concat([df1, df2, df3], ignore_index=True)

# Remove rows with placeholder labels
df = df[df['label'] != -1]

texts = df['text'].tolist()
labels = df['label'].tolist()

print(f"Total samples: {len(texts)}")
print(f"Label distribution: {pd.Series(labels).value_counts()}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Create and fit the vectorizer with a limited vocabulary size
vectorizer = TfidfVectorizer(max_features=20000)  # Limit the number of features to reduce memory usage
X_train_vec = vectorizer.fit_transform(X_train)

# Create and fit the model
model = LogisticRegression(solver='liblinear')  # 'liblinear' is often more memory efficient for large datasets
model.fit(X_train_vec, y_train)

# Ensure the directory exists
os.makedirs("hatespeech/saved_models", exist_ok=True)

# Save the vectorizer and model
with open("hatespeech/saved_models/vectorizer.pkl", 'wb') as f:
    pickle.dump(vectorizer, f)

with open("hatespeech/saved_models/lr_model.pkl", 'wb') as f:
    pickle.dump(model, f)

print("Models saved successfully.")
