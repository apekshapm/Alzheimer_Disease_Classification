# 🧠 Alzheimer's Disease Classification

A machine learning application that predicts Alzheimer's disease risk using patient demographic, clinical, and cognitive data with a Random Forest classifier.

## 📋 Features

- **Single Patient Prediction**: Get predictions for individual patients
- **Batch Prediction**: Upload CSV files for multiple patient predictions
- **Model Metrics**: View accuracy, confusion matrix, and classification report
- **Feature Importance Analysis**: Identify key predictors (MMSE scores, hypertension, etc.)
- **Interactive Visualizations**: Histograms, box plots, and confusion matrices

## 🛠️ Tech Stack

- **Streamlit** - Web app framework
- **Scikit-learn** - Machine learning (Random Forest)
- **Pandas** - Data manipulation
- **Matplotlib & Seaborn** - Visualizations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/apekshapm/Alzheimer_Disease_Classification.git
cd Alzheimer_Disease_Classification
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place your dataset:
   - Add `alzheimers_disease_data.csv` in the repository root directory

## 🚀 Running Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📂 Dataset Structure

Expected CSV columns:
- `Age` - Patient age
- `Gender` - Male/Female
- `Ethnicity` - Ethnicity information
- `Diagnosis` - Target variable (Alzheimer's status)
- Clinical and cognitive features (MMSE scores, etc.)

## 🌐 Live Deployment

### Deploy to Streamlit Cloud ⭐ RECOMMENDED

1. Repository is already connected to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select:
   - Repository: `apekshapm/Alzheimer_Disease_Classification`
   - Branch: `main`
   - Main file path: `app.py`
6. Click Deploy!

**Your live app will be available at**: 
```
https://share.streamlit.io/apekshapm/Alzheimer_Disease_Classification/main/app.py
```

### Alternative Deployment Options

- **Railway.app** - Free tier with easy GitHub integration
- **Render** - Free tier with automatic deployments
- **Heroku** - Paid option with reliable uptime
- **PythonAnywhere** - Python-specific hosting

## 📊 Model Performance

- **Algorithm**: Random Forest Classifier (100 trees)
- **Test Set Size**: 20% of data
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Key Predictors**: MMSE scores, Hypertension status, Age

## 💻 Usage Guide

### Single Prediction
1. Navigate to "Single Prediction" tab
2. Enter patient age and gender
3. Click "Predict" button
4. View diagnosis prediction

### Batch Prediction
1. Navigate to "Batch Prediction" tab
2. Upload CSV file with patient data
3. Review uploaded data
4. Predictions appear automatically
5. Download results as CSV

### Model Metrics
1. Navigate to "Model Metrics" tab
2. View:
   - Model accuracy and dataset size
   - Confusion matrix heatmap
   - Classification report (precision, recall, F1)
   - Feature importance chart

## 🐛 Troubleshooting

**"Dataset not found" error**:
- Ensure `alzheimers_disease_data.csv` is in the root directory
- Or upload it to the batch prediction section

**Column mismatch errors**:
- Verify your CSV has required columns: Age, Gender, Ethnicity, Diagnosis

**Predictions not loading**:
- Check that input features match training data format

## 📝 Project Structure

```
Alzheimer_Disease_Classification/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── alzheimers_disease_data.csv    # Dataset (add this)
├── README.md                       # This file
├── .gitignore                      # Git ignore file
└── .streamlit/config.toml         # Streamlit configuration
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Apeksha P M**
- GitHub: [@apekshapm](https://github.com/apekshapm)
- Repository: [Alzheimer_Disease_Classification](https://github.com/apekshapm/Alzheimer_Disease_Classification)

## 📧 Support

For issues or questions, please open a GitHub issue in the repository.

---

**✨ Ready to Deploy!** Your app is fully configured for Streamlit Cloud deployment. 🚀
