import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("Alzheimer's Disease Prediction")

# Load the dataset
@st.cache_data  # Cache the dataset to avoid reloading it every time
def load_data():
    # Replace this path with the correct path to your dataset
    df = pd.read_csv(r"C:\Data science\Alzheimer's Disease Classification\Alzheimer's Disease Classification\alzheimers_disease_data.csv")
    df = df.dropna()  # Handle missing values
    # Convert categorical columns to numeric using one-hot encoding
    df = pd.get_dummies(df, columns=['Gender', 'Ethnicity'], drop_first=True)
    return df

df = load_data()

# Split the data into features and target
X = df.drop(columns=['Diagnosis'])
y = df['Diagnosis']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
@st.cache_resource  # Cache the model to avoid retraining every time
def train_model():
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

model = train_model()

# Make predictions on the test set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Sidebar for navigation
st.sidebar.header("Navigation")
option = st.sidebar.radio("Choose an option", ["Single Prediction", "Batch Prediction", "Model Metrics"])

# Single Prediction
if option == "Single Prediction":
    st.header("Single Patient Prediction")
    
    # Input fields for single prediction
    age = st.number_input('Age', min_value=0, max_value=120, value=50)
    gender = st.selectbox('Gender', ['Male', 'Female'])
    # Add more fields as necessary based on your dataset
    
    if st.button('Predict'):
        # Create a DataFrame from the inputs
        input_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            # Add more fields as necessary
        })
        
        # Ensure the input data has the same columns as the training data
        input_data = pd.get_dummies(input_data, columns=['Gender'], drop_first=True)
        
        # Align columns with the training data
        input_data = input_data.reindex(columns=X.columns, fill_value=0)
        
        # Make a prediction
        prediction = model.predict(input_data)
        
        # Display the prediction
        st.success(f'Prediction: {prediction[0]}')

# Batch Prediction
elif option == "Batch Prediction":
    st.header("Batch Prediction from CSV")
    uploaded_file = st.file_uploader("Upload a CSV file with patient data", type=["csv"])
    
    if uploaded_file is not None:
        # Read the uploaded file
        batch_data = pd.read_csv(uploaded_file)
        
        # Display the uploaded data
        st.write("Uploaded Data:")
        st.write(batch_data)
        
        # Ensure the input data has the same columns as the training data
        batch_data = pd.get_dummies(batch_data, columns=['Gender', 'Ethnicity'], drop_first=True)
        batch_data = batch_data.reindex(columns=X.columns, fill_value=0)
        
        # Make predictions
        predictions = model.predict(batch_data)
        
        # Add predictions to the DataFrame
        batch_data['Prediction'] = predictions
        
        # Display the predictions
        st.write("Predictions:")
        st.write(batch_data)
        
        # Download the predictions as a CSV file
        st.download_button(
            label="Download Predictions",
            data=batch_data.to_csv(index=False),
            file_name='predictions.csv',
            mime='text/csv',
        )

# Model Metrics
elif option == "Model Metrics":
    st.header("Model Performance Metrics")
    
    # Display model accuracy
    st.subheader(f"Model Accuracy: {accuracy:.2f}")
    
    # Confusion Matrix
    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    st.pyplot(fig)
    
    # Classification Report
    st.subheader("Classification Report")
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.write(report_df)