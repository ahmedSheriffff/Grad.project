# -*- coding: utf-8 -*-
"""PoofOfConcept(AI|12).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GT-uA9T3646xIKR5no2R38EmT8gJAaxC
"""

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras import mixed_precision
import matplotlib.pyplot as plt
import seaborn as sns

# Check for GPU availability
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Allow TensorFlow to dynamically allocate memory on the GPU
tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0], True)

# Load the datasets
ds1 = pd.read_csv('ds1.csv')  # Replace with the correct path to ds1.csv
ds2 = pd.read_csv('ds2.csv', encoding='ISO-8859-1')  # or 'latin1'

# Preprocess ds2 (Email Type column)
ds2['Email Type'] = ds2['Email Type'].replace({'Phishing Email': 1, 'Safe Email': 0})

# Rename columns in ds1 to match the format of ds2
ds1 = ds1.rename(columns={'text': 'Email Text', 'spam': 'Email Type'})

# Combine both datasets
combined_data = pd.concat([ds1[['Email Text', 'Email Type']], ds2[['Email Text', 'Email Type']]])

# Check for missing values and drop them
combined_data.dropna(inplace=True)

# Check for invalid values in 'Email Type' column and filter out non-0/1 entries
valid_types = [0, 1]
combined_data = combined_data[combined_data['Email Type'].isin(valid_types)]

# Convert Email Type to integers
combined_data['Email Type'] = combined_data['Email Type'].astype(int)

# Extract features and labels
X = combined_data['Email Text']
y = combined_data['Email Type']

# Visualize the data distribution
sns.countplot(x='Email Type', data=combined_data)
plt.title('Distribution of Email Types')
plt.show()

# Preprocessing: Transform the text data using TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
X_tfidf = tfidf.fit_transform(X).toarray()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.5, random_state=42)

# Define models to be used
models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'SVM': SVC(),
    'Random Forest': RandomForestClassifier(),
    'Decision Tree': DecisionTreeClassifier()
}

# Train and evaluate each model
model_accuracies = {}
for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    model_accuracies[model_name] = accuracy
    print(f'{model_name} Accuracy: {accuracy:.4f}')

# Visualize model accuracies
plt.figure(figsize=(10, 5))
sns.barplot(x=list(model_accuracies.keys()), y=list(model_accuracies.values()))
plt.title('Model Accuracies')
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.show()

# Deep learning model: Tokenize and pad sequences for deep learning
max_words = 5000
max_len = 500
tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)
X_padded = pad_sequences(X_seq, maxlen=max_len)

X_train_dl, X_test_dl, y_train_dl, y_test_dl = train_test_split(X_padded, y, test_size=0.2, random_state=42)

# Enable mixed precision training (faster on GPUs)
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

# Build the deep learning model
model_dl = Sequential()
model_dl.add(Dense(128, activation='relu', input_shape=(max_len,)))
model_dl.add(Dropout(0.5))
model_dl.add(Dense(64, activation='relu'))
model_dl.add(Dropout(0.5))
model_dl.add(Dense(1, activation='sigmoid'))

model_dl.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the deep learning model
model_dl.fit(X_train_dl, y_train_dl, epochs=5, batch_size=32, validation_split=0.2, verbose=2)

# Evaluate the deep learning model
loss, accuracy_dl = model_dl.evaluate(X_test_dl, y_test_dl, verbose=0)
print(f'Deep Learning Model Accuracy: {accuracy_dl:.4f}')

# Print the best model
model_accuracies['Deep Learning'] = accuracy_dl
best_model = max(model_accuracies, key=model_accuracies.get)
print(f'Highest Accuracy Model: {best_model} with accuracy {model_accuracies[best_model]:.4f}')

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import mixed_precision
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Check for GPU availability
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

# Allow TensorFlow to dynamically allocate memory on the GPU
tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0], True)

# Load the datasets
ds1 = pd.read_csv('ds1.csv')  # Replace with the correct path to ds1.csv
ds2 = pd.read_csv('ds2.csv', encoding='ISO-8859-1')  # or 'latin1'

# Preprocess ds2 (Email Type column)
ds2['Email Type'] = ds2['Email Type'].replace({'Phishing Email': 1, 'Safe Email': 0})

# Rename columns in ds1 to match the format of ds2
ds1 = ds1.rename(columns={'text': 'Email Text', 'spam': 'Email Type'})

# Combine both datasets
combined_data = pd.concat([ds1[['Email Text', 'Email Type']], ds2[['Email Text', 'Email Type']]])

# Check for missing values and drop them
combined_data.dropna(inplace=True)

# Check for invalid values in 'Email Type' column and filter out non-0/1 entries
valid_types = [0, 1]
combined_data = combined_data[combined_data['Email Type'].isin(valid_types)]

# Convert Email Type to integers
combined_data['Email Type'] = combined_data['Email Type'].astype(int)

# Extract features and labels
X = combined_data['Email Text']
y = combined_data['Email Type']

# Visualize the data distribution
sns.countplot(x='Email Type', data=combined_data)
plt.title('Distribution of Email Types')
plt.show()

# Pie chart for class distribution
combined_data['Email Type'].value_counts().plot.pie(
    labels=['Safe Email', 'Phishing Email'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['lightblue', 'orange']
)
plt.title('Class Distribution of Email Types')
plt.ylabel('')  # Remove y-axis label
plt.show()

# Word clouds for each class
phishing_text = " ".join(combined_data[combined_data['Email Type'] == 1]['Email Text'])
safe_text = " ".join(combined_data[combined_data['Email Type'] == 0]['Email Text'])

# Phishing Emails Word Cloud
plt.figure(figsize=(12, 6))
wordcloud_phishing = WordCloud(width=800, height=400, background_color='black').generate(phishing_text)
plt.imshow(wordcloud_phishing, interpolation='bilinear')
plt.title('Word Cloud for Phishing Emails')
plt.axis('off')
plt.show()

# Safe Emails Word Cloud
plt.figure(figsize=(12, 6))
wordcloud_safe = WordCloud(width=800, height=400, background_color='white').generate(safe_text)
plt.imshow(wordcloud_safe, interpolation='bilinear')
plt.title('Word Cloud for Safe Emails')
plt.axis('off')
plt.show()

# Preprocessing: Transform the text data using TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
X_tfidf = tfidf.fit_transform(X).toarray()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.5, random_state=42)

# Define models to be used
models = {
    'Naive Bayes': MultinomialNB(),
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'SVM': SVC(),
    'Random Forest': RandomForestClassifier(),
    'Decision Tree': DecisionTreeClassifier()
}

# Train and evaluate each model
model_accuracies = {}
for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    model_accuracies[model_name] = accuracy
    print(f'{model_name} Accuracy: {accuracy:.4f}')

    # Confusion matrix for each model
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Safe', 'Phishing'])
    disp.plot(cmap='Blues')
    plt.title(f'Confusion Matrix for {model_name}')
    plt.show()

# Visualize model accuracies
plt.figure(figsize=(10, 5))
sns.barplot(x=list(model_accuracies.keys()), y=list(model_accuracies.values()))
plt.title('Model Accuracies')
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.show()

# Deep learning model: Tokenize and pad sequences for deep learning
max_words = 5000
max_len = 500
tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)
X_padded = pad_sequences(X_seq, maxlen=max_len)

X_train_dl, X_test_dl, y_train_dl, y_test_dl = train_test_split(X_padded, y, test_size=0.2, random_state=42)

# Enable mixed precision training (faster on GPUs)
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)

# Build the deep learning model
model_dl = Sequential()
model_dl.add(Dense(128, activation='relu', input_shape=(max_len,)))
model_dl.add(Dropout(0.5))
model_dl.add(Dense(64, activation='relu'))
model_dl.add(Dropout(0.5))
model_dl.add(Dense(1, activation='sigmoid'))

model_dl.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the deep learning model
history = model_dl.fit(X_train_dl, y_train_dl, epochs=5, batch_size=32, validation_split=0.2, verbose=2)

# Evaluate the deep learning model
loss, accuracy_dl = model_dl.evaluate(X_test_dl, y_test_dl, verbose=0)
print(f'Deep Learning Model Accuracy: {accuracy_dl:.4f}')

# Loss and accuracy plots
plt.figure(figsize=(10, 5))
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Deep Learning Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Deep Learning Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Feature importance for Random Forest
if 'Random Forest' in models:
    rf_model = models['Random Forest']
    feature_importances = rf_model.feature_importances_
    sorted_idx = np.argsort(feature_importances)[-20:]  # Top 20 features

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(sorted_idx)), feature_importances[sorted_idx], align='center')
    plt.yticks(range(len(sorted_idx)), [tfidf.get_feature_names_out()[i] for i in sorted_idx])
    plt.title('Top 20 Important Features (Random Forest)')
    plt.xlabel('Feature Importance')
    plt.ylabel('Feature')
    plt.show()

# Print the best model
model_accuracies['Deep Learning'] = accuracy_dl
best_model = max(model_accuracies, key=model_accuracies.get)
print(f'Highest Accuracy Model: {best_model} with accuracy {model_accuracies[best_model]:.4f}')