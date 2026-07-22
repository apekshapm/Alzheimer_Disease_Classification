import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title("Alzheimer's Disease Prediction")

# Columns that are identifiers / not predictive features and must be
# dropped before training (DoctorInCharge is text and will crash sklearn;
# PatientID is just a row identifier).
DROP_COLS = ['PatientID', 'DoctorInCharge']

# Ethnicity is a nominal (unordered) category in this dataset, so it gets
# one-hot encoded. Gender is already binary (0/1) and EducationLevel is
# ordinal (0-3), so both are left as-is - no need to dummy-encode them.
CATEGORICAL_COLS = ['Ethnicity']


@st.cache_data  # Cache the dataset so it isn't reloaded on every interaction
def load_data():
    dataset_path = os.path.join(os.path.dirname(__file__), "alzheimers_disease_data.csv")

    if not os.path.exists(dataset_path):
        st.error(f"Dataset not found at: {dataset_path}")
        st.info("Please ensure 'alzheimers_disease_data.csv' is in the app directory")
        st.stop()

    df = pd.read_csv(dataset_path)
    df = df.dropna()
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    df = pd.get_dummies(df, columns=CATEGORICAL_COLS, drop_first=True)
    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")
    st.stop()

# Features / target
X = df.drop(columns=['Diagnosis'])
y = df['Diagnosis']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


@st.cache_resource  # Cache the trained model, keyed on its training data
def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model


model = train_model(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Sidebar navigation
st.sidebar.header("Navigation")
option = st.sidebar.radio("Choose an option", ["Single Prediction", "Batch Prediction", "Model Metrics"])


def encode_and_align(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Apply the same encoding used during training, then align columns
    with the training feature set so the model always sees the exact
    columns it was fit on, in the exact same order."""
    raw_df = raw_df.drop(columns=[c for c in DROP_COLS if c in raw_df.columns])
    encoded = pd.get_dummies(raw_df, columns=CATEGORICAL_COLS, drop_first=True)
    encoded = encoded.reindex(columns=X.columns, fill_value=0)
    return encoded


# ---------------------------------------------------------------------
# Single Prediction
# ---------------------------------------------------------------------
if option == "Single Prediction":
    st.header("Single Patient Prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Demographics")
        age = st.number_input('Age', min_value=0, max_value=120, value=73)
        gender = st.selectbox('Gender', options=[0, 1], format_func=lambda x: 'Male' if x == 0 else 'Female')
        ethnicity = st.selectbox('Ethnicity', options=[0, 1, 2, 3])
        education = st.selectbox('Education Level', options=[0, 1, 2, 3])

        st.subheader("Lifestyle")
        bmi = st.number_input('BMI', min_value=0.0, max_value=60.0, value=23.0)
        smoking = st.selectbox('Smoking', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        alcohol = st.number_input('Alcohol Consumption (units/week)', min_value=0.0, max_value=30.0, value=10.0)
        physical_activity = st.number_input('Physical Activity (hrs/week)', min_value=0.0, max_value=20.0, value=5.0)
        diet_quality = st.number_input('Diet Quality (0-10)', min_value=0.0, max_value=10.0, value=5.0)
        sleep_quality = st.number_input('Sleep Quality (0-10)', min_value=0.0, max_value=10.0, value=7.0)

    with col2:
        st.subheader("Medical History")
        family_history = st.selectbox('Family History of Alzheimers', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        cardiovascular = st.selectbox('Cardiovascular Disease', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        diabetes = st.selectbox('Diabetes', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        depression = st.selectbox('Depression', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        head_injury = st.selectbox('Head Injury', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        hypertension = st.selectbox('Hypertension', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')

        st.subheader("Vitals & Labs")
        systolic_bp = st.number_input('Systolic BP', min_value=60, max_value=250, value=120)
        diastolic_bp = st.number_input('Diastolic BP', min_value=40, max_value=150, value=80)
        cholesterol_total = st.number_input('Total Cholesterol', min_value=0.0, max_value=400.0, value=200.0)
        cholesterol_ldl = st.number_input('LDL Cholesterol', min_value=0.0, max_value=300.0, value=100.0)
        cholesterol_hdl = st.number_input('HDL Cholesterol', min_value=0.0, max_value=150.0, value=50.0)
        cholesterol_trig = st.number_input('Triglycerides', min_value=0.0, max_value=500.0, value=150.0)

    with col3:
        st.subheader("Cognitive & Functional")
        mmse = st.number_input('MMSE Score (0-30)', min_value=0.0, max_value=30.0, value=25.0)
        functional_assessment = st.number_input('Functional Assessment (0-10)', min_value=0.0, max_value=10.0, value=7.0)
        memory_complaints = st.selectbox('Memory Complaints', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        behavioral_problems = st.selectbox('Behavioral Problems', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        adl = st.number_input('ADL Score (0-10)', min_value=0.0, max_value=10.0, value=7.0)
        confusion = st.selectbox('Confusion', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        disorientation = st.selectbox('Disorientation', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        personality_changes = st.selectbox('Personality Changes', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        difficulty_tasks = st.selectbox('Difficulty Completing Tasks', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
        forgetfulness = st.selectbox('Forgetfulness', options=[0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')

    if st.button('Predict', type='primary'):
        input_data = pd.DataFrame([{
            'Age': age,
            'Gender': gender,
            'Ethnicity': ethnicity,
            'EducationLevel': education,
            'BMI': bmi,
            'Smoking': smoking,
            'AlcoholConsumption': alcohol,
            'PhysicalActivity': physical_activity,
            'DietQuality': diet_quality,
            'SleepQuality': sleep_quality,
            'FamilyHistoryAlzheimers': family_history,
            'CardiovascularDisease': cardiovascular,
            'Diabetes': diabetes,
            'Depression': depression,
            'HeadInjury': head_injury,
            'Hypertension': hypertension,
            'SystolicBP': systolic_bp,
            'DiastolicBP': diastolic_bp,
            'CholesterolTotal': cholesterol_total,
            'CholesterolLDL': cholesterol_ldl,
            'CholesterolHDL': cholesterol_hdl,
            'CholesterolTriglycerides': cholesterol_trig,
            'MMSE': mmse,
            'FunctionalAssessment': functional_assessment,
            'MemoryComplaints': memory_complaints,
            'BehavioralProblems': behavioral_problems,
            'ADL': adl,
            'Confusion': confusion,
            'Disorientation': disorientation,
            'PersonalityChanges': personality_changes,
            'DifficultyCompletingTasks': difficulty_tasks,
            'Forgetfulness': forgetfulness,
        }])

        input_encoded = encode_and_align(input_data)
        prediction = model.predict(input_encoded)[0]
        probability = model.predict_proba(input_encoded)[0]

        if prediction == 1:
            st.error(f"Prediction: **Alzheimer's Diagnosis Positive** (confidence: {probability[1]:.1%})")
        else:
            st.success(f"Prediction: **Alzheimer's Diagnosis Negative** (confidence: {probability[0]:.1%})")

# ---------------------------------------------------------------------
# Batch Prediction
# ---------------------------------------------------------------------
elif option == "Batch Prediction":
    st.header("Batch Prediction from CSV")
    st.caption("Upload a CSV with the same feature columns as the training data (Diagnosis column not required).")
    uploaded_file = st.file_uploader("Upload a CSV file with patient data", type=["csv"])

    if uploaded_file is not None:
        try:
            batch_raw = pd.read_csv(uploaded_file)

            st.write("Uploaded Data:")
            st.dataframe(batch_raw)

            # Columns required before encoding (i.e. everything the model
            # needs, in raw un-encoded form)
            required_raw_cols = set(X.columns) - {c for c in X.columns if c.startswith('Ethnicity_')}
            required_raw_cols |= {'Ethnicity'}
            missing_cols = required_raw_cols - set(batch_raw.columns)
            if missing_cols:
                st.error(f"Uploaded file is missing required columns: {sorted(missing_cols)}")
                st.stop()

            batch_encoded = encode_and_align(batch_raw.copy())
            predictions = model.predict(batch_encoded)
            probabilities = model.predict_proba(batch_encoded)[:, 1]

            results = batch_raw.copy()
            results['Prediction'] = predictions
            results['Probability_Positive'] = probabilities.round(3)

            st.write("Predictions:")
            st.dataframe(results)

            st.download_button(
                label="Download Predictions",
                data=results.to_csv(index=False),
                file_name='predictions.csv',
                mime='text/csv',
            )
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")

# ---------------------------------------------------------------------
# Model Metrics
# ---------------------------------------------------------------------
elif option == "Model Metrics":
    st.header("Model Performance Metrics")

    st.subheader(f"Model Accuracy: {accuracy:.2%}")

    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['No Alzheimers', 'Alzheimers'],
                yticklabels=['No Alzheimers', 'Alzheimers'])
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    st.pyplot(fig)

    st.subheader("Classification Report")
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.dataframe(report_df)

    st.subheader("Feature Importance")
    importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(15)

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.barplot(data=importance_df, x='Importance', y='Feature', ax=ax2)
    ax2.set_title('Top 15 Most Important Features')
    st.pyplot(fig2)
